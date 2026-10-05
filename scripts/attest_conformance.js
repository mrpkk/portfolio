/* Node-сторона проверки соответствия demos/attest ↔ mrpkk/attest.
 *
 * Читает JSON из stdin и отвечает в двух режимах:
 *   {"cases":  [ {name, artifact, schema}, ... ]} -> {"results": [ {verdict, trust_score, ...}, ... ]}
 *   {"verify": [ {record, signature, algorithm}, ... ]} -> {"ok": [true, ...]}
 *
 * Вызывается из scripts/attest_conformance.py, руками не запускается.
 */

'use strict';

const path = require('path');

const DEMO = path.join(__dirname, '..', 'demos', 'attest');
require(path.join(DEMO, 'rules.js'));
const engine = require(path.join(DEMO, 'engine.js'));

let raw = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (chunk) => (raw += chunk));
process.stdin.on('end', async () => {
  const input = JSON.parse(raw);

  if (Array.isArray(input.verify)) {
    const ok = [];
    for (const att of input.verify) {
      ok.push(await engine.verifySignature(att, {}));
    }
    process.stdout.write(JSON.stringify({ ok }));
    return;
  }

  const results = [];
  for (const c of input.cases || []) {
    // artifact_raw сохраняет разницу int/float при передаче JSON (4 против 4.0)
    const artifact = c.artifact_raw !== undefined ? engine.parseJSON(c.artifact_raw) : c.artifact;
    const r = await engine.verify(artifact, c.schema, 'conformance', {});
    results.push({
      name: c.name,
      verdict: r.verdict,
      trust_score: r.trust_score,
      reason: r.reason,
      violations: r.violations,
      signals: r.signals,
      attestation: r.attestation,
      // запись с float-обёртками (для проверки подписи) и её plain-вид (для сравнения)
      record_wrapped: r.attestation.record,
      record_plain: engine.plainify(r.attestation.record),
    });
  }
  process.stdout.write(JSON.stringify({ results }));
});