# Changelog

All notable changes to TorusGuard are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-08-19

### Added
- *Note: TorusGuard is an agent-guidance framework, not a complete automated scanner. Manual review is required for complex logic vulnerabilities.*
- Added SSRF and outbound-request security rules under `rules/`.
- Added business-logic abuse and sensitive-flow review.
- Added mass-assignment and property-level authorization rules.
- Added CSRF and credentialed cross-origin request guidance.
- Added webhook signature, replay, and idempotency rules.
- Added GraphQL security guidance for depth, complexity, batching, and resolver authorization.
- Added WebSocket authentication, channel authorization, and message validation rules.
- Added dependency and CI/CD supply-chain guidance.
- Added cache and sensitive-response protection rules.
- Added advanced API examples and review templates.

### Changed
- Expanded `/torusguard audit` to detect API styles and advanced resource-consumption risks.
- Expanded `/torusguard verify` with advanced API and integration checks.
- Preserved all v0.2 rule IDs for compatibility.

### Security
- Added SSRF network-boundary and outbound-request review.
- Added business-flow and replay-abuse analysis.

## [0.2.0] - 2026-08-18

### Added
- Stable TorusGuard rule IDs across secrets, database exposure, input handling, authentication, abuse prevention, client exposure, and platform hardening.
- 25 documented security rules under `rules/`.
- Standardized audit report, security context, threat model, deployment pre-flight, endpoint review, and security exception templates.
- Vulnerable and hardened React + Express reference examples.
- Security implementation guides for React/Vite, Next.js, Express, Supabase, and Firebase.
- `/TorusGuard verify` production pre-flight workflow.

### Changed
- Expanded `/TorusGuard audit` with rule IDs, severity, confidence, evidence, verification steps, and manual-review sections.
- Expanded `/TorusGuard harden` to require audit-first remediation and post-fix verification.
- Improved skill references with framework-aware safe defaults and hard bans.

### Security
- Clarified that browser-delivered code is public and that DevTools cannot be blocked.
- Strengthened server-side requirements for authorization, database access, validation, rate limiting, and production configuration.

### Removed
- npm package infrastructure (`package.json`, validation scripts) — TorusGuard remains documentation-driven

## [0.1.0] - 2026-08-18

### Added
- Initial rules and references.
