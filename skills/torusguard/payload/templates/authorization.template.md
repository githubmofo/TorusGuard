# TorusGuard Target Authorization Record

**Authorization ID:** `{{authorization_id}}`  
**Generated At:** `{{timestamp}}`  
**Valid Until:** `{{valid_until}}`  

---

## 1. Target Identification
- **Project / Application:** `{{target_name}}`
- **Target URL / Hosts:** `{{target_hosts}}`
- **Scope Type:** `{{scope_type}}`

---

## 2. Permitted Boundaries
- **Allowed Path Prefixes:**
{{allowed_path_prefixes_list}}

- **Explicitly Forbidden / Excluded Paths:**
{{forbidden_paths_list}}

- **Max Navigation Depth:** `{{max_depth}}`
- **Max Request Budget:** `{{max_requests}}`
- **Allow State-Changing Methods:** `{{allow_state_changing_methods}}`

---

## 3. Owner Confirmation & Legal Statement
> [!IMPORTANT]
> The target application owner has confirmed that this testing environment is authorized for non-destructive, bounded runtime security validation.

- **Authorized By:** `{{authorized_by}}`
- **Confirmation Status:** `Owner Confirmed`
