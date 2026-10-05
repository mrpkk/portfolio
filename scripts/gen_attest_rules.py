#!/usr/bin/env python3
"""Сгенерировать demos/attest/rules.js из ЖИВОГО кода attest.

Правило: таблица сигнатур не копируется руками. Единственный источник истины —
/home/iamthat/Документы/work/sales/attest/attest/{poison,core,schema,service}.py.
Скрипт импортирует их и выгружает константы в JS, поэтому страница не может
разойтись с сервисом: regenerating after any rule change is one command.

    python3 /home/iamthat/portfolio/scripts/gen_attest_rules.py

Ключи окружения (ATTEST_SECRET и т.п.) вычищаются до импорта: в браузерную
страницу попадает только публичный dev-ключ, как и задумано в SPEC §2.3.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

ATTEST_SRC = Path("/home/iamthat/Документы/work/sales/attest")
OUT = Path("/home/iamthat/portfolio/demos/attest/rules.js")

# секреты в браузерную страницу не попадают — только dev-ключ
for _name in ("ATTEST_SECRET", "ATTEST_HMAC_KEY", "ATTEST_FREE_DAILY", "ATTEST_PRICE_ATOMS"):
    os.environ.pop(_name, None)

sys.path.insert(0, str(ATTEST_SRC))

from attest import core, poison, provenance, schema, service  # noqa: E402

# Python re -> JS RegExp. Все сигнатуры компилируются с IGNORECASE|MULTILINE.
# \b в Python unicode-aware (кириллица = буква), в JS — нет, поэтому заменяем
# на явную проверку \p{L}\p{N}_ с обеих сторон позиции.
_WB = (
    r"(?:(?<=[\p{L}\p{N}_])(?![\p{L}\p{N}_])|"
    r"(?<![\p{L}\p{N}_])(?=[\p{L}\p{N}_]))"
)


def _b(pattern: str) -> str:
    """Python re -> JS RegExp (u).

    1. \\b в Python unicode-aware (кириллица = буква), в JS нет -> заменяем
       на явную проверку \\p{L}\\p{N}_ с обеих сторон позиции границы.
    2. \" внутри класса символов — identity escape, который запрещён с флагом u.
    """
    return pattern.replace(r"\b", _WB).replace(r'\"', '"')


def _sig_flags(regex) -> str:
    flags = ""
    if regex.flags & re.IGNORECASE:
        flags += "i"
    if regex.flags & re.MULTILINE:
        flags += "m"
    if regex.flags & re.DOTALL:
        flags += "s"
    return flags or "m"


def build() -> dict:
    signatures = [
        {"name": name, "re": _b(rx.pattern), "flags": _sig_flags(rx)}
        for rx, name in poison.COMPILED
    ]

    helpers = {}
    for attr in (
        "BASE64_BLOB",
        "URL",
        "BARE_IP",
        "HIDDEN_TEXT",
        "ZERO_WIDTH",
        "CYRILLIC",
        "LATIN",
        "EMAIL",
        "OBFUSCATED_CONTACT",
        "IMPERATIVE",
        "CREDENTIAL_REF",
    ):
        rx = getattr(poison, attr)
        helpers[attr] = {"re": _b(rx.pattern), "flags": _sig_flags(rx)}

    fingerprints = {}
    for mod, modname in ((poison, "poison"), (core, "core"), (schema, "schema"), (service, "service")):
        mod_path = Path(mod.__file__)
        fingerprints[modname] = hashlib.sha256(mod_path.read_bytes()).hexdigest()[:16]

    return {
        "generated_from": {
            "repo": "mrpkk/attest (attest/poison.py, core.py, schema.py, service.py)",
            "sha256_16": fingerprints,
        },
        "signatures": signatures,
        "severity": poison.SEVERITY,
        "helpers": helpers,
        "sets": {
            "injectionKinds": sorted(core.INJECTION_KINDS),
            "dangerousCommands": sorted(core.DANGEROUS_COMMANDS),
            "criticalKinds": sorted(core.CRITICAL_KINDS),
            "trustworthyKeys": sorted(poison._TRUSTWORTHY_KEYS),
            "ssrfHosts": sorted(poison.SSRF_HOSTS),
            "metadataHosts": sorted(poison.METADATA_HOSTS),
        },
        "scoring": {
            "severityWeight": core.SEVERITY_WEIGHT,
            "violationWeight": core.VIOLATION_WEIGHT,
            "maxString": schema.MAX_STRING,
            "maxDepth": schema.MAX_DEPTH,
            "maxItems": schema.MAX_ITEMS,
            "walkListLimit": 500,
            "itemSchemaLimit": 1000,
            "invariantListLimit": 200,
        },
        "hardViolationRules": [
            "type",
            "required",
            "null",
            "depth",
            "empty",
            "size",
            "minimum",
            "maximum",
        ],
        "provenance": {
            "devKey": provenance._key_from_env().decode("utf-8"),
            "algorithm": "hmac-sha256",
        },
        "pricing": {
            "freeDaily": service.DEFAULT_FREE_DAILY,
            "plans": service.PRICING,
        },
    }


def main() -> int:
    data = build()
    body = json.dumps(data, ensure_ascii=False, indent=2)
    header = (
        "/* СГЕНЕРИРОВАНО — не редактировать руками.\n"
        "   Источник: mrpkk/attest, attest/poison.py + core.py + schema.py + service.py\n"
        "   Пересобрать: python3 /home/iamthat/portfolio/scripts/gen_attest_rules.py\n"
        "   Проверить соответствие: python3 /home/iamthat/portfolio/scripts/attest_conformance.py\n"
        "   sha256(первые 16): "
        + json.dumps(data["generated_from"]["sha256_16"], ensure_ascii=False)
        + "\n"
        "   dev-ключ ниже — публичный и годится только для демонстрации (SPEC 2.3). */\n"
        "(typeof window !== 'undefined' ? window : globalThis).ATTEST_RULES = "
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(header + body + ";\n", encoding="utf-8")
    print(f"записан {OUT}")
    print(f"сигнатур: {len(data['signatures'])}, хелперов: {len(data['helpers'])}")
    print("отпечатки исходников: " + json.dumps(data["generated_from"]["sha256_16"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())