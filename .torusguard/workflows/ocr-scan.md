# /torusguard-ocr-scan — Multi-Modal OCR Secret Scanning

$ARGUMENTS

---

## Objective
Detect optical leaks of private API keys, AWS credentials, database URIs, GitHub personal access tokens, and private certificates embedded inside visual artifacts (`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tiff`) up to 10MB using Tesseract OCR and deterministic regex signatures.

---

## Tri-Mode Parity
- **Mode A (Terminal CLI):** `torusguard ocr-scan <target>`
- **Mode B (AI Chat Slash Command):** `/torusguard ocr-scan <target>`
- **Mode C (Native MCP Tool):** `torusguard_ocr_scan`

---

## Execution Steps

1. **Verify Target:** Check target image or directory exists on disk.
2. **Inspect File Size:** Reject images exceeding 10MB (`DefaultMaxImageSize`) to preserve DoS resilience.
3. **Execute OCR Extraction:** Run Tesseract optical text analysis via Go scanner or MCP tool.
4. **Pattern Match Secrets:** Evaluate optical text against `TG-SEC-001` through `TG-SEC-007` signatures.
5. **Redact & Report:** Emit sanitized finding cards and synchronize into `security_report.md`.
