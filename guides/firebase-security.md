# Firebase Security Guide

## When to use

Load during audits of Firebase Auth, Firestore, Realtime Database, or Storage.

**Related rules:** TG-DB-003, TG-AUTH-002, TG-AUTH-003, TG-SEC-002

## Key distinction

| SDK | Where | Purpose |
|-----|-------|---------|
| **Firebase client SDK** | Browser/mobile | User-facing ops constrained by Security Rules |
| **Firebase Admin SDK** | Server only | Privileged operations — never in frontend |

## Checklist

- [ ] Admin SDK credentials server-only (TG-DB-003)
- [ ] Firestore/RTDB Security Rules deployed and tested
- [ ] Storage rules restrict paths by `request.auth.uid`
- [ ] Client rules do not trust client-supplied ownership fields alone
- [ ] Custom claims used for roles verified server-side for sensitive ops
- [ ] Emulator tests for rule changes

## Client SDK (safe with rules)

```javascript
import { initializeApp } from 'firebase/app';
import { getFirestore, doc, getDoc } from 'firebase/firestore';

const app = initializeApp(firebaseConfig); // public config is OK
const db = getFirestore(app);
```

## Firestore rules example

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    match /orders/{orderId} {
      allow read: if request.auth != null
        && resource.data.ownerId == request.auth.uid;
    }
  }
}
```

## Admin SDK (server only)

```javascript
// functions or server/index.js — never in React src/
import admin from 'firebase-admin';
admin.initializeApp({ credential: admin.credential.cert(serviceAccount) });
```

Never commit service account JSON; use environment or secret manager (TG-SEC-001, TG-SEC-003).

## Manual rules review checklist

1. Default-deny: are unmatched paths blocked?
2. Can users read/write other users' documents by guessing IDs?
3. Are admin collections inaccessible to normal users?
4. Do Storage paths include user ID validation?
5. Run emulator tests for allow/deny cases

## Auth token validation

For custom backends verifying Firebase ID tokens, use Admin SDK `verifyIdToken` — do not decode JWT without signature verification.

## Related documentation

- [rules/TG-DB-003-frontend-admin-sdk.md](../rules/TG-DB-003-frontend-admin-sdk.md)
- [rules/TG-AUTH-003-missing-object-authorization.md](../rules/TG-AUTH-003-missing-object-authorization.md)
- [skills/torusguard/references/frontend-no-db.md](../skills/torusguard/references/frontend-no-db.md)
