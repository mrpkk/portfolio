/* attest · JS-порт движка verdicts, 1:1 к mrpkk/attest.
 *
 * Логика (обход дерева, структурный канал, подсчёт доверия, вердикт, HMAC)
 * написана здесь один раз; таблица правил приходит из rules.js, который
 * генерируется из Python-исходников сервиса. Расхождение ловит
 * scripts/attest_conformance.py — он гоняет одни и те же фикстуры через
 * python -m attest и через этот файл и требует полного совпадения.
 *
 * Публичный API: window.attestEngine.verify(artifact, schema, source, opts)
 */

(function (global) {
  'use strict';

  var R = global.ATTEST_RULES;

  var sigRE = R.signatures.map(function (s) {
    return { name: s.name, re: new RegExp(s.re, s.flags + 'u') };
  });

  function helper(name) {
    var h = R.helpers[name];
    return new RegExp(h.re, h.flags + 'u');
  }

  // глобальная копия для проходов findall/finditer (lastIndex не должен течь)
  function globalOf(rx) {
    return new RegExp(rx.source, rx.flags + 'g');
  }

  var RE_BASE64 = helper('BASE64_BLOB');
  var RE_URL = helper('URL');
  var RE_BARE_IP = helper('BARE_IP');
  var RE_HIDDEN = helper('HIDDEN_TEXT');
  var RE_ZERO_WIDTH = helper('ZERO_WIDTH');
  var RE_CYRILLIC = helper('CYRILLIC');
  var RE_LATIN = helper('LATIN');
  var RE_EMAIL = helper('EMAIL');
  var RE_OBF_CONTACT = helper('OBFUSCATED_CONTACT');
  var RE_IMPERATIVE = helper('IMPERATIVE');
  var RE_CREDENTIAL = helper('CREDENTIAL_REF');

  var SEVERITY = R.severity;
  var INJECTION_KINDS = new Set(R.sets.injectionKinds);
  var DANGEROUS = new Set(R.sets.dangerousCommands);
  var CRITICAL_KINDS = new Set(R.sets.criticalKinds);
  var TRUSTWORTHY = new Set(R.sets.trustworthyKeys);
  var SSRF_HOSTS = new Set(R.sets.ssrfHosts);
  var METADATA_HOSTS = new Set(R.sets.metadataHosts);
  var HARD_RULES = new Set(R.hardViolationRules);
  var SC = R.scoring;

  /* ---------------------------------------------------------------- poison */

  function scanText(text, where) {
    var norm = text.normalize('NFKC');
    var out = [];

    for (var i = 0; i < sigRE.length; i++) {
      var m = sigRE[i].re.exec(norm);
      if (m) {
        out.push(sig(sigRE[i].name, SEVERITY[sigRE[i].name] || 'medium', where, m[0]));
      }
    }

    if (RE_ZERO_WIDTH.test(text)) out.push(sig('zero_width_smuggle', 'high', where, 'невидимые unicode-символы'));
    if (RE_HIDDEN.test(text)) out.push(sig('hidden_html', 'high', where, 'скрытый текст в разметке'));

    var words = norm.match(/\S+/gu) || [];
    for (var w = 0; w < words.length; w++) {
      var stripped = words[w].replace(/^[.,!?;:'"()[\]{}]+/, '').replace(/[.,!?;:'"()[\]{}]+$/, '');
      if (Array.from(stripped).length >= 4 && RE_CYRILLIC.test(stripped) && RE_LATIN.test(stripped)) {
        out.push(sig('mixed_script_word', 'high', where, '«' + stripped.slice(0, 40) + '» — смешанные алфавиты'));
        break;
      }
    }

    var bm;
    var base64Re = globalOf(RE_BASE64);
    while ((bm = base64Re.exec(norm)) !== null) {
      if (norm.slice(Math.max(0, bm.index - 64), bm.index).toLowerCase().indexOf('base64,') !== -1) continue;
      var decoded = decodeB64(bm[0]);
      if (decoded === null) continue;
      if (decoded.length < 8 || !isPrintable(decoded)) continue;
      var hit = null;
      for (var k = 0; k < sigRE.length; k++) {
        if (sigRE[k].re.test(decoded)) { hit = sigRE[k].name; break; }
      }
      if (hit) {
        out.push(sig('base64_' + hit, 'critical', where, 'декодировано: ' + decoded.slice(0, 120)));
      } else if (structuralExfiltration(decoded)) {
        out.push(sig('base64_exfiltration', 'critical', where, 'декодировано: ' + decoded.slice(0, 120)));
      } else {
        out.push(sig('base64_blob', 'low', where, 'base64-блок ' + bm[0].length + ' символов'));
      }
    }

    return out;
  }

  function sig(kind, severity, where, evidence) {
    return { kind: kind, severity: severity, where: where, evidence: String(evidence).slice(0, 200) };
  }

  function decodeB64(blob) {
    try {
      var padded = blob + '='.repeat((4 - (blob.length % 4)) % 4);
      var bin = global.atob(padded);
      var bytes = new Uint8Array(bin.length);
      for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
      return new TextDecoder('utf-8').decode(bytes);
    } catch (e) {
      return null;
    }
  }

  function isPrintable(text) {
    return !/[\p{Cc}\p{Cf}\p{Cs}\p{Co}]/u.test(text);
  }

  function walk(node, path, sink, depth) {
    if (depth > 40) return;
    if (node !== null && typeof node === 'object' && !Array.isArray(node)) {
      Object.keys(node).forEach(function (k) { walk(node[k], path + '.' + k, sink, depth + 1); });
    } else if (Array.isArray(node)) {
      for (var i = 0; i < Math.min(node.length, SC.walkListLimit); i++) {
        walk(node[i], path + '[' + i + ']', sink, depth + 1);
      }
    } else if (typeof node === 'string') {
      sink.push([path, node]);
    }
  }

  function keyOf(path) {
    var parts = path.split('.');
    var last = parts[parts.length - 1];
    return last.split('[')[0].toLowerCase();
  }

  var PROMOTED = new Set([
    'ignore_previous', 'disregard_context', 'forget_instructions', 'prompt_injection',
    'role_override', 'conceal_from_user', 'conceal_from_user_ru', 'exfiltrate_secrets'
  ]);

  function structuralExfiltration(text) {
    if (!RE_IMPERATIVE.test(text) || !RE_CREDENTIAL.test(text)) return null;
    var m = RE_EMAIL.exec(text) || RE_URL.exec(text) || RE_OBF_CONTACT.exec(text);
    return m ? m[0] : null;
  }

  function hostOf(url) {
    var m = /^https?:\/\/([^/:?#]+)/i.exec(url);
    return m ? m[1].toLowerCase() : '';
  }

  function hostClass(host) {
    if (host === '') return '';
    var hits = function (set) {
      return set.has(host) || [...set].some(function (h) { return host.endsWith('.' + h); });
    };
    if (hits(METADATA_HOSTS)) return 'metadata_endpoint';
    if (hits(SSRF_HOSTS)) return 'ssrf_target';
    return '';
  }

  function dedupe(signals) {
    var seen = new Set();
    var out = [];
    signals.forEach(function (s) {
      var key = (s.kind === 'ssrf_target' || s.kind === 'metadata_endpoint')
        ? s.kind + '|' + s.where
        : s.kind + '|' + s.where + '|' + s.evidence;
      if (seen.has(key)) return;
      seen.add(key);
      out.push(s);
    });
    return out;
  }

  function scanPoison(artifact) {
    if (typeof artifact === 'string') return dedupe(scanText(artifact, '$'));
    if (artifact === null || typeof artifact !== 'object') return [];

    var leaves = [];
    walk(artifact, '$', leaves, 0);
    var signals = [];

    leaves.forEach(function (pair) {
      var path = pair[0];
      var text = pair[1];
      var key = keyOf(path);
      scanText(text, path).forEach(function (s) {
        if (PROMOTED.has(s.kind) && !TRUSTWORTHY.has(key)) {
          s.severity = 'critical';
          s.kind = 'injection_in_data_field:' + key;
        }
        signals.push(s);
      });
      if (RE_IMPERATIVE.test(text)) {
        var target = structuralExfiltration(text);
        if (target) {
          signals.push(sig('exfiltration_instruction:' + key, 'critical', path,
            'императив + упоминание секрета + адрес ' + target));
        }
      }
    });

    var flat = JSON.stringify(artifact);
    var um;
    var urlRe = globalOf(RE_URL);
    while ((um = urlRe.exec(flat)) !== null) {
      var kind = hostClass(hostOf(um[0]));
      if (kind) signals.push(sig(kind, kind === 'metadata_endpoint' ? 'critical' : 'high', '$', um[0].slice(0, 120)));
    }

    var ipm;
    var ipRe = globalOf(RE_BARE_IP);
    while ((ipm = ipRe.exec(flat)) !== null) {
      var host = ipm[1];
      var octets = host.split('.').map(Number);
      if (octets.length !== 4 || octets.some(function (o) { return o > 255; })) continue;
      if (octets.join('.') !== host) continue;
      if (host === '1.0.0.0' || host === '0.0.0.0') continue;
      var ipKind = hostClass(host);
      if (!ipKind && host.startsWith('127.')) ipKind = 'ssrf_target';
      if (!ipKind && host.startsWith('10.')) ipKind = 'ssrf_target';
      if (ipKind) {
        signals.push(sig(ipKind, ipKind === 'metadata_endpoint' ? 'critical' : 'high', '$', ipm[0].slice(0, 120)));
      }
    }

    return dedupe(signals);
  }

  /* ---------------------------------------------------------------- schema */

  function violation(path, rule, detail) {
    return { path: path, rule: rule, detail: detail };
  }

  // Python type(x).__name__ — в тексте нарушений контракта это видно пользователю,
  // поэтому названия совпадают с серверными, а не с JS-именами.
  function typeName(value) {
    if (value === null) return 'NoneType';
    if (Array.isArray(value)) return 'list';
    if (isPyFloat(value)) return 'float';
    if (typeof value === 'boolean') return 'bool';
    if (typeof value === 'number') return Number.isInteger(value) ? 'int' : 'float';
    if (typeof value === 'string') return 'str';
    return 'dict';
  }

  function typeOk(value, expected) {
    switch (expected) {
      case 'string': return typeof value === 'string';
      case 'number': return typeof value === 'number' && Number.isFinite(value);
      case 'integer': return typeof value === 'number' && Number.isInteger(value) && !isPyFloat(value);
      case 'boolean': return typeof value === 'boolean';
      case 'null': return value === null;
      case 'array': return Array.isArray(value);
      case 'object': return value !== null && typeof value === 'object' && !Array.isArray(value);
      default: return true;
    }
  }

  function validate(value, sch, path, depth, out) {
    if (depth > SC.maxDepth) {
      out.push(violation(path, 'depth', 'превышена глубина ' + SC.maxDepth));
      return;
    }
    var expected = sch && sch.type;
    if (typeof expected === 'string' && !typeOk(value, expected)) {
      out.push(violation(path, 'type', 'ожидался ' + expected + ', получен ' + typeName(value)));
      return;
    }
    if (Array.isArray(expected) && !expected.some(function (t) { return typeOk(value, t); })) {
      out.push(violation(path, 'type', 'ожидался один из ' + JSON.stringify(expected) + ', получен ' + typeName(value)));
      return;
    }

    if (typeof value === 'string') {
      if (value.length > SC.maxString) {
        out.push(violation(path, 'size', 'строка ' + value.length + ' > ' + SC.maxString));
      }
      if (sch && sch.pattern) {
        try {
          if (!new RegExp(sch.pattern, 'u').test(value)) {
            out.push(violation(path, 'pattern', 'не совпало с /' + sch.pattern + '/'));
          }
        } catch (e) { /* невалидный pattern — как и в Python, пропускаем */ }
      }
      if (sch && Array.isArray(sch.enum) && sch.enum.indexOf(value) === -1) {
        out.push(violation(path, 'enum', 'значение не входит в enum[' + sch.enum.length + ']'));
      }
      return;
    }

    if (typeof value === 'number' && Number.isFinite(value)) {
      if (sch && 'minimum' in sch && value < sch.minimum) {
        out.push(violation(path, 'minimum', value + ' < ' + sch.minimum));
      }
      if (sch && 'maximum' in sch && value > sch.maximum) {
        out.push(violation(path, 'maximum', value + ' > ' + sch.maximum));
      }
      return;
    }

    if (Array.isArray(value)) {
      if (value.length > SC.maxItems) {
        out.push(violation(path, 'size', 'элементов ' + value.length + ' > ' + SC.maxItems));
      }
      if (sch && sch.items && typeof sch.items === 'object') {
        for (var i = 0; i < Math.min(value.length, SC.itemSchemaLimit); i++) {
          validate(value[i], sch.items, path + '[' + i + ']', depth + 1, out);
        }
      }
      return;
    }

    if (value !== null && typeof value === 'object') {
      var props = (sch && sch.properties) || {};
      var required = (sch && sch.required) || [];
      var additional = !sch || sch.additionalProperties === undefined ? true : sch.additionalProperties;

      required.forEach(function (k) {
        if (!Object.prototype.hasOwnProperty.call(value, k)) {
          out.push(violation(path + '.' + k, 'required', 'обязательное поле отсутствует'));
        }
      });
      Object.keys(props).forEach(function (k) {
        if (Object.prototype.hasOwnProperty.call(value, k)) {
          validate(value[k], props[k], path + '.' + k, depth + 1, out);
        }
      });
      if (additional === false) {
        Object.keys(value).forEach(function (k) {
          if (!Object.prototype.hasOwnProperty.call(props, k)) {
            out.push(violation(path + '.' + k, 'additionalProperties', 'лишнее поле'));
          }
        });
      }
    }
  }

  function basicInvariants(artifact, path, depth, out) {
    if (depth > SC.maxDepth) {
      out.push(violation(path, 'depth', 'превышена глубина ' + SC.maxDepth));
      return;
    }
    if (typeof artifact === 'string') {
      if (artifact.length > SC.maxString) out.push(violation(path, 'size', 'строка ' + artifact.length + ' > ' + SC.maxString));
    } else if (Array.isArray(artifact)) {
      if (artifact.length > SC.maxItems) out.push(violation(path, 'size', 'элементов ' + artifact.length + ' > ' + SC.maxItems));
      for (var i = 0; i < Math.min(artifact.length, SC.invariantListLimit); i++) {
        basicInvariants(artifact[i], path + '[' + i + ']', depth + 1, out);
      }
    } else if (artifact !== null && typeof artifact === 'object') {
      Object.keys(artifact).forEach(function (k) {
        basicInvariants(artifact[k], path + '.' + k, depth + 1, out);
      });
    }
  }

  function validateSchema(artifact, schema) {
    var out = [];
    if (schema && typeof schema === 'object' && Object.keys(schema).length) {
      validate(artifact, schema, '$', 0, out);
    } else {
      basicInvariants(artifact, '$', 0, out);
    }

    if (artifact === null) {
      out.push(violation('$', 'null', 'артефакт пуст — агент получит ничего'));
    } else if (typeof artifact === 'string' && !artifact.trim()) {
      out.push(violation('$', 'empty', 'пустая строка'));
    } else if (typeof artifact === 'object' && Object.keys(artifact).length === 0) {
      out.push(violation('$', 'empty', 'пустая структура'));
    }
    return out;
  }

  /* --------------------------------------------------------------- scoring */

  function score(violations, signals) {
    var penalty = violations.length * SC.violationWeight;
    signals.forEach(function (s) {
      penalty += SC.severityWeight[s.severity] === undefined ? 5.0 : SC.severityWeight[s.severity];
    });
    return Math.max(0, 100 - penalty);
  }

  function decide(violations, signals, trust) {
    var critical = signals.filter(function (s) {
      return CRITICAL_KINDS.has(baseKind(s.kind)) || DANGEROUS.has(baseKind(s.kind)) || s.severity === 'critical';
    });
    if (critical.length) return ['reject', 'критичный сигнал: ' + critical[0].kind + ' @ ' + critical[0].where];
    if (!signals.length && !violations.length) return ['accept', 'схема в порядке, признаков отравления нет'];
    if (violations.length) {
      var hard = violations.filter(function (v) { return HARD_RULES.has(v.rule); });
      if (hard.length) return ['reject', 'нарушение контракта: ' + hard[0].rule + ' @ ' + hard[0].path];
    }
    var signatureAttack = signals.filter(function (s) { return INJECTION_KINDS.has(baseKind(s.kind)); });
    if (signatureAttack.length) {
      return ['reject', 'сигнатурная инъекция: ' + signatureAttack[0].kind + ' @ ' + signatureAttack[0].where];
    }
    var strong = signals.filter(function (s) { return s.severity === 'high'; });
    if (strong.length >= 2) {
      return ['reject', 'несколько независимых сигналов: ' + strong.slice(0, 3).map(function (s) { return s.kind; }).join(', ')];
    }
    if (trust < 60) return ['reject', 'доверие слишком низкое (' + trust.toFixed(0) + '/100)'];
    if (trust < 90) return ['review', 'есть замечания, требуется взгляд человека (' + trust.toFixed(0) + '/100)'];
    return ['accept', 'незначительные замечания (' + trust.toFixed(0) + '/100)'];
  }

  // "injection_in_data_field:description" -> "injection_in_data_field"
  function baseKind(kind) {
    return kind.split(':')[0];
  }

  /* ------------------------------------------------------------ provenance */

  /* --- числа: Python различает int и float, JSON — нет -----------------------
   *
   * json.dumps(85.0) -> "85.0", а JSON.stringify(85) -> "85". Из-за этой
   * разницы подпись и sha256(content) в браузере не совпали бы с серверными,
   * поэтому float помечается обёрткой {__pyfloat: n}, а парсер ниже
   * воспроизводит это правило прямо из текста артефакта.
   */
  function pyf(n) { return { __pyfloat: n }; }
  function isPyFloat(v) { return v !== null && typeof v === 'object' && typeof v.__pyfloat === 'number'; }

  function pyNum(n) {
    // repr(float) в Python: целое значение всегда с дробной частью
    return Number.isInteger(n) ? n.toFixed(1) : String(n);
  }

  // Python json.dumps(sort_keys=True, separators=(",",":"), ensure_ascii=False)
  function canonical(value) {
    if (value === null) return 'null';
    if (isPyFloat(value)) return pyNum(value.__pyfloat);
    if (typeof value === 'boolean') return value ? 'true' : 'false';
    if (typeof value === 'number') return Number.isInteger(value) ? String(value) : String(value);
    if (typeof value === 'string') return JSON.stringify(value);
    if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
    var keys = Object.keys(value).sort();
    return '{' + keys.map(function (k) { return JSON.stringify(k) + ':' + canonical(value[k]); }).join(',') + '}';
  }

  /* --- парсер JSON, который помнит float ------------------------------------
   *
   * JSON.parse теряет разницу 4 и 4.0, а Python её сохраняет. Разбор свой
   * (~60 строк), чтобы sha256(content_hash) совпадал с серверным байт в байт.
   */
  function pyJSONParse(text) {
    var i = 0;
    function ws() { while (i < text.length && ' \t\n\r'.indexOf(text[i]) !== -1) i++; }
    function fail(msg) { throw new SyntaxError(msg + ' (позиция ' + i + ')'); }

    function value() {
      ws();
      var ch = text[i];
      if (ch === '{') return object();
      if (ch === '[') return array();
      if (ch === '"') return string();
      if (ch === '-' || (ch >= '0' && ch <= '9')) return number();
      if (text.startsWith('true', i)) { i += 4; return true; }
      if (text.startsWith('false', i)) { i += 5; return false; }
      if (text.startsWith('null', i)) { i += 4; return null; }
      fail('неожиданный символ ' + JSON.stringify(ch || 'конец ввода'));
    }

    function object() {
      var out = {};
      i++; ws();
      if (text[i] === '}') { i++; return out; }
      for (;;) {
        ws();
        if (text[i] !== '"') fail('ожидался ключ');
        var k = string();
        ws();
        if (text[i] !== ':') fail('ожидалось :');
        i++;
        out[k] = value();
        ws();
        if (text[i] === ',') { i++; continue; }
        if (text[i] === '}') { i++; return out; }
        fail('ожидалась , или }');
      }
    }

    function array() {
      var out = [];
      i++; ws();
      if (text[i] === ']') { i++; return out; }
      for (;;) {
        out.push(value());
        ws();
        if (text[i] === ',') { i++; continue; }
        if (text[i] === ']') { i++; return out; }
        fail('ожидалась , или ]');
      }
    }

    function string() {
      var out = '';
      i++;
      for (;;) {
        var ch = text[i];
        if (ch === undefined) fail('строка не закрыта');
        if (ch === '"') { i++; return out; }
        if (ch === '\\') {
          var esc = text[i + 1];
          i += 2;
          if (esc === 'u') { out += String.fromCharCode(parseInt(text.slice(i, i + 4), 16)); i += 4; continue; }
          out += ({ n: '\n', t: '\t', r: '\r', b: '\b', f: '\f' })[esc] || esc;
          continue;
        }
        out += ch;
        i++;
      }
    }

    function number() {
      var start = i;
      if (text[i] === '-') i++;
      while (i < text.length && text[i] >= '0' && text[i] <= '9') i++;
      var isFloat = false;
      if (text[i] === '.') { isFloat = true; i++; while (i < text.length && text[i] >= '0' && text[i] <= '9') i++; }
      if (text[i] === 'e' || text[i] === 'E') {
        isFloat = true; i++;
        if (text[i] === '+' || text[i] === '-') i++;
        while (i < text.length && text[i] >= '0' && text[i] <= '9') i++;
      }
      var raw2 = text.slice(start, i);
      if (!/^-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?$/.test(raw2)) fail('плохое число ' + raw2);
      var n = Number(raw2);
      return isFloat ? pyf(n) : n;
    }

    var result = value();
    ws();
    if (i !== text.length) fail('лишние символы после значения');
    return result;
  }

  async function sha256Hex(bytes) {
    var digest = await crypto.subtle.digest('SHA-256', bytes);
    return [...new Uint8Array(digest)].map(function (b) { return b.toString(16).padStart(2, '0'); }).join('');
  }

  async function hmacHex(keyText, payloadText) {
    var key = await crypto.subtle.importKey(
      'raw', new TextEncoder().encode(keyText), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']
    );
    var mac = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(payloadText));
    return [...new Uint8Array(mac)].map(function (b) { return b.toString(16).padStart(2, '0'); }).join('');
  }

  function round3(n) {
    return Math.round(n * 1000) / 1000;
  }

  async function verify(artifact, schema, source, opts) {
    opts = opts || {};
    var violations = validateSchema(artifact, schema);
    var signals = scanPoison(artifact);
    var trust = score(violations, signals);
    var dec = decide(violations, signals, trust);
    var verdict = dec[0];
    var reason = dec[1];

    var contentHash = 'sha256:' + await sha256Hex(new TextEncoder().encode(canonical(artifact)));
    var record = {
      attestation_id: global.crypto.randomUUID ? global.crypto.randomUUID() : 'demo-' + Date.now(),
      source: source || 'unknown',
      verified_at: pyf(Date.now() / 1000),
      content_hash: contentHash,
      verdict: verdict,
      trust_score: pyf(round3(trust)),
      violations: violations,
      signals: signals
    };

    var keyText = opts.key || R.provenance.devKey;
    var signature = opts.sign === false
      ? 'unsigned'
      : 'hmac-sha256:' + await hmacHex(keyText, canonical(record));

    return {
      verdict: verdict,
      trust_score: round3(trust),
      reason: reason,
      violations: violations,
      signals: signals,
      attestation: {
        record: record,
        signature: signature,
        algorithm: opts.sign === false ? 'none' : R.provenance.algorithm
      }
    };
  }

  // запись с float-обёртками -> обычные значения (для показа и для JSON)
  function plainify(value) {
    if (isPyFloat(value)) return value.__pyfloat;
    if (Array.isArray(value)) return value.map(plainify);
    if (value !== null && typeof value === 'object') {
      var out = {};
      Object.keys(value).forEach(function (k) { out[k] = plainify(value[k]); });
      return out;
    }
    return value;
  }

  /* Проверка подписи.
   *
   * Запись, пришедшая из JSON, теряет тип float (100.0 -> 100), а канонизация
   * Python их различает. В ProvenanceRecord ровно два дробных поля, поэтому
   * они приводятся к float явно — иначе подпись, выданная сервером, не прошла
   * бы проверку в браузере.
   */
  async function verifySignature(attestation, opts) {
    opts = opts || {};
    var keyText = opts.key || R.provenance.devKey;
    var rec = plainify(attestation.record);
    rec.verified_at = pyf(Number(rec.verified_at));
    rec.trust_score = pyf(Number(rec.trust_score));
    var expected = 'hmac-sha256:' + await hmacHex(keyText, canonical(rec));
    return expected === attestation.signature;
  }

  global.attestEngine = {
    verify: verify,
    verifySignature: verifySignature,
    canonical: canonical,
    parseJSON: pyJSONParse,
    plainify: plainify,
    rules: R
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = global.attestEngine;
  }
})(typeof window !== 'undefined' ? window : globalThis);