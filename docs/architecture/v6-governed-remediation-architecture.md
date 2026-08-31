# TorusGuard v6 Governed Remediation & Targeted Recheck Architecture

**Specification Version:** `6.0.0`  
**Date:** August 31, 2026  
**Status:** Approved Architectural Standard

---

## 1. Architectural Vision

TorusGuard v6 transforms static application security analysis into a **closed-loop, governed remediation system**. Rather than acting as a passive scanner that emits uncoordinated findings, TorusGuard v6 coordinates the complete path from discovery to safe code modification and differential recheck.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          AI Agent & User Interface                          │
│     (Commands: /torusguard init, audit, verify, harden, apply, recheck)     │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                    TorusGuard v6 Workflow Controller                        │
│                                                                             │
│  ┌──────────────────────┐  ┌─────────────────────┐  ┌────────────────────┐  │
│  │   Identity Engine    │  │  Clustering Engine  │  │   Bundle Manager   │  │
│  │  (Stable Fingerprint)│  │ (Root-Cause Groups) │  │(Remediation Guides)│  │
│  └──────────────────────┘  └─────────────────────┘  └────────────────────┘  │
│  ┌──────────────────────┐  ┌─────────────────────┐  ┌────────────────────┐  │
│  │    Patch Governor    │  │  Targeted Rechecker │  │   SARIF Exporter   │  │
│  │  (Policy Enforcement)│  │ (Scoped Re-audits)  │  │  (JSON v2.1.0)     │  │
│  └──────────────────────┘  └─────────────────────┘  └────────────────────┘  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                         Isolated Run Folder System                          │
│                           runs/<run-id>/                                    │
│   manifest.json   summary.md   findings.md   remediation.md   apply-plan.md │
│   recheck.md      evidence.json diff-summary.md changed-files.txt sarif.json│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Subsystems

### 2.1. Stable Finding Identity Engine (`core/identity.py`)
Computes immutable fingerprints invariant to whitespace, single-line comments, and line number shifts:
$$\text{Fingerprint} = \text{SHA-256}(\text{RuleID} \parallel \text{NormalizedPath} \parallel \text{RegionHash} \parallel \text{SinkSignature})$$

### 2.2. Root-Cause Clustering Engine (`core/clustering.py`)
Aggregates individual findings into systemic root-cause clusters to facilitate holistic architectural remediation.

### 2.3. Remediation Bundle Manager (`core/bundle.py`)
Emits five standardized artifacts per finding bundle:
- `finding.md`: Contextual problem statement and why it matters.
- `remediation.md`: Framework-native recommendations and target file list.
- `minimal_patch_plan.md`: Unified diff preview.
- `verify-after-change.md`: Explicit verification command and test assertions.
- `metadata.json`: Machine-readable metadata.

### 2.4. Minimal Patch Governor (`core/governance.py`)
Enforces Ponytail-style minimal diff governance before applying patches:
- Max additions and deletions limits.
- Max touched files limit ($\le 2$ files).
- High-risk context escalation (auth, credentials, database, crypto, upload endpoints).
- Rejects boilerplate, excessive commentary, and full file rewrites.

### 2.5. Targeted Rechecker (`core/rechecker.py`)
Re-evaluates modified scopes and adjacent trust boundaries to determine resolution:
- **`Confirmed Fixed`:** Vulnerability resolved; 0 regressions.
- **`Partially Fixed`:** Safe pattern added but unsafe path remains accessible.
- **`Needs Manual Review`:** Requires external infrastructure or runtime authentication.
- **`Regressed`:** Patch introduced a secondary flaw.
- **`Not Reproducible`:** Target code unchanged.

### 2.6. Standard SARIF v2.1.0 Exporter (`core/sarif.py`)
Produces OASIS standard SARIF v2.1.0 JSON documents with stable fingerprints for ecosystem interoperability.

---

## 3. Run Folder Specification

Every TorusGuard run is isolated in `.torusguard/runs/<run-id>/` containing:
1. `manifest.json`: Execution metadata, git commit hash, status counts.
2. `summary.md`: Executive summary & cluster table.
3. `findings.md`: Detailed finding descriptions with confidence scores.
4. `remediation.md`: Remediation guides grouped by cluster.
5. `apply-plan.md`: Patch policy decisions and churn summary.
6. `recheck.md`: Targeted recheck outcome and regression analysis.
7. `evidence.json`: Cryptographic evidence ledger.
8. `diff-summary.md`: Unified diff of applied patches.
9. `changed-files.txt`: Modified file listing.
10. `sarif.json`: SARIF v2.1.0 output.
11. `logs/`: Runtime logs.
