# 🛡️ TorusGuard Living Security Report

> **Notice:** This document is the living, single-source-of-truth ledger for security findings,
> candidate patches, and verified closures across this repository. Updated automatically by
> TorusGuard CLI commands (`audit`, `harden`, `apply`, `recheck`) and AI chat workflows.

---

## 📊 Security Posture Overview

- **Health Score:** `100/100` — **🟢 HARDENED & SECURE**
- **Last Updated:** `2026-09-12 22:03:19 IST`
- **Total Tracked Findings:** `40`
- **Status Breakdown:** `🔴 0 Open` · `🟠 0 Verified` · `🟡 0 Candidate` · `🔵 0 Applied` · `🟢 40 Resolved` · `❌ 0 Regressed` · `⚪ 0 Suppressed`

| Severity | Total | Open / Regressed | Resolved | Candidate / Applied |
| :--- | :---: | :---: | :---: | :---: |
| **Critical** | 24 | 0 | 24 | 0 |
| **High** | 9 | 0 | 9 | 0 |
| **Medium** | 7 | 0 | 7 | 0 |
| **Low** | 0 | 0 | 0 | 0 |

---

## 🔍 Tracked Findings Detail

### [TG-DB-002] Privileged Database Credential in Browser Context
- **Finding ID:** `TG-DB-002-d9bd69df`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 70% (High Confidence)
- **Target:** `demo/playground/vulnerable_nextjs/actions.ts:9`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-DB-002-d9bd69df`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in demo/playground/vulnerable_nextjs/actions.ts. |
| 2026-09-12 22:00:07 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-db-002-9-5f7850 formulated (+1 / -1 lines). |
| 2026-09-12 22:00:15 IST | Patch Applied | `run-20260912-215731-audit` | Candidate patch applied to disk. Pre-apply snapshot saved in run-20260912-215731-audit. |
| 2026-09-12 22:02:27 IST | Resolved | `run-20260912-220227-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-DIFF-001] Accidental Security Check Bypass in Patch Additions
- **Finding ID:** `TG-DIFF-001-7db54483`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 70% (High Confidence)
- **Target:** `skills/torusguard/payload/scripts/rules_sync.py:180`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-DIFF-001-7db54483`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in skills/torusguard/payload/scripts/rules_sync.py. |
| 2026-09-12 21:55:55 IST | Resolved | `run-20260912-215555-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-DIFF-001] Accidental Security Check Bypass in Patch Additions
- **Finding ID:** `TG-DIFF-001-77bc2f9b`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 70% (High Confidence)
- **Target:** `skills/torusguard/payload/scripts/rules_sync.py:157`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-DIFF-001-77bc2f9b`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in skills/torusguard/payload/scripts/rules_sync.py. |
| 2026-09-12 21:55:55 IST | Resolved | `run-20260912-215555-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-DIFF-001] Accidental Security Check Bypass in Patch Additions
- **Finding ID:** `TG-DIFF-001-cb5ae7e9`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 70% (High Confidence)
- **Target:** `skills/torusguard/payload/scripts/rules_sync.py:172`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-DIFF-001-cb5ae7e9`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in skills/torusguard/payload/scripts/rules_sync.py. |
| 2026-09-12 21:55:55 IST | Resolved | `run-20260912-215555-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-DIFF-001] Accidental Security Check Bypass in Patch Additions
- **Finding ID:** `TG-DIFF-001-0e4204af`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 70% (High Confidence)
- **Target:** `skills/torusguard/payload/scripts/rules_sync.py:169`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-DIFF-001-0e4204af`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in skills/torusguard/payload/scripts/rules_sync.py. |
| 2026-09-12 21:55:55 IST | Resolved | `run-20260912-215555-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-DIFF-001] Accidental Security Check Bypass in Patch Additions
- **Finding ID:** `TG-DIFF-001-671d3513`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 70% (High Confidence)
- **Target:** `skills/torusguard/payload/scripts/harden_runner.py:246`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-DIFF-001-671d3513`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in skills/torusguard/payload/scripts/harden_runner.py. |
| 2026-09-12 21:48:13 IST | Resolved | `run-20260912-214813-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-DIFF-001] Accidental Security Check Bypass in Patch Additions
- **Finding ID:** `TG-DIFF-001-b6549484`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 70% (High Confidence)
- **Target:** `skills/torusguard/payload/scripts/harden_runner.py:256`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-DIFF-001-b6549484`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in skills/torusguard/payload/scripts/harden_runner.py. |
| 2026-09-12 21:48:13 IST | Resolved | `run-20260912-214813-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-DIFF-001] Accidental Security Check Bypass in Patch Additions
- **Finding ID:** `TG-DIFF-001-c4cfaa8a`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 70% (High Confidence)
- **Target:** `skills/torusguard/payload/scripts/harden_runner.py:251`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-DIFF-001-c4cfaa8a`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in skills/torusguard/payload/scripts/harden_runner.py. |
| 2026-09-12 21:48:13 IST | Resolved | `run-20260912-214813-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-GQL-004] Unnecessary Production Introspection
- **Finding ID:** `TG-GQL-004-a6ecb0bb`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 55% (Medium Confidence)
- **Target:** `skills/torusguard/payload/scripts/harden_runner.py:365`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-GQL-004-a6ecb0bb`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in skills/torusguard/payload/scripts/harden_runner.py. |
| 2026-09-12 21:48:13 IST | Resolved | `run-20260912-214813-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SEC-001] Hardcoded Secret or API Key in Tracked Source
- **Finding ID:** `TG-SEC-001-c393d596`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 80% (High Confidence)
- **Target:** `examples/vulnerable-react-express/server/index.js:18`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SEC-001-c393d596`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/vulnerable-react-express/server/index.js. |
| 2026-09-12 22:00:07 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-sec-001-18-a3c1e8 formulated (+1 / -1 lines). |
| 2026-09-12 22:00:15 IST | Patch Applied | `run-20260912-215731-audit` | Candidate patch applied to disk. Pre-apply snapshot saved in run-20260912-215731-audit. |
| 2026-09-12 22:02:27 IST | Resolved | `run-20260912-220227-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SEC-001] Hardcoded Secret or API Key in Tracked Source
- **Finding ID:** `TG-SEC-001-bb5e4b77`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 80% (High Confidence)
- **Target:** `examples/vulnerable-react-express/server/index.js:9`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SEC-001-bb5e4b77`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/vulnerable-react-express/server/index.js. |
| 2026-09-12 21:56:47 IST | Patch Formulated | `run-20260912-215555-audit` | Ponytail candidate bundle bnd-tg-sec-001-9-e22e50 formulated (+1 / -1 lines). |
| 2026-09-12 21:59:29 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-sec-001-9-e22e50 formulated (+1 / -1 lines). |
| 2026-09-12 22:00:07 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-sec-001-9-e22e50 formulated (+1 / -1 lines). |
| 2026-09-12 22:00:15 IST | Patch Applied | `run-20260912-215731-audit` | Candidate patch applied to disk. Pre-apply snapshot saved in run-20260912-215731-audit. |
| 2026-09-12 22:02:27 IST | Resolved | `run-20260912-220227-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SEC-002] Public Client Environment Variable Secret Exposure
- **Finding ID:** `TG-SEC-002-d6272a02`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 55% (Medium Confidence)
- **Target:** `demo/playground/vulnerable_nextjs/actions.ts:9`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SEC-002-d6272a02`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 22:01:34 IST | Discovered | `run-20260912-220134-audit` | Initial discovery during static AST audit in demo/playground/vulnerable_nextjs/actions.ts. |
| 2026-09-12 22:02:00 IST | Resolved | `run-20260912-220200-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SSRF-002] Missing Internal Network Protection
- **Finding ID:** `TG-SSRF-002-8378a839`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 65% (Medium Confidence)
- **Target:** `core/clustering.py:53`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SSRF-002-8378a839`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in core/clustering.py. |
| 2026-09-12 21:55:55 IST | Resolved | `run-20260912-215555-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SSRF-002] Missing Internal Network Protection
- **Finding ID:** `TG-SSRF-002-d08ed1ca`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 65% (Medium Confidence)
- **Target:** `examples/hardened-react-express/client/vite.config.js:7`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SSRF-002-d08ed1ca`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/hardened-react-express/client/vite.config.js. |
| 2026-09-12 21:55:55 IST | Resolved | `run-20260912-215555-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SSRF-002] Missing Internal Network Protection
- **Finding ID:** `TG-SSRF-002-a79cf464`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 65% (Medium Confidence)
- **Target:** `examples/hardened-react-express/server/index.js:121`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SSRF-002-a79cf464`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/hardened-react-express/server/index.js. |
| 2026-09-12 21:55:55 IST | Resolved | `run-20260912-215555-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SSRF-002] Missing Internal Network Protection
- **Finding ID:** `TG-SSRF-002-3c5a7c3c`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 65% (Medium Confidence)
- **Target:** `examples/vulnerable-react-express/client/src/App.jsx:42`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SSRF-002-3c5a7c3c`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/vulnerable-react-express/client/src/App.jsx. |
| 2026-09-12 21:55:55 IST | Resolved | `run-20260912-215555-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SSRF-002] Missing Internal Network Protection
- **Finding ID:** `TG-SSRF-002-13c81e3a`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 65% (Medium Confidence)
- **Target:** `examples/vulnerable-react-express/client/src/config.js:5`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SSRF-002-13c81e3a`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/vulnerable-react-express/client/src/config.js. |
| 2026-09-12 21:55:55 IST | Resolved | `run-20260912-215555-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SSRF-002] Missing Internal Network Protection
- **Finding ID:** `TG-SSRF-002-b0f87c06`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 65% (Medium Confidence)
- **Target:** `examples/vulnerable-react-express/client/vite.config.js:10`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SSRF-002-b0f87c06`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/vulnerable-react-express/client/vite.config.js. |
| 2026-09-12 21:55:55 IST | Resolved | `run-20260912-215555-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SSRF-002] Missing Internal Network Protection
- **Finding ID:** `TG-SSRF-002-ee77c629`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 65% (Medium Confidence)
- **Target:** `examples/vulnerable-react-express/server/index.js:82`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SSRF-002-ee77c629`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/vulnerable-react-express/server/index.js. |
| 2026-09-12 21:55:55 IST | Resolved | `run-20260912-215555-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SSRF-002] Missing Internal Network Protection
- **Finding ID:** `TG-SSRF-002-a0d1eac8`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 65% (Medium Confidence)
- **Target:** `skills/torusguard/payload/config/scope.json:4`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SSRF-002-a0d1eac8`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in skills/torusguard/payload/config/scope.json. |
| 2026-09-12 21:55:55 IST | Resolved | `run-20260912-215555-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SSRF-002] Missing Internal Network Protection
- **Finding ID:** `TG-SSRF-002-3ead2e3d`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 65% (Medium Confidence)
- **Target:** `skills/torusguard/payload/scripts/harden_runner.py:208`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SSRF-002-3ead2e3d`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in skills/torusguard/payload/scripts/harden_runner.py. |
| 2026-09-12 21:48:13 IST | Resolved | `run-20260912-214813-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SSRF-004] Unbounded Outbound Request Without Timeout
- **Finding ID:** `TG-SSRF-004-dcf3f71e`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 55% (Medium Confidence)
- **Target:** `examples/python/fastapi-hardened/main.py:30`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SSRF-004-dcf3f71e`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/python/fastapi-hardened/main.py. |
| 2026-09-12 21:57:31 IST | Resolved | `run-20260912-215731-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SSRF-004] Unbounded Outbound Request Without Timeout
- **Finding ID:** `TG-SSRF-004-d8472223`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 55% (Medium Confidence)
- **Target:** `examples/python/fastapi-vuln/main.py:9`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SSRF-004-d8472223`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/python/fastapi-vuln/main.py. |
| 2026-09-12 21:56:47 IST | Patch Formulated | `run-20260912-215555-audit` | Ponytail candidate bundle bnd-tg-ssrf-004-9-9803ad formulated (+1 / -1 lines). |
| 2026-09-12 21:59:29 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-ssrf-004-9-9803ad formulated (+1 / -1 lines). |
| 2026-09-12 22:00:07 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-ssrf-004-9-9803ad formulated (+1 / -1 lines). |
| 2026-09-12 22:00:15 IST | Patch Applied | `run-20260912-215731-audit` | Candidate patch applied to disk. Pre-apply snapshot saved in run-20260912-215731-audit. |
| 2026-09-12 22:02:27 IST | Resolved | `run-20260912-220227-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SSRF-004] Unbounded Outbound Request Without Timeout
- **Finding ID:** `TG-SSRF-004-4ac97262`
- **Status:** 🟢 RESOLVED
- **Severity:** Critical | **Confidence:** 55% (Medium Confidence)
- **Target:** `skills/torusguard/payload/scripts/harden_runner.py:341`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SSRF-004-4ac97262`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in skills/torusguard/payload/scripts/harden_runner.py. |
| 2026-09-12 21:48:13 IST | Resolved | `run-20260912-214813-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-AUTH-003] Missing Object-Level Authorization (IDOR)
- **Finding ID:** `TG-AUTH-003-6a05e509`
- **Status:** 🟢 RESOLVED
- **Severity:** High | **Confidence:** 55% (Medium Confidence)
- **Target:** `examples/hardened-react-express/server/index.js:49`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-AUTH-003-6a05e509`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/hardened-react-express/server/index.js. |
| 2026-09-12 21:56:47 IST | Patch Formulated | `run-20260912-215555-audit` | Ponytail candidate bundle bnd-tg-auth-003-49-7c96f3 formulated (+1 / -1 lines). |
| 2026-09-12 22:02:27 IST | Resolved | `run-20260912-220227-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-AUTH-004] Insecure Session Cookie Configuration
- **Finding ID:** `TG-AUTH-004-f60870ef`
- **Status:** 🟢 RESOLVED
- **Severity:** High | **Confidence:** 70% (High Confidence)
- **Target:** `skills/torusguard/payload/scripts/rules_sync.py:180`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-AUTH-004-f60870ef`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in skills/torusguard/payload/scripts/rules_sync.py. |
| 2026-09-12 21:55:55 IST | Resolved | `run-20260912-215555-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-AUTH-004] Insecure Session Cookie Configuration
- **Finding ID:** `TG-AUTH-004-6b0c7ebf`
- **Status:** 🟢 RESOLVED
- **Severity:** High | **Confidence:** 70% (High Confidence)
- **Target:** `skills/torusguard/payload/scripts/rules_sync.py:166`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-AUTH-004-6b0c7ebf`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in skills/torusguard/payload/scripts/rules_sync.py. |
| 2026-09-12 21:55:55 IST | Resolved | `run-20260912-215555-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-INPUT-001] Missing Server-Side Request Validation
- **Finding ID:** `TG-INPUT-001-dbe9cc30`
- **Status:** 🟢 RESOLVED
- **Severity:** High | **Confidence:** 70% (High Confidence)
- **Target:** `examples/vulnerable-react-express/server/index.js:77`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-INPUT-001-dbe9cc30`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 22:01:34 IST | Discovered | `run-20260912-220134-audit` | Initial discovery during static AST audit in examples/vulnerable-react-express/server/index.js. |
| 2026-09-12 22:02:00 IST | Resolved | `run-20260912-220200-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-INPUT-001] Missing Server-Side Request Validation
- **Finding ID:** `TG-INPUT-001-c7457f38`
- **Status:** 🟢 RESOLVED
- **Severity:** High | **Confidence:** 65% (Medium Confidence)
- **Target:** `examples/vulnerable-react-express/server/index.js:27`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-INPUT-001-c7457f38`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/vulnerable-react-express/server/index.js. |
| 2026-09-12 22:00:07 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-input-001-27-2486f1 formulated (+1 / -1 lines). |
| 2026-09-12 22:00:15 IST | Patch Applied | `run-20260912-215731-audit` | Candidate patch applied to disk. Pre-apply snapshot saved in run-20260912-215731-audit. |
| 2026-09-12 22:02:27 IST | Resolved | `run-20260912-220227-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-INPUT-003] Unsafe Dynamic Code or HTML Execution
- **Finding ID:** `TG-INPUT-003-fea9421e`
- **Status:** 🟢 RESOLVED
- **Severity:** High | **Confidence:** 80% (High Confidence)
- **Target:** `examples/vulnerable-react-express/client/src/App.jsx:53`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-INPUT-003-fea9421e`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/vulnerable-react-express/client/src/App.jsx. |
| 2026-09-12 21:56:47 IST | Patch Formulated | `run-20260912-215555-audit` | Ponytail candidate bundle bnd-tg-input-003-53-d167b4 formulated (+1 / -1 lines). |
| 2026-09-12 21:59:29 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-input-003-53-d167b4 formulated (+1 / -1 lines). |
| 2026-09-12 22:00:07 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-input-003-53-d167b4 formulated (+1 / -1 lines). |
| 2026-09-12 22:00:15 IST | Patch Applied | `run-20260912-215731-audit` | Candidate patch applied to disk. Pre-apply snapshot saved in run-20260912-215731-audit. |
| 2026-09-12 22:02:27 IST | Resolved | `run-20260912-220227-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-PLATFORM-001] Wildcard CORS With Credentials
- **Finding ID:** `TG-PLATFORM-001-7dd35cb4`
- **Status:** 🟢 RESOLVED
- **Severity:** High | **Confidence:** 80% (High Confidence)
- **Target:** `examples/vulnerable-react-express/server/index.js:12`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-PLATFORM-001-7dd35cb4`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/vulnerable-react-express/server/index.js. |
| 2026-09-12 21:56:47 IST | Patch Formulated | `run-20260912-215555-audit` | Ponytail candidate bundle bnd-tg-platform-001-12-cf8156 formulated (+1 / -1 lines). |
| 2026-09-12 21:59:29 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-platform-001-12-cf8156 formulated (+1 / -1 lines). |
| 2026-09-12 22:00:07 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-platform-001-12-cf8156 formulated (+1 / -1 lines). |
| 2026-09-12 22:00:15 IST | Patch Applied | `run-20260912-215731-audit` | Candidate patch applied to disk. Pre-apply snapshot saved in run-20260912-215731-audit. |
| 2026-09-12 22:02:27 IST | Resolved | `run-20260912-220227-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-PLATFORM-001] Wildcard CORS With Credentials
- **Finding ID:** `TG-PLATFORM-001-1a813dde`
- **Status:** 🟢 RESOLVED
- **Severity:** High | **Confidence:** 80% (High Confidence)
- **Target:** `skills/torusguard/payload/scripts/harden_runner.py:202`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-PLATFORM-001-1a813dde`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in skills/torusguard/payload/scripts/harden_runner.py. |
| 2026-09-12 21:48:13 IST | Resolved | `run-20260912-214813-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-RATE-001] Unlimited Authentication Endpoint
- **Finding ID:** `TG-RATE-001-dcd0a3c7`
- **Status:** 🟢 RESOLVED
- **Severity:** High | **Confidence:** 65% (Medium Confidence)
- **Target:** `examples/vulnerable-react-express/server/index.js:26`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-RATE-001-dcd0a3c7`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/vulnerable-react-express/server/index.js. |
| 2026-09-12 21:56:47 IST | Patch Formulated | `run-20260912-215555-audit` | Ponytail candidate bundle bnd-tg-rate-001-26-affcfa formulated (+1 / -1 lines). |
| 2026-09-12 21:59:29 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-rate-001-26-affcfa formulated (+1 / -1 lines). |
| 2026-09-12 22:00:07 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-rate-001-26-affcfa formulated (+1 / -1 lines). |
| 2026-09-12 22:00:15 IST | Patch Applied | `run-20260912-215731-audit` | Candidate patch applied to disk. Pre-apply snapshot saved in run-20260912-215731-audit. |
| 2026-09-12 22:02:27 IST | Resolved | `run-20260912-220227-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-CLIENT-001] Public Production Source Maps
- **Finding ID:** `TG-CLIENT-001-1ba4789e`
- **Status:** 🟢 RESOLVED
- **Severity:** Medium | **Confidence:** 65% (Medium Confidence)
- **Target:** `examples/vulnerable-react-express/client/vite.config.js:7`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-CLIENT-001-1ba4789e`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/vulnerable-react-express/client/vite.config.js. |
| 2026-09-12 22:00:07 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-client-001-7-587129 formulated (+1 / -1 lines). |
| 2026-09-12 22:00:15 IST | Patch Applied | `run-20260912-215731-audit` | Candidate patch applied to disk. Pre-apply snapshot saved in run-20260912-215731-audit. |
| 2026-09-12 22:02:27 IST | Resolved | `run-20260912-220227-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-PLATFORM-002] Missing Security Headers
- **Finding ID:** `TG-PLATFORM-002-1f383dcf`
- **Status:** 🟢 RESOLVED
- **Severity:** Medium | **Confidence:** 65% (Medium Confidence)
- **Target:** `examples/hardened-react-express/server/index.js:17`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-PLATFORM-002-1f383dcf`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/hardened-react-express/server/index.js. |
| 2026-09-12 22:00:07 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-platform-002-17-876973 formulated (+1 / -1 lines). |
| 2026-09-12 22:00:15 IST | Patch Applied | `run-20260912-215731-audit` | Candidate patch applied to disk. Pre-apply snapshot saved in run-20260912-215731-audit. |
| 2026-09-12 22:02:27 IST | Resolved | `run-20260912-220227-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-PLATFORM-002] Missing Security Headers
- **Finding ID:** `TG-PLATFORM-002-eef342ec`
- **Status:** 🟢 RESOLVED
- **Severity:** Medium | **Confidence:** 65% (Medium Confidence)
- **Target:** `examples/vulnerable-react-express/server/index.js:5`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-PLATFORM-002-eef342ec`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/vulnerable-react-express/server/index.js. |
| 2026-09-12 22:00:07 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-platform-002-5-40c794 formulated (+1 / -1 lines). |
| 2026-09-12 22:00:15 IST | Patch Applied | `run-20260912-215731-audit` | Candidate patch applied to disk. Pre-apply snapshot saved in run-20260912-215731-audit. |
| 2026-09-12 22:02:27 IST | Resolved | `run-20260912-220227-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-PLATFORM-003] Production Stack Trace Exposure
- **Finding ID:** `TG-PLATFORM-003-f5fce823`
- **Status:** 🟢 RESOLVED
- **Severity:** Medium | **Confidence:** 55% (Medium Confidence)
- **Target:** `skills/torusguard/payload/scripts/harden_runner.py:357`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-PLATFORM-003-f5fce823`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in skills/torusguard/payload/scripts/harden_runner.py. |
| 2026-09-12 21:48:13 IST | Resolved | `run-20260912-214813-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-RATE-002] Unlimited Public Write Endpoint
- **Finding ID:** `TG-RATE-002-d67d7c98`
- **Status:** 🟢 RESOLVED
- **Severity:** Medium | **Confidence:** 65% (Medium Confidence)
- **Target:** `examples/vulnerable-react-express/server/index.js:54`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-RATE-002-d67d7c98`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/vulnerable-react-express/server/index.js. |
| 2026-09-12 22:00:07 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-rate-002-54-0b38d2 formulated (+1 / -1 lines). |
| 2026-09-12 22:00:15 IST | Patch Applied | `run-20260912-215731-audit` | Candidate patch applied to disk. Pre-apply snapshot saved in run-20260912-215731-audit. |
| 2026-09-12 22:02:27 IST | Resolved | `run-20260912-220227-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SEC-004] Sensitive Information in Logs
- **Finding ID:** `TG-SEC-004-dbbc17f7`
- **Status:** 🟢 RESOLVED
- **Severity:** Medium | **Confidence:** 70% (High Confidence)
- **Target:** `examples/vulnerable-react-express/client/src/App.jsx:30`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SEC-004-dbbc17f7`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/vulnerable-react-express/client/src/App.jsx. |
| 2026-09-12 22:00:07 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-sec-004-30-00569e formulated (+1 / -1 lines). |
| 2026-09-12 22:00:15 IST | Patch Applied | `run-20260912-215731-audit` | Candidate patch applied to disk. Pre-apply snapshot saved in run-20260912-215731-audit. |
| 2026-09-12 22:02:27 IST | Resolved | `run-20260912-220227-audit` | Finding no longer detected in source code during latest audit pass. |

---

### [TG-SEC-004] Sensitive Information in Logs
- **Finding ID:** `TG-SEC-004-08753da5`
- **Status:** 🟢 RESOLVED
- **Severity:** Medium | **Confidence:** 70% (High Confidence)
- **Target:** `examples/vulnerable-react-express/server/index.js:28`

**What is wrong:**  
Security violation detected by TorusGuard scanner.

**Why it matters:**  
Violates TorusGuard strict production safety and isolation invariant.

#### Lifecycle History for `TG-SEC-004-08753da5`
| Timestamp | Action | Run ID | Details |
| :--- | :--- | :--- | :--- |
| 2026-09-12 21:41:10 IST | Discovered | `run-20260912-214110-audit` | Initial discovery during static AST audit in examples/vulnerable-react-express/server/index.js. |
| 2026-09-12 22:00:07 IST | Patch Formulated | `run-20260912-215731-audit` | Ponytail candidate bundle bnd-tg-sec-004-28-a1a0a1 formulated (+1 / -1 lines). |
| 2026-09-12 22:00:15 IST | Patch Applied | `run-20260912-215731-audit` | Candidate patch applied to disk. Pre-apply snapshot saved in run-20260912-215731-audit. |
| 2026-09-12 22:02:27 IST | Resolved | `run-20260912-220227-audit` | Finding no longer detected in source code during latest audit pass. |

---
