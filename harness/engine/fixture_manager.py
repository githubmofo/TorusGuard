"""
TorusGuard Fixture Manager (v0.5.2)
Loads, indexes, and validates structured fixture definitions and paired differential targets.
"""

from pathlib import Path
from typing import List, Dict, Optional
from .models import FixtureDefinition, FixtureVariant, ValidationOutcome


class FixtureManager:
    """
    Manages the catalog of validation fixtures, paired differential applications, and regression test suites.
    """

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()
        self.fixtures: Dict[str, FixtureDefinition] = {}
        self._load_standard_fixtures()

    def _load_standard_fixtures(self):
        # 1. Django Reference Pair
        self.register_fixture(
            FixtureDefinition(
                fixture_id="TG-FIX-django-idor-scoping",
                framework="django",
                scenario="Django ViewSet object-level authorization & settings DEBUG exposure",
                target_rule_id="TG-AUTH-007",
                expected_outcome=ValidationOutcome.VULNERABLE_CONFIRMED,
                vulnerable_variant=FixtureVariant(
                    relative_path="examples/python/django-vuln",
                    code_pattern="Invoice.objects.all()",
                    expected_findings_count=6,
                ),
                hardened_variant=FixtureVariant(
                    relative_path="examples/python/django-hardened",
                    code_pattern="Invoice.objects.filter(owner=request.user)",
                    expected_findings_count=0,
                    is_hardened=True,
                ),
                reproduction_command="python manage.py test",
                expected_diff_summary="DEBUG set to False; ALLOWED_HOSTS populated; get_queryset scoped to request.user.",
            )
        )

        # 2. DRF Reference Pair
        self.register_fixture(
            FixtureDefinition(
                fixture_id="TG-FIX-drf-mass-assignment-throttle",
                framework="drf",
                scenario="DRF Serializer field protection, rate throttling, and pagination caps",
                target_rule_id="TG-AUTH-006",
                expected_outcome=ValidationOutcome.VULNERABLE_CONFIRMED,
                vulnerable_variant=FixtureVariant(
                    relative_path="examples/python/drf-vuln",
                    code_pattern="fields = '__all__'",
                    expected_findings_count=5,
                ),
                hardened_variant=FixtureVariant(
                    relative_path="examples/python/drf-hardened",
                    code_pattern="read_only_fields = ('role', 'is_staff')",
                    expected_findings_count=0,
                    is_hardened=True,
                ),
                reproduction_command="pytest",
                expected_diff_summary="read_only_fields explicit; ScopedRateThrottle attached; max_page_size set.",
            )
        )

        # 3. FastAPI Reference Pair
        self.register_fixture(
            FixtureDefinition(
                fixture_id="TG-FIX-fastapi-ssrf-pydantic",
                framework="fastapi",
                scenario="FastAPI outbound SSRF URL validation and Pydantic v2 extra field forbidding",
                target_rule_id="TG-SSRF-001",
                expected_outcome=ValidationOutcome.VULNERABLE_CONFIRMED,
                vulnerable_variant=FixtureVariant(
                    relative_path="examples/python/fastapi-vuln",
                    code_pattern="httpx.get(target_url)",
                    expected_findings_count=5,
                ),
                hardened_variant=FixtureVariant(
                    relative_path="examples/python/fastapi-hardened",
                    code_pattern="validate_outbound_destination(url)",
                    expected_findings_count=0,
                    is_hardened=True,
                ),
                reproduction_command="pytest",
                expected_diff_summary="IP destination validation filtering RFC 1918 blocks; Pydantic extra='forbid'.",
            )
        )

        # 4. Flask Reference Pair
        self.register_fixture(
            FixtureDefinition(
                fixture_id="TG-FIX-flask-csrf-upload",
                framework="flask",
                scenario="Flask CSRFProtect, secure cookie flags, and upload filename sanitization",
                target_rule_id="TG-CSRF-001",
                expected_outcome=ValidationOutcome.VULNERABLE_CONFIRMED,
                vulnerable_variant=FixtureVariant(
                    relative_path="examples/python/flask-vuln",
                    code_pattern="file.save(os.path.join(UPLOAD_DIR, file.filename))",
                    expected_findings_count=5,
                ),
                hardened_variant=FixtureVariant(
                    relative_path="examples/python/flask-hardened",
                    code_pattern="secure_filename(file.filename)",
                    expected_findings_count=0,
                    is_hardened=True,
                ),
                reproduction_command="pytest",
                expected_diff_summary="CSRFProtect(app) enabled; SESSION_COOKIE_SECURE=True; secure_filename with UUID prefix.",
            )
        )

        # 5. SQLAlchemy Reference Pair
        self.register_fixture(
            FixtureDefinition(
                fixture_id="TG-FIX-sqlalchemy-bound-parameters",
                framework="sqlalchemy",
                scenario="SQLAlchemy named text(:param) bindings and tenant query scoping",
                target_rule_id="TG-INPUT-002",
                expected_outcome=ValidationOutcome.VULNERABLE_CONFIRMED,
                vulnerable_variant=FixtureVariant(
                    relative_path="examples/python/sqlalchemy-vuln",
                    code_pattern="session.execute(f'SELECT * FROM items WHERE name LIKE {q}')",
                    expected_findings_count=4,
                ),
                hardened_variant=FixtureVariant(
                    relative_path="examples/python/sqlalchemy-hardened",
                    code_pattern="session.execute(text('SELECT * FROM items WHERE name LIKE :q'), {'q': f'%{q}%'})",
                    expected_findings_count=0,
                    is_hardened=True,
                ),
                reproduction_command="pytest",
                expected_diff_summary="Parameterized text(:param) queries; tenant_id enforced on query filters.",
            )
        )

    def register_fixture(self, fixture: FixtureDefinition):
        self.fixtures[fixture.fixture_id] = fixture

    def get_fixture(self, fixture_id: str) -> Optional[FixtureDefinition]:
        return self.fixtures.get(fixture_id)

    def list_fixtures(self) -> List[FixtureDefinition]:
        return list(self.fixtures.values())
