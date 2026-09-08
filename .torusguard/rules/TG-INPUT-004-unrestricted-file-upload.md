# TG-INPUT-004: Unrestricted File Upload

## Severity
High

## Applies To
- Profile avatar and document upload endpoints
- Media management APIs and admin upload tools
- Import features that accept archives or spreadsheets
- Object storage presigned upload workflows

## Why It Matters
Unrestricted uploads let attackers store executable scripts, malware, oversized payloads, and deceptive file types.
If uploaded files are publicly accessible or processed unsafely, attackers can trigger XSS, remote code execution, SSRF through parsers, or storage exhaustion denial of service.
Weak upload controls also create legal and compliance risk when sensitive content is mishandled.

## What TorusGuard Looks For
- Acceptance based only on filename extension or client-provided MIME type.
- Missing maximum file size, count, or rate limits.
- Uploading directly to web-served directories without safe naming.
- Lack of malware scanning or content-type verification by signature.
- Processing of complex formats without sandboxing and strict parser limits.

## Unsafe Example
```js
app.post("/api/upload", upload.single("file"), async (req, res) => {
  const file = req.file;

  // Trusts original name and MIME from client
  const destination = path.join(__dirname, "public/uploads", file.originalname);
  await fs.promises.writeFile(destination, file.buffer);

  // Public URL serves whatever was uploaded
  res.json({ ok: true, url: `/uploads/${file.originalname}` });
});
```

## Safe Example
```js
import crypto from "crypto";
import FileType from "file-type";

const MAX_SIZE = 5 * 1024 * 1024;
const ALLOWED = new Set(["image/png", "image/jpeg", "application/pdf"]);

app.post("/api/upload", upload.single("file"), async (req, res) => {
  const file = req.file;
  if (!file || file.size > MAX_SIZE) {
    return res.status(400).json({ ok: false, error: "Invalid file size" });
  }

  const detected = await FileType.fromBuffer(file.buffer);
  const mime = detected?.mime || "";
  if (!ALLOWED.has(mime)) {
    return res.status(400).json({ ok: false, error: "Unsupported file type" });
  }

  const extension = mime === "image/png" ? "png" : mime === "image/jpeg" ? "jpg" : "pdf";
  const storedName = `${crypto.randomUUID()}.${extension}`;
  const storagePath = path.join(__dirname, "private_uploads", storedName);

  await fs.promises.writeFile(storagePath, file.buffer, { mode: 0o600 });
  await queueForMalwareScan(storagePath);

  res.json({ ok: true, fileId: storedName });
});
```

## Remediation
1. Enforce strict allowlists for file type, extension, and verified signature/MIME.
2. Set max size, max count, and upload rate limits per user and per endpoint.
3. Store files outside web root with generated names, never original filenames.
4. Scan uploaded content with malware detection before making files retrievable.
5. Re-validate file safety at retrieval and transformation points (thumbnailing, OCR, parsing).
6. Use presigned uploads with constrained policies and short expirations where applicable.

## Verification
- Upload files with double extensions (`.jpg.php`) and mismatched MIME signatures.
- Attempt oversized and high-frequency uploads to validate throttling and limits.
- Confirm stored filenames are non-guessable and not user-controlled.
- Verify uploaded objects cannot be executed as active content by browsers.
- Ensure parser pipelines reject malformed archives and nested compression bombs.

## False Positives and Exceptions
- Internal-only transfer channels with signed artifacts may permit broader file types, but must still enforce size and scanning controls.
- Some media pipelines rely on asynchronous scanning; temporary quarantine states are acceptable with blocked access until scan completion.
- Legacy endpoints may need phased migration, but unrestricted direct serving is not acceptable long term.

## Related Rules
- [TG-INPUT-001](./TG-INPUT-001-missing-server-validation.md)
- [TG-INPUT-003](./TG-INPUT-003-unsafe-html-or-code-execution.md)
- [TG-AUTH-004](./TG-AUTH-004-insecure-session-cookie.md)
