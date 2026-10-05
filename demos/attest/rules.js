/* СГЕНЕРИРОВАНО — не редактировать руками.
   Источник: mrpkk/attest, attest/poison.py + core.py + schema.py + service.py
   Пересобрать: python3 /home/iamthat/portfolio/scripts/gen_attest_rules.py
   Проверить соответствие: python3 /home/iamthat/portfolio/scripts/attest_conformance.py
   sha256(первые 16): {"poison": "98b03cc91716c96c", "core": "27759fc5ad450330", "schema": "49dce8e0c1a09984", "service": "bd73d7e84ad8a221"}
   dev-ключ ниже — публичный и годится только для демонстрации (SPEC 2.3). */
(typeof window !== 'undefined' ? window : globalThis).ATTEST_RULES = {
  "generated_from": {
    "repo": "mrpkk/attest (attest/poison.py, core.py, schema.py, service.py)",
    "sha256_16": {
      "poison": "98b03cc91716c96c",
      "core": "27759fc5ad450330",
      "schema": "49dce8e0c1a09984",
      "service": "bd73d7e84ad8a221"
    }
  },
  "signatures": [
    {
      "name": "ignore_previous",
      "re": "ignore\\s+(all\\s+)?(previous|prior|above|earlier)\\s+(instructions?|prompts?|rules?|directions?)",
      "flags": "im"
    },
    {
      "name": "disregard_context",
      "re": "disregard\\s+(all\\s+)?(previous|prior|above|earlier|your)\\s+",
      "flags": "im"
    },
    {
      "name": "forget_instructions",
      "re": "forget\\s+(everything|all|your)\\s+(you|instructions?|rules?|training)",
      "flags": "im"
    },
    {
      "name": "role_override",
      "re": "(you\\s+are\\s+now|from\\s+now\\s+on\\s+you\\s+are)\\s+(\\w+\\s+){0,3}?(mode|assistant|agent|model|dan|pirate|hacker)",
      "flags": "im"
    },
    {
      "name": "prompt_injection",
      "re": "new\\s+(system\\s+)?(prompt|instructions?|rules?)\\s*:",
      "flags": "im"
    },
    {
      "name": "special_token_smuggle",
      "re": "<\\|?(im_start|im_end|system|endoftext)\\|?>",
      "flags": "im"
    },
    {
      "name": "role_block_smuggle",
      "re": "```\\s*(system|assistant)(?:(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_])|(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_]))",
      "flags": "im"
    },
    {
      "name": "exfiltrate_secrets",
      "re": "(reveal|print|show|output|repeat|send)\\s+(me\\s+)?(your|the)\\s+(system\\s+)?(prompt|instructions?|api[_ ]?key|secret|token|credential|password)",
      "flags": "im"
    },
    {
      "name": "exfiltrate_network",
      "re": "(send|post|exfiltrate|transmit|upload)\\s+(the\\s+)?(contents?|data|keys?|secrets?|credentials?)\\s+to\\s+https?://",
      "flags": "im"
    },
    {
      "name": "live_credential_shape",
      "re": "(?:(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_])|(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_]))(sk|pk|ghp|gho|xox[baprs])[-_][A-Za-z0-9_\\-]{16,}(?:(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_])|(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_]))",
      "flags": "im"
    },
    {
      "name": "aws_key_shape",
      "re": "(?:(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_])|(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_]))AKIA[0-9A-Z]{16}(?:(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_])|(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_]))",
      "flags": "im"
    },
    {
      "name": "private_key_material",
      "re": "-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----",
      "flags": "im"
    },
    {
      "name": "pem_material",
      "re": "-----BEGIN (?:CERTIFICATE|PUBLIC KEY)-----.*-----END",
      "flags": "im"
    },
    {
      "name": "destructive_command",
      "re": "rm\\s+-rf\\s+[/~]",
      "flags": "im"
    },
    {
      "name": "remote_exec_pipe",
      "re": "(curl|wget)\\s+[^\\s|]+\\s*\\|\\s*(ba)?sh",
      "flags": "im"
    },
    {
      "name": "obfuscated_exec",
      "re": "eval\\s*\\(\\s*(atob|base64|decode)",
      "flags": "im"
    },
    {
      "name": "conceal_from_user",
      "re": "do\\s+not\\s+(tell|inform|mention\\s+to|reveal\\s+to)\\s+(the\\s+)?(user|owner|human)",
      "flags": "im"
    },
    {
      "name": "conceal_from_user_ru",
      "re": "(without|без)\\s+(telling|informing|notifying|asking|уведомления|уведомляя)\\s+(the\\s+)?(user|owner|human|пользовател)",
      "flags": "im"
    },
    {
      "name": "conceal_from_user_ru",
      "re": "не\\s+(сообщай|сообщив|сообщая|уведомляй|уведомляя|говори|говоря|упомяни|раскрыва)\\w*\\s+(пользовател|юзер|owner|заказчик|владельц)",
      "flags": "im"
    },
    {
      "name": "conceal_from_user",
      "re": "(do\\s+not|never)\\s+(reveal|disclose|show)\\s+(this|it)\\s+to\\s+(the\\s+)?(user|human)",
      "flags": "im"
    },
    {
      "name": "remote_exec_pipe_line",
      "re": "^\\s*(?:sudo\\s+)?(?:curl|wget)(?:(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_])|(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_])).*\\|\\s*(?:ba)?sh",
      "flags": "im"
    },
    {
      "name": "urgency_override",
      "re": "important\\s*[:!]\\s*(?:you\\s+must|always|never)",
      "flags": "im"
    },
    {
      "name": "assistant_turn_smuggle",
      "re": "assistant\\s*:\\s*(?:ignore|disregard|forget)",
      "flags": "im"
    }
  ],
  "severity": {
    "exfiltrate_secrets": "critical",
    "exfiltrate_network": "critical",
    "live_credential_shape": "critical",
    "aws_key_shape": "critical",
    "private_key_material": "critical",
    "pem_material": "high",
    "obfuscated_exec": "critical",
    "remote_exec_pipe": "critical",
    "remote_exec_pipe_line": "critical",
    "destructive_command": "high",
    "ignore_previous": "high",
    "disregard_context": "high",
    "forget_instructions": "high",
    "prompt_injection": "high",
    "special_token_smuggle": "critical",
    "role_block_smuggle": "high",
    "assistant_turn_smuggle": "high",
    "role_override": "high",
    "conceal_from_user": "critical",
    "conceal_from_user_ru": "critical",
    "urgency_override": "low",
    "mixed_script_word": "critical"
  },
  "helpers": {
    "BASE64_BLOB": {
      "re": "(?:(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_])|(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_]))[A-Za-z0-9+/]{32,}={0,2}(?:(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_])|(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_]))",
      "flags": "m"
    },
    "URL": {
      "re": "https?://[^\\s\"'<>()\\[\\]]+[^\\s\"'<>()\\[\\],.;:!?]",
      "flags": "m"
    },
    "BARE_IP": {
      "re": "(?:(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_])|(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_]))(\\d{1,3}(?:\\.\\d{1,3}){3})(:\\d{1,5})?(?:(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_])|(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_]))",
      "flags": "m"
    },
    "HIDDEN_TEXT": {
      "re": "(?:color\\s*:\\s*(?:#fff(?:fff)?|white)|font-size\\s*:\\s*(?:0|0px|1px)|display\\s*:\\s*none|opacity\\s*:\\s*0)",
      "flags": "i"
    },
    "ZERO_WIDTH": {
      "re": "[\\u200b-\\u200f\\u2028\\u2029\\u202a-\\u202e\\u2060-\\u2064\\ufeff]",
      "flags": "m"
    },
    "CYRILLIC": {
      "re": "[\\u0400-\\u04ff]",
      "flags": "m"
    },
    "LATIN": {
      "re": "[a-z]",
      "flags": "i"
    },
    "EMAIL": {
      "re": "(?:(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_])|(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_]))[\\w.+-]+@[\\w-]+(?:\\.[\\w-]+)*(?:(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_])|(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_]))",
      "flags": "m"
    },
    "OBFUSCATED_CONTACT": {
      "re": "(?:(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_])|(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_]))[\\w.+-]{2,}\\s*(?:\\[at\\]|\\(at\\)|\\{at\\}|\\s+at\\s+)\\s*[\\w-]+(?:\\s*(?:\\[dot\\]|\\(dot\\)|\\{dot\\}|\\s+dot\\s+)\\s*[\\w-]+)+",
      "flags": "i"
    },
    "IMPERATIVE": {
      "re": "(?:(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_])|(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_]))(send|email|e-?mail|forward|post|transmit|upload|share|reveal|disclose|print|output|report|submit|paste|copy|export|dump|steal|exfiltrate|attain|obtain|retrieve|visit|open|click|navigate|install|run|execute|eval|add|append|include|use|set|configure|update|change|override|replace|ignore|disregard|skip|bypass|disable|turn\\s+off|call|invoke|request|отправь|перешли|отправьте|сообщи|покажи|выведи|раскрой|приложи|скопируй|выгрузи|загрузи|установи|запусти|выполни|добавь|используй|установи|настрой|измени|замени|проигнорируй|пропусти|отключи)(?:(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_])|(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_]))",
      "flags": "i"
    },
    "CREDENTIAL_REF": {
      "re": "(?:(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_])|(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_]))(api[\\s_-]?key|secret|token|credential|password|private[\\s_-]?key|session|cookie|auth|seed|mnemonic|ключ|пароль|токен|секрет)\\w*",
      "flags": "i"
    }
  },
  "sets": {
    "injectionKinds": [
      "assistant_turn_smuggle",
      "conceal_from_user",
      "conceal_from_user_ru",
      "disregard_context",
      "exfiltrate_network",
      "exfiltrate_secrets",
      "forget_instructions",
      "ignore_previous",
      "injection_in_data_field",
      "prompt_injection",
      "role_block_smuggle",
      "role_override",
      "special_token_smuggle"
    ],
    "dangerousCommands": [
      "aws_key_shape",
      "base64_exfiltration",
      "destructive_command",
      "exfiltration_instruction",
      "hidden_html",
      "live_credential_shape",
      "metadata_endpoint",
      "mixed_script_word",
      "obfuscated_exec",
      "private_key_material",
      "remote_exec_pipe",
      "remote_exec_pipe_line",
      "zero_width_smuggle"
    ],
    "criticalKinds": [
      "aws_key_shape",
      "exfiltrate_network",
      "exfiltrate_secrets",
      "exfiltration_instruction",
      "injection_in_data_field",
      "live_credential_shape",
      "mixed_script_word",
      "obfuscated_exec",
      "private_key_material",
      "remote_exec_pipe",
      "remote_exec_pipe_line"
    ],
    "trustworthyKeys": [
      "answer",
      "body",
      "content",
      "data",
      "message",
      "output",
      "result",
      "text",
      "value"
    ],
    "ssrfHosts": [
      "0.0.0.0",
      "10.0.0.1",
      "127.0.0.1",
      "::1",
      "[::1]",
      "[::]",
      "localhost"
    ],
    "metadataHosts": [
      "0",
      "100.100.100.200",
      "169.254.169.254",
      "metadata.goog",
      "metadata.google.internal"
    ]
  },
  "scoring": {
    "severityWeight": {
      "critical": 40.0,
      "high": 15.0,
      "medium": 5.0,
      "low": 1.0
    },
    "violationWeight": 8.0,
    "maxString": 200000,
    "maxDepth": 12,
    "maxItems": 10000,
    "walkListLimit": 500,
    "itemSchemaLimit": 1000,
    "invariantListLimit": 200
  },
  "hardViolationRules": [
    "type",
    "required",
    "null",
    "depth",
    "empty",
    "size",
    "minimum",
    "maximum"
  ],
  "provenance": {
    "devKey": "attest-dev-key-do-not-use-in-production",
    "algorithm": "hmac-sha256"
  },
  "pricing": {
    "freeDaily": 20,
    "plans": {
      "free": {
        "price": "0",
        "unit": "проверок в сутки",
        "what": "полная проверка, без ограничений по размеру артефакта"
      },
      "per_call": {
        "price": "0.005",
        "currency": "USDC",
        "network": "base",
        "what": "проверка сверх бесплатного тарифа, оплата за вызов по x402"
      },
      "subscription": {
        "price": "9",
        "currency": "USDC",
        "unit": "в месяц",
        "what": "снимает лимит, подходит конвейеру в CI"
      }
    }
  }
};
