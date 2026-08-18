# Threat Model - [PROJECT_NAME]

## System overview
- **System name:** [PROJECT_NAME]
- **Business purpose:** [SYSTEM_PURPOSE]
- **Architecture summary:** [ARCHITECTURE_SUMMARY]
- **Primary components:** [PRIMARY_COMPONENTS]
- **Data flow summary:** [DATA_FLOW_SUMMARY]

## Assets to protect
- **User identity data:** [IDENTITY_DATA_ASSETS]
- **Sensitive business data:** [BUSINESS_DATA_ASSETS]
- **Credentials/secrets/keys:** [SECRETS_AND_KEYS]
- **Operational integrity assets:** [OPERATIONAL_ASSETS]
- **Availability-critical services:** [AVAILABILITY_CRITICAL_ASSETS]

## Actors and attacker goals
- **Legitimate actors:** [LEGITIMATE_ACTORS]
- **External attacker goals:** [EXTERNAL_ATTACKER_GOALS]
- **Insider threat goals:** [INSIDER_THREAT_GOALS]
- **Automated abuse goals:** [AUTOMATED_ABUSE_GOALS]

## Trust boundaries
- **Client boundary:** [CLIENT_TRUST_BOUNDARY]
- **Perimeter/edge boundary:** [EDGE_TRUST_BOUNDARY]
- **Application boundary:** [APPLICATION_TRUST_BOUNDARY]
- **Data storage boundary:** [DATASTORE_TRUST_BOUNDARY]
- **Third-party boundary:** [THIRD_PARTY_TRUST_BOUNDARY]

## Entry points
- **Public HTTP endpoints:** [PUBLIC_HTTP_ENTRY_POINTS]
- **Authentication endpoints:** [AUTH_ENTRY_POINTS]
- **Admin/ops interfaces:** [ADMIN_ENTRY_POINTS]
- **Background job/event inputs:** [ASYNC_ENTRY_POINTS]
- **Third-party callbacks/webhooks:** [WEBHOOK_ENTRY_POINTS]

## Threat scenarios
| Scenario ID | Threat description | Affected assets | Attack path | Likelihood | Impact | Risk level |
|---|---|---|---|---|---|---|
| [SCENARIO_ID_01] | [THREAT_DESCRIPTION_01] | [AFFECTED_ASSETS_01] | [ATTACK_PATH_01] | [LIKELIHOOD_01] | [IMPACT_01] | [RISK_LEVEL_01] |
| [SCENARIO_ID_02] | [THREAT_DESCRIPTION_02] | [AFFECTED_ASSETS_02] | [ATTACK_PATH_02] | [LIKELIHOOD_02] | [IMPACT_02] | [RISK_LEVEL_02] |
| [SCENARIO_ID_03] | [THREAT_DESCRIPTION_03] | [AFFECTED_ASSETS_03] | [ATTACK_PATH_03] | [LIKELIHOOD_03] | [IMPACT_03] | [RISK_LEVEL_03] |

## Existing controls
- **Preventive controls:** [PREVENTIVE_CONTROLS]
- **Detective controls:** [DETECTIVE_CONTROLS]
- **Corrective controls:** [CORRECTIVE_CONTROLS]
- **Recovery controls:** [RECOVERY_CONTROLS]

## Residual risks
- **High residual risks:** [HIGH_RESIDUAL_RISKS]
- **Medium residual risks:** [MEDIUM_RESIDUAL_RISKS]
- **Accepted residual risks:** [ACCEPTED_RESIDUAL_RISKS]
- **Risk owners:** [RESIDUAL_RISK_OWNERS]

## Required follow-ups
- **Immediate actions (0-7 days):** [IMMEDIATE_ACTIONS]
- **Near-term actions (8-30 days):** [NEAR_TERM_ACTIONS]
- **Quarterly actions (31-90 days):** [QUARTERLY_ACTIONS]
- **Tracking ticket references:** [TRACKING_TICKETS]
- **Next model review date:** [NEXT_THREAT_MODEL_REVIEW_DATE]
