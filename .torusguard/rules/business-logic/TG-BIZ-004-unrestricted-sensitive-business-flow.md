# TG-BIZ-004: Unrestricted Sensitive Business Flow

## Severity
High. Critical administrative or high-impact actions lacking step-up authentication, secondary confirmation, or multi-person governance allow compromised sessions to inflict irreversible damage.

## Applies To
- Tenant Deletion, Role Escalation, API Key Rotation, Wire Transfers
- Node.js, Python, Go, Java, C#

## Why It Matters
Session hijacking, CSRF, or brief workstation abandonment can allow attackers to execute destructive operations (such as purging an entire organization's database or transferring company funds) if the flow executes immediately on a single unconfirmed click.

## What TorusGuard Looks For
- Destructive administrative endpoints (`/delete-organization`, `/transfer-ownership`) executing without recent password re-authentication, MFA step-up verification, or explicit confirmation tokens.

## Unsafe Example
```javascript
// UNSAFE: Destructive deletion executing without password re-verification
app.delete('/api/orgs/:id', authMiddleware, async (req, res) => {
  await db.org.delete({ where: { id: req.params.id } });
  res.json({ success: true });
});
```

## Safe Example
```javascript
// SAFE: Requiring password re-authentication before executing destructive action
app.delete('/api/orgs/:id', authMiddleware, async (req, res) => {
  const { confirmPassword } = req.body;
  const isValid = await verifyPassword(req.user.id, confirmPassword);
  if (!isValid) return res.status(403).json({ error: 'Invalid password confirmation' });
  await db.org.delete({ where: { id: req.params.id } });
  res.json({ success: true });
});
```

## Ponytail Remediation Budget
- Additions: <= 12 lines
- Deletions: <= 2 lines

## Remediation
1. Enforce step-up authentication (password re-prompt or TOTP code) on high-risk endpoints.
2. Implement two-stage confirmation (`DELETE` requires prior confirmation token).

## Related Rules
- `TG-AUTH-002`: Client-Only Authorization
- `TG-RATE-003`: Unbounded Resource Consumption
