# TorusGuard Data & Storage Architecture

## 1. Storage Philosophy
TorusGuard employs an **immutable, flat-file JSON and Markdown storage architecture**. To maintain zero external dependencies, portability across air-gapped systems, and native version control integration, TorusGuard does not require an external database server (such as PostgreSQL or SQLite).

All persistence occurs in the local repository workspace under `.torusguard/runs/`.

---

## 2. Directory & Run Folder Hierarchy

Every execution generates a hermetically isolated, timestamped run directory:

```text
.torusguard/
└── runs/
    └── run-20260827-110000-django-core/
        ├── metadata.json              # Run profile, timestamp, tool version, commit hash
        ├── findings/                  # Granular JSON finding documents
        │   ├── finding-001.json
        │   └── finding-002.json
        ├── evidence/                  # Raw code snippets with SHA-256 integrity
        │   ├── evidence-001.txt
        │   └── evidence-002.txt
        ├── patches/                   # Ponytail unified Git diffs
        │   └── patch-001.diff
        ├── recheck/                   # Differential recheck validation log
        │   └── recheck-log.json
        └── validation/                # Rendered human-readable Markdown report
            └── large-project-report.md
```

---

## 3. Entity Data Models

### 3.1. Metadata Schema (`metadata.json`)
| Field | Type | Description |
|---|---|---|
| `run_id` | String | Canonical UUID or timestamped identifier (`run-YYYYMMDD-HHMMSS-<target>`) |
| `version` | String | TorusGuard core engine release version (`v0.5.6`) |
| `timestamp` | ISO-8601 | Exact scan start timestamp |
| `project_id` | String | Target repository identifier from `manifest.yaml` |
| `git_commit` | String | Current HEAD commit SHA-1 of the scanned repository |
| `files_analyzed`| Integer | Total relevant source files scanned |
| `active_rules` | Array[String]| List of enabled Rule IDs |

### 3.2. Finding Entity Structure
```text
Finding
├── finding_id: UUID
├── rule_id: String (e.g. TG-DB-004)
├── title: String
├── severity: Enum [Critical, High, Medium, Low, Info]
├── priority: Enum [Immediate P0, Near-Term P1, Backlog P2]
├── confidence:
│   ├── score: Integer (0-100)
│   └── band: Enum [Confirmed, High, Needs Review, Informational]
├── provenance:
│   ├── discovery_engine: String
│   ├── decision_path: Array[String]
│   └── raw_evidence_hash: SHA-256 String
├── target:
│   ├── file_path: String
│   ├── start_line: Integer
│   └── end_line: Integer
└── lifecycle:
    ├── current_stage: Enum [Detect, Classify, Verify, Remediate, Recheck, Archive]
    └── history: Array[LifecycleTransition]
```

### 3.3. Retest Record Structure
```text
RetestRecord
├── retest_id: UUID
├── finding_id: UUID
├── timestamp: ISO-8601
├── status: Enum [Verified Fixed, Still Present, Partially Fixed, New Risk]
├── diff_applied: String (Path to diff)
├── test_suite_result: Enum [Passed, Failed, Unavailable]
└── verified_evidence_hash: SHA-256 String
```

---

## 4. Integrity & Retention Policies
- **Immutability:** Run folders are strictly append-only. Subsequent audits or rechecks create new timestamped run folders without overwriting historical records.
- **Git Tracking:** Developers may optionally commit `.torusguard/runs/` to track historical security progress directly in Git version history.
