# TorusGuard Skill Reference: C# & ASP.NET Core Security

> **Loaded When:** A project is identified as a C# / .NET application (`*.csproj`, `*.sln`, ASP.NET Core detected).

---

## 🛡️ Key Inspection Areas & Rules

### 1. Authentication & Authorization
* `TG-AUTH-001`: Ensure controllers and endpoints have `[Authorize]` attributes.
* Prohibit unvetted `[AllowAnonymous]` on sensitive business logic or user data endpoints.

### 2. Entity Framework Core & SQL Injection
* `TG-INPUT-002`: Use LINQ expressions or `FromSqlInterpolated` with interpolated string syntax (EF Core converts parameters automatically).
* Prohibit raw `FromSqlRaw` with un-parameterized string concatenations.
* `TG-DB-004`: Configure Global Query Filters (`HasQueryFilter(e => e.TenantId == _currentTenant)`) for multi-tenant safety.

### 3. Anti-Forgery & TLS
* `TG-CSRF-001`: Ensure `[ValidateAntiForgeryToken]` or `[AutoValidateAntiforgeryToken]` is applied to POST/PUT/DELETE actions.
* Prohibit `DangerousAcceptAnyServerCertificateValidator`.

---

## 🛠️ Safe Patterns Summary

```csharp
// Safe Entity Framework Parameterized Query
var user = await context.Users
    .Where(u => u.Id == userId && u.TenantId == currentTenantId)
    .FirstOrDefaultAsync();

// Safe Global Query Filter in DbContext
modelBuilder.Entity<Invoice>()
    .HasQueryFilter(i => i.TenantId == _tenantProvider.GetTenantId());

// Safe Controller Security
[Authorize]
[ApiController]
[Route("api/[controller]")]
public class InvoicesController : ControllerBase { ... }
```
