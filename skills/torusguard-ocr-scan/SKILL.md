---
name: torusguard-ocr-scan
description: Scans images, architecture diagrams, and screenshots via Tesseract OCR for leaked API keys, tokens, and credentials via CLI or AI Agent.
version: 2.0.0
workflow: .torusguard/workflows/ocr-scan.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - internal/scanner/ocr.go
  - cmd/torusguard/main.go
---

# TorusGuard OCR Vision Scan — Multi-Modal Secret Extraction

## Objective
Detect optical leaks of private API keys, AWS credentials, database URIs, GitHub personal access tokens, and private certificates embedded inside visual artifacts (PNG, JPG, WebP, BMP, TIFF) up to 10MB using Tesseract OCR and deterministic regex signatures.

---

## Tri-Mode Execution

### Mode A: Automated CLI Execution
Run OCR scanning against a single diagram file or an entire directory of visual assets:
```bash
# Scan a specific architecture diagram or screenshot
torusguard ocr-scan docs/architecture/diagram.png

# Scan an entire directory of media assets
torusguard ocr-scan ./assets/images/
```

### Mode B: In-Session AI Chat Slash Command
Run `/torusguard ocr-scan <path>` in chat.
The agent invokes the native Go scanner or MCP tool to extract optical text, analyze credential patterns, and report leaked keys.

### Mode C: Native MCP Tool Call
MCP-enabled coding agents (Antigravity, Cursor, Windsurf, Claude Code) call:
```json
{
  "tool": "torusguard_ocr_scan",
  "arguments": {
    "target": "docs/architecture/cloud-architecture.png",
    "max_image_mb": 10
  }
}
```

---

## Supported Patterns & Invariants
- **TG-SEC-001:** Hardcoded API Keys / Tokens / OpenAI & Stripe Keys (`sk-live-...`, `sk-...`).
- **TG-SEC-002:** AWS Access Key IDs (`AKIA[0-9A-Z]{16}`).
- **TG-SEC-003:** GitHub Personal Access Tokens (`ghp_...`, `github_pat_...`).
- **TG-SEC-004:** Database Connection URIs (`postgres://user:pass@host:5432/db`).
- **TG-SEC-005:** Private Key Headers (`-----BEGIN RSA PRIVATE KEY-----`).
- **TG-SEC-007:** Password assignments (`password = "..."`).
- **10MB DoS Guard:** Files exceeding 10MB are rejected fail-closed to prevent resource exhaustion attacks.

---

## 🏛️ OpenCodeReview Hybrid Architecture Integration
- **Deterministic OCR Preprocessing:** Optical extraction and regex pattern matching run entirely in compiled Go code without LLM hallucination.
- **Token Efficiency:** Only the extracted text and detected secret matches are emitted to the agent context (zero token waste on binary image blobs).

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Reading Binary Images as Text** | Attempts to read raw `.png` or `.jpg` with `view_file` as utf-8 text. | Invoke `torusguard ocr-scan` or `torusguard_ocr_scan` to perform OCR. |
| **Ignoring Image File Size Bounds** | Tries to OCR multi-hundred megabyte video files or giant raw images. | Adhere to the 10MB DoS boundary (`DefaultMaxImageSize`). |
| **Echoing Full Leaked Secrets in Logs** | Prints live production credentials unredacted in terminal output or reports. | Partially redact sensitive tokens (e.g. `sk-live-****3211`). |
| **Assuming Images Don't Contain Secrets** | Audits only `.go` or `.js` code and ignores cloud diagrams or screenshots. | Always run OCR vision scan across image directories during full audits. |

---

## ✅ Pre-Flight Self-Audit

Before concluding an OCR inspection, verify:
- [ ] Is Tesseract installed and discoverable on PATH?
- [ ] Are all target files valid image formats (`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tiff`)?
- [ ] Are target image file sizes strictly $\le 10$ MB?
- [ ] Did I check against all 7 canonical secret signatures (`TG-SEC-001` through `TG-SEC-007`)?
- [ ] Are confirmed leaks documented in `security_report.md` with remediation steps?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY: Confirm target image existence and size <= 10MB.
BUILD:  Execute torusguard ocr-scan or torusguard_ocr_scan to extract optical text.
CONFIRM: Match text against OCRSecretPattern signatures, redact sensitive tokens, and record in security_report.md.
```
