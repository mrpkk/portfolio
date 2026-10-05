'use strict';

/*
 * Live Attest demo — real client-side Web Crypto attestation.
 * No backend, no mocks: ECDSA P-256 keypair, canonical statement,
 * SHA-256 digest, signature, verification, and a negative control.
 */

const ALG = { name: 'ECDSA', namedCurve: 'P-256' };
const SIGN_ALG = { name: 'ECDSA', hash: 'SHA-256' };

const $ = (id) => document.getElementById(id);

function setStep(n, state, note) {
    const li = document.querySelector(`.steps li[data-i="${n}"]`);
    if (!li) return;
    li.classList.remove('run', 'ok', 'bad');
    if (state) li.classList.add(state);
    li.querySelector('.s').textContent = note || '—';
}

function toHex(buf) {
    const b = new Uint8Array(buf);
    let out = '';
    for (let i = 0; i < b.length; i++) out += b[i].toString(16).padStart(2, '0');
    return out;
}

function canonical(obj) {
    return JSON.stringify(obj, Object.keys(obj).sort());
}

async function showOrigin() {
    $('origin').textContent = window.location.origin;
    const secure = window.isSecureContext;
    const el = $('secure');
    el.textContent = secure ? 'yes (crypto.subtle available)' : 'NO — crypto.subtle blocked';
    el.classList.add(secure ? 'yes' : 'no');
    if (!secure) {
        $('run').disabled = true;
        const v = $('verdict');
        v.className = 'verdict fail';
        v.textContent =
            'Insecure context: crypto.subtle is unavailable.\n' +
            'This page must be served over HTTPS (it is, via GitHub Pages).';
    }
}

async function runAttestation() {
    const btn = $('run');
    btn.disabled = true;
    for (let i = 1; i <= 6; i++) setStep(i, null, '—');
    $('copy').disabled = true;
    $('verdict').className = 'verdict idle';
    $('verdict').textContent = 'Running…';

    try {
        // 1 — non-extractable key pair
        setStep(1, 'run', '…');
        const kp = await crypto.subtle.generateKey(ALG, false, ['sign', 'verify']);
        const spki = await crypto.subtle.exportKey('spki', kp.publicKey);
        setStep(1, 'ok', kp.privateKey.extractable ? 'EXTRACTABLE (bad)' : 'extractable=false');

        // 2 — attestation statement + canonical form
        setStep(2, 'run', '…');
        const statement = {
            version: 'bhaga-attest/1',
            subject: 'browser:' + navigator.userAgent.slice(0, 120),
            origin: window.location.origin,
            issued_at: new Date().toISOString(),
            nonce: toHex(crypto.getRandomValues(new Uint8Array(16))),
            alg: 'ECDSA-P256-SHA256',
        };
        const canonicalStr = canonical(statement);
        $('stmt').textContent = JSON.stringify(statement, null, 2);
        setStep(2, 'ok', canonicalStr.length + ' bytes canonical');

        // 3 — digest
        setStep(3, 'run', '…');
        const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(canonicalStr));
        const digestHex = toHex(digest);
        setStep(3, 'ok', digestHex.slice(0, 16) + '…');

        // 4 — sign
        setStep(4, 'run', '…');
        const signature = await crypto.subtle.sign(SIGN_ALG, kp.privateKey, digest);
        const sigHex = toHex(signature);
        setStep(4, 'ok', signature.byteLength + ' bytes DER');

        // 5 — verify
        setStep(5, 'run', '…');
        const good = await crypto.subtle.verify(SIGN_ALG, kp.publicKey, signature, digest);
        setStep(5, good ? 'ok' : 'bad', good ? 'PASS' : 'FAIL');

        // 6 — negative control
        setStep(6, 'run', '…');
        const tampered = { ...statement, origin: statement.origin + '/tampered' };
        const tamperedDigest = await crypto.subtle.digest(
            'SHA-256',
            new TextEncoder().encode(canonical(tampered))
        );
        const stillValid = await crypto.subtle.verify(SIGN_ALG, kp.publicKey, signature, tamperedDigest);
        setStep(6, stillValid ? 'bad' : 'ok', stillValid ? 'ACCEPTED (bad)' : 'REJECTED');

        // material
        $('m-alg').textContent = ALG.name + ' ' + ALG.namedCurve;
        $('m-ext').textContent = String(kp.privateKey.extractable);
        $('m-spki').textContent = toHex(await crypto.subtle.digest('SHA-256', spki));
        $('m-digest').textContent = digestHex;
        $('m-sig').textContent = sigHex;
        $('m-siglen').textContent = signature.byteLength + ' bytes';

        const v = $('verdict');
        if (good && !stillValid) {
            v.className = 'verdict pass';
            v.textContent =
                'PASS  signature verified against public key\n' +
                'PASS  tampered statement rejected by the same verifier\n' +
                '\nThe attestation is cryptographically binding: any change to the\n' +
                'statement invalidates the signature.';
        } else if (good && stillValid) {
            v.className = 'verdict fail';
            v.textContent =
                'FAIL  a tampered statement was accepted.\n' +
                'The signature is not bound to the statement content.';
        } else {
            v.className = 'verdict fail';
            v.textContent = 'FAIL  the genuine signature did not verify.';
        }

        $('copy').disabled = false;
        $('copy').dataset.json = JSON.stringify(statement, null, 2);
    } catch (err) {
        const v = $('verdict');
        v.className = 'verdict fail';
        v.textContent = 'ERROR  ' + (err && err.message ? err.message : String(err));
        for (let i = 1; i <= 6; i++) {
            const li = document.querySelector(`.steps li[data-i="${i}"]`);
            if (li.classList.contains('run')) setStep(i, 'bad', 'error');
        }
    } finally {
        btn.disabled = false;
        btn.textContent = 'Run again';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    showOrigin();
    $('run').addEventListener('click', runAttestation);
    $('copy').addEventListener('click', async () => {
        const btn = $('copy');
        try {
            await navigator.clipboard.writeText(btn.dataset.json || '');
            btn.textContent = 'Copied';
        } catch (e) {
            btn.textContent = 'Copy blocked by browser';
        }
        setTimeout(() => (btn.textContent = 'Copy JSON'), 1600);
    });
});