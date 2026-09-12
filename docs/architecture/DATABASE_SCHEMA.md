# TorusGuard Data & Storage Architecture

## 1. Storage Philosophy
TorusGuard employs an **immutable, flat-file JSON and Markdown storage architecture**. To maintain zero external dependencies, portability across air-gapped systems, and native version control integration, TorusGuard does not require an external database server (such as PostgreSQL or SQLite).

All persistence occurs in the local repository workspace across three storage tiers:
1. **Living Security Report Ground Truth:** `security_report.md` at workspace root.
2. **Adaptive Security Memory Engine:** `.torusguard/memory/` (persistent patterns, events, context).
3. **Execution Run Isolation & Snapshots:** `.torusguard/runs/<run_id>/` and `.torusguard/snapshots/<run_id>/`.

---

## 2. Directory & Run Folder Hierarchy

Every execution generates an isolated, timestamped run directory and updates the living report:

```text
TorusGuard/
├── security_report.md                 # Single source of truth for findings & health score
├── .torusguard/
│   ├── memory/                        # Adaptive persistent memory
│   │   ├── events/                    # Append-only ledger of audit/apply/recheck events
│   │   ├── patterns.json              # Distilled Golden Fix Recipes and confirmed patterns
│   │   ├── context.json               # Fast prompt context card
│   │   └── profile.json               # Workspace security DNA
│   ├── snapshots/                     # Pre-apply rollback backups
│   │   └── run-20260912-221500/
│   │       └── target_file.ts.bak     # Byte-for-byte pre-apply backup
│   └── runs/                          # Execution history folders
│       └── run-20260912-221500-audit/
│           ├── manifest.json          # Run profile, timestamp, version, commit hash
│           ├── findings.json          # Raw structured finding objects
│           ├── summary.md             # Executive summary
│           ├── results.sarif          # OASIS SARIF v2.1.0 structured export
│           ├── report-latest.html     # Standalone visual dark-mode HTML report
│           └── bundles/               # Formulated Ponytail candidate patch bundles
│               └── TG-CSRF-001/
│                   ├── patch.diff
│                   └── minimal_patch_plan.md
```

---

## 3. Entity Data Models

### 3.1. Living Report Finding Entity Structure
```text
Finding
├── finding_id: String (e.g. TG-CSRF-001)
├── rule_id: String (e.g. TG-CSRF-001)
├── title: String
├── severity: Enum [Critical, High, Medium, Low, Informational]
├── priority: Enum [Immediate P0, Near-Term P1, Backlog P2]
├── status: Enum [OPEN 🔴, VERIFIED 🟠, CANDIDATE 🟡, APPLIED 🔵, RESOLVED 🟢, REGRESSED ❌, FALSE POSITIVE ⚪]
├── confidence_score: Integer (0-100)
├── fingerprint: String (line-shift invariant hash)
├── target:
│   ├── file_path: String
│   ├── line_number: Integer
│   └── line_content: String
└── history: Array[LifecycleEvent]
    ├── event_id: String
    ├── timestamp: ISO-8601 (IST)
    ├── transition: String
    └── run_id: String
```

### 3.2. Golden Fix Recipe Structure (`patterns.json`)
```text
GoldenRecipe
├── recipe_id: String
├── rule_id: String
├── framework: String
├── patch_diff: Unified Diff String
├── additions: Integer (<= 35)
├── deletions: Integer (<= 25)
├── verified_at: ISO-8601 (IST)
└── confidence_multiplier: Float
```

---

## 4. Integrity & Retention Policies
- **Immutability:** Run folders and event ledgers are strictly append-only.
- **Rollback Guarantee:** Snapshots in `.torusguard/snapshots/<run_id>/` guarantee 100% byte-for-byte restoration via `npx torusguard rollback`.
- **TTL Decay:** Stale memory advice automatically decays after 90 days.
