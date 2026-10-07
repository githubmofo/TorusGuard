---
name: torusguard-ocr-scan
description: Scans images, architecture diagrams, and screenshots via Hybrid First-Principles + Tesseract OCR for leaked API keys, tokens, and credentials via CLI or AI Agent.
version: 2.2.0
workflow: .torusguard/workflows/ocr-scan.md
tools: Read, Grep, Glob, Write, run_command
scripts-binding:
  - internal/scanner/ocr.go
  - cmd/torusguard/main.go
---

# TorusGuard OCR Vision Scan — Multi-Modal Secret Extraction

## Objective
Detect optical leaks of private API keys, AWS credentials, database URIs, GitHub personal access tokens, and private certificates embedded inside visual artifacts (PNG, JPG, JPEG, WebP, SVG, BMP, TIFF) up to 10MB using a **Hybrid First-Principles engine** (zero external dependencies) combined with optional **Tesseract deep optical character recognition**.

---

## Tri-Mode Execution

### Mode A: Automated CLI Execution
Run OCR scanning against the entire project (auto-discovery) or a specific visual asset:
```bash
# Auto-discover and scan all images and diagrams across the workspace
torusguard ocr-scan

# Or via npx (zero installation):
npx torusguard ocr-scan

# Scan a specific architecture diagram or screenshot
torusguard ocr-scan docs/architecture/diagram.png

# Scan an entire directory of media assets
torusguard ocr-scan ./assets/images/
```

### Mode B: In-Session AI Chat Slash Command
Run `/torusguard ocr-scan [path]` in chat.
The agent invokes the native Go scanner or MCP tool to extract optical and embedded text, analyze credential patterns, and report leaked keys.

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
- **TG-SEC-006:** JSON Web Tokens (`eyJ...`).
- **TG-SEC-007:** Plaintext passwords and assignment credentials.
- **10MB DoS Guard:** Files exceeding 10MB are rejected fail-closed to prevent resource exhaustion attacks.

---

## 🏛️ Hybrid Architecture: Zero-Dependency First-Principles + Optional Deep OCR
1. **First-Principles Extraction (Always Active, Zero Dependencies):**
   - Directly parses PNG metadata chunks (`tEXt`, `zTXt`, `iTXt`).
   - Parses SVG XML tags and inner text nodes.
   - Extracts EXIF metadata and uncompressed printable string sequences ($\ge 6$ chars).
2. **Deep Optical Recognition (Optional):**
   - If Tesseract OCR is installed in PATH, TorusGuard executes deep optical character recognition on flattened pixel rasters.
   - If Tesseract is not installed, TorusGuard **never crashes or aborts**; it scans via first-principles and provides 1-line install guidance.

---

## 🚨 LLM Trap Table

| Pattern | What AI Does Wrong | What Is Actually Correct |
| :--- | :--- | :--- |
| **Reading Binary Images as Text** | Attempts to read raw `.png` or `.jpg` with `view_file` as utf-8 text. | Invoke `torusguard ocr-scan` or `torusguard_ocr_scan` to perform OCR. |
| **Crashing When Tesseract Is Missing** | Aborts scan if Tesseract binary is not on system PATH. | Rely on TorusGuard's built-in first-principles extractor; it handles images natively without crashing. |
| **Ignoring Image File Size Bounds** | Tries to OCR multi-hundred megabyte video files or giant raw images. | Adhere to the 10MB DoS boundary (`DefaultMaxImageSize`). |
| **Echoing Full Leaked Secrets in Logs** | Prints live production credentials unredacted in terminal output or reports. | Partially redact sensitive tokens (e.g. `sk-live-****3211`). |
| **Assuming Images Don't Contain Secrets** | Audits only `.go` or `.js` code and ignores cloud diagrams or screenshots. | Always run OCR vision scan across image directories during full audits. |

---

## ✅ Pre-Flight Self-Audit

Before concluding an OCR inspection, verify:
- [ ] Did I run `torusguard ocr-scan` to inspect images and diagrams?
- [ ] Are all target files valid image formats (`.png`, `.jpg`, `.jpeg`, `.webp`, `.svg`, `.bmp`, `.tiff`)?
- [ ] Are target image file sizes strictly $\le 10$ MB?
- [ ] Did I check against all 7 canonical secret signatures (`TG-SEC-001` through `TG-SEC-007`)?
- [ ] Are confirmed leaks documented in `security_report.md` with remediation steps?

---

## 🔁 VBC Protocol (Verify → Build → Confirm)

```
VERIFY: Confirm target image existence and size <= 10MB (or auto-discover workspace images).
BUILD:  Execute torusguard ocr-scan or torusguard_ocr_scan to extract optical/embedded text.
CONFIRM: Match text against OCRSecretPattern signatures, redact sensitive tokens, and record in security_report.md.
```
