# /torusguard-ocr-scan — Multi-Modal OCR Secret Scanning

$ARGUMENTS

---

## Objective
Detect optical leaks of private API keys, AWS credentials, database URIs, GitHub personal access tokens, and private certificates embedded inside visual artifacts (`.png`, `.jpg`, `.jpeg`, `.webp`, `.svg`, `.bmp`, `.tiff`) up to 10MB using a **Hybrid First-Principles engine** (zero external dependencies) and optional **Tesseract deep optical character recognition**.

---

## Tri-Mode Parity
- **Mode A (Terminal CLI):** `torusguard ocr-scan [target]` or `npx torusguard ocr-scan [target]`
- **Mode B (AI Chat Slash Command):** `/torusguard ocr-scan [target]`
- **Mode C (Native MCP Tool):** `torusguard_ocr_scan`

---

## Execution Steps

1. **Discover or Verify Target:**
   - If a target path is provided, verify it exists on disk.
   - If no target is provided, auto-discover all images (`.png`, `.jpg`, `.jpeg`, `.webp`, `.svg`, `.bmp`) across the workspace.
2. **Inspect File Size Bounds:** Reject files exceeding 10MB (`DefaultMaxImageSize`) to preserve DoS resilience.
3. **Execute Hybrid OCR Extraction:**
   - Run first-principles embedded text extraction (PNG chunks, SVG tags, EXIF, byte streams).
   - If Tesseract is installed, execute deep optical character recognition on pixel rasters.
   - If Tesseract is not installed, continue cleanly with first-principles text without crashing.
4. **Pattern Match Secrets:** Evaluate extracted text against `TG-SEC-001` through `TG-SEC-007` signatures.
5. **Redact & Report:** Emit sanitized 75-column finding cards and synchronize findings into `security_report.md`.
