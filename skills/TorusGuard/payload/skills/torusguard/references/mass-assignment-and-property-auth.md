# Mass Assignment and Property Authorization

- Explicit writable-field allowlists.
- DTOs or request schemas.
- Separate user-editable and server-managed fields.
- Server-side assignment for role, balance, status, ownership, and verification.
- Authorization checks for sensitive individual properties.
- Tests that submit unexpected fields.

## Unsafe
```javascript
await User.update(req.body, { where: { id: req.user.id } });
```

## Safe
```javascript
const input = updateProfileSchema.parse(req.body);
await User.update(
  { displayName: input.displayName, avatarUrl: input.avatarUrl },
  { where: { id: req.user.id } }
);
```
