"""
TorusGuard v6.2 Modern Stack Profiler & Version Family Detector
Analyzes project manifests, code syntax, and dependency configurations to detect
framework version families (Django 5.x/4.x, FastAPI/Pydantic v2, SQLAlchemy 2.0, Next.js 14+),
async paradigms, container/workflow setups, and modern configuration patterns.
"""

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
import re
import json


@dataclass
class StackProfile:
    primary_language: str = "Python"
    framework: str = "Unknown"
    version_family: str = "Modern"
    is_async: bool = False
    orm_layer: str = "None"
    orm_version_family: str = "2.0+"
    config_loader: str = "Standard"
    dependency_manager: str = "pip"
    container_engine: Optional[str] = None
    ci_platform: Optional[str] = None
    frontend_framework: Optional[str] = None
    detected_features: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class StackProfiler:
    """
    Inspects repository files to determine comprehensive modern stack profile.
    """

    @classmethod
    def profile_repository(cls, repo_path: Path) -> StackProfile:
        profile = StackProfile()
        detected_features = []

        if not repo_path.exists():
            return profile

        # Collect files
        all_files: List[Path] = []
        try:
            for p in repo_path.rglob("*"):
                if p.is_file() and not any(part.startswith(".") and part != ".github" for part in p.parts):
                    all_files.append(p)
        except Exception:
            pass

        file_names = {f.name for f in all_files}
        file_paths_str = [str(f.relative_to(repo_path)).replace("\\", "/") for f in all_files]

        # 1. Dependency Manager Detection
        if "uv.lock" in file_names:
            profile.dependency_manager = "uv"
            detected_features.append("uv (Astral) fast package manager")
        elif "poetry.lock" in file_names:
            profile.dependency_manager = "poetry"
            detected_features.append("Poetry packaging")
        elif "Pipfile.lock" in file_names:
            profile.dependency_manager = "pipenv"
        elif "pnpm-lock.yaml" in file_names:
            profile.dependency_manager = "pnpm"
        elif "package-lock.json" in file_names:
            profile.dependency_manager = "npm"
        elif "yarn.lock" in file_names:
            profile.dependency_manager = "yarn"
        elif "pyproject.toml" in file_names:
            profile.dependency_manager = "pyproject.toml (PEP 621)"

        # 2. Container & CI Platform
        if any("Dockerfile" in name or "Containerfile" in name for name in file_names):
            profile.container_engine = "Docker / OCI Container"
            detected_features.append("Containerized deployment (Dockerfile)")
        if any(p.startswith(".github/workflows/") for p in file_paths_str):
            profile.ci_platform = "GitHub Actions"
            detected_features.append("GitHub Actions CI/CD workflows")

        # 3. Source Code Inspection
        py_files = [f for f in all_files if f.suffix in [".py", ".pyi"]]
        ts_files = [f for f in all_files if f.suffix in [".ts", ".tsx", ".js", ".jsx"]]

        py_content_sample = ""
        for pf in py_files[:20]:
            try:
                py_content_sample += pf.read_text(encoding="utf-8", errors="ignore") + "\n"
            except Exception:
                pass

        ts_content_sample = ""
        for tf in ts_files[:20]:
            try:
                ts_content_sample += tf.read_text(encoding="utf-8", errors="ignore") + "\n"
            except Exception:
                pass

        # Check async paradigm
        if "async def " in py_content_sample or "await " in py_content_sample:
            profile.is_async = True
            detected_features.append("Async / Await Coroutines")

        # Framework & Version Family Detection
        if "from fastapi" in py_content_sample or "import fastapi" in py_content_sample:
            profile.framework = "FastAPI"
            if "Annotated[" in py_content_sample or "model_validator" in py_content_sample or "pydantic_settings" in py_content_sample:
                profile.version_family = "FastAPI 0.100+ (Pydantic v2)"
                detected_features.append("Pydantic v2 Typed Validation & Annotated Dependencies")
            else:
                profile.version_family = "FastAPI 0.9x (Legacy)"

        elif "django" in py_content_sample or "DJANGO_SETTINGS_MODULE" in py_content_sample:
            profile.framework = "Django"
            if "aget(" in py_content_sample or "asgiref" in py_content_sample or "async def " in py_content_sample:
                profile.version_family = "Django 5.x (Async Native)"
                detected_features.append("Django 5.x Async ORM & Views")
            else:
                profile.version_family = "Django 4.x / Standard"

        elif "from flask" in py_content_sample or "import flask" in py_content_sample:
            profile.framework = "Flask"
            profile.version_family = "Flask 3.x"

        # ORM Layer
        if "sqlalchemy" in py_content_sample:
            profile.orm_layer = "SQLAlchemy"
            if "select(" in py_content_sample or "AsyncSession" in py_content_sample or "mapped_column" in py_content_sample:
                profile.orm_version_family = "SQLAlchemy 2.0+ (Modern 2.0 Syntax)"
                detected_features.append("SQLAlchemy 2.0 select() queries & async sessions")
            else:
                profile.orm_version_family = "SQLAlchemy 1.4 (Legacy Query API)"
        elif profile.framework == "Django":
            profile.orm_layer = "Django ORM"
            profile.orm_version_family = "Django Model Manager"

        # Frontend Framework
        if '"next"' in ts_content_sample or "'next'" in ts_content_sample or "use server" in ts_content_sample:
            profile.frontend_framework = "Next.js 14+ (App Router)"
            detected_features.append("Next.js App Router & Server Actions")
        elif "react" in ts_content_sample:
            profile.frontend_framework = "React"

        # Configuration Loading
        if "pydantic_settings" in py_content_sample or "BaseSettings" in py_content_sample:
            profile.config_loader = "pydantic-settings (Type-Safe Env)"
            detected_features.append("pydantic-settings environment validation")
        elif "os.getenv" in py_content_sample or "os.environ" in py_content_sample:
            profile.config_loader = "os.environ"

        profile.detected_features = detected_features
        return profile
