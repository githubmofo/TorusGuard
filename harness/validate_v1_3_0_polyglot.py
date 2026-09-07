#!/usr/bin/env python3
"""
TorusGuard v1.3.0 Universal Polyglot Security Engine Test Suite
Validates:
1. Universal Stack Detection across 10+ language & framework ecosystems:
   - Go (Gin + GORM)
   - Rust (Axum + Diesel)
   - Java (Spring Boot + Hibernate)
   - C# / .NET (ASP.NET Core + EF Core)
   - PHP (Laravel + Eloquent)
   - Ruby (Rails + ActiveRecord)
   - Kotlin (Ktor)
   - Elixir (Phoenix)
   - File extension census fallback (no manifest)
2. Polyglot Diff Guard bypass detection across:
   - Go (InsecureSkipVerify: true)
   - Java (csrf().disable())
   - C# ([AllowAnonymous])
   - PHP (CURLOPT_SSL_VERIFYPEER => false)
   - Rust (unsafe { ... })
3. Polyglot Tenant Scoping Patterns across GORM, LINQ, and Prisma
4. Stack-Adaptive AI IDE Rules Generation within token budget (<= 400 tokens)
5. Custom rules directory indexing
"""

import sys
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

# Ensure UTF-8 stdout/stderr on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / ".torusguard" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import stack_detect  # type: ignore
import diff_guard  # type: ignore
import rules_sync  # type: ignore


def test_v1_3_0_polyglot():
    print("=" * 80)
    print("TORUSGUARD v1.3.0 UNIVERSAL POLYGLOT ENGINE TEST SUITE")
    print("=" * 80)

    with tempfile.TemporaryDirectory() as tmp_dir:
        base_test = Path(tmp_dir).resolve()

        # ---------------------------------------------------------------------
        # 1. Universal Stack Detection: Multi-Language Manifests
        # ---------------------------------------------------------------------
        print("\n--- 1. Testing Universal Stack Detection (10 Ecosystems) ---")

        # 1A. Go (Gin + GORM)
        go_dir = base_test / "go_app"
        go_dir.mkdir()
        (go_dir / "go.mod").write_text(
            "module example.com/goapp\n\ngo 1.22\n\nrequire (\n\tgithub.com/gin-gonic/gin v1.9.1\n\tgorm.io/gorm v1.25.7\n)\n",
            encoding="utf-8"
        )
        stk_go = stack_detect.detect_stack(go_dir)
        assert stk_go["language"] == "Go", f"Expected Go, got {stk_go['language']}"
        assert stk_go["framework"] == "Gin", f"Expected Gin, got {stk_go['framework']}"
        assert stk_go["data_layer"] == "GORM", f"Expected GORM, got {stk_go['data_layer']}"
        assert stk_go["confidence"] == "Confirmed"
        print("  [PASS] Go ecosystem: Detected Go + Gin + GORM")

        # 1B. Rust (Axum + Diesel)
        rust_dir = base_test / "rust_app"
        rust_dir.mkdir()
        (rust_dir / "Cargo.toml").write_text(
            '[package]\nname = "rust_app"\nversion = "0.1.0"\n\n[dependencies]\naxum = "0.7"\ndiesel = "2.1"\n',
            encoding="utf-8"
        )
        stk_rust = stack_detect.detect_stack(rust_dir)
        assert stk_rust["language"] == "Rust", f"Expected Rust, got {stk_rust['language']}"
        assert stk_rust["framework"] == "Axum", f"Expected Axum, got {stk_rust['framework']}"
        assert stk_rust["data_layer"] == "Diesel ORM", f"Expected Diesel, got {stk_rust['data_layer']}"
        print("  [PASS] Rust ecosystem: Detected Rust + Axum + Diesel ORM")

        # 1C. Java (Spring Boot + Hibernate)
        java_dir = base_test / "java_app"
        java_dir.mkdir()
        (java_dir / "pom.xml").write_text(
            "<project>\n  <dependencies>\n    <dependency>\n      <groupId>org.springframework.boot</groupId>\n      <artifactId>spring-boot-starter-web</artifactId>\n    </dependency>\n    <dependency>\n      <groupId>org.hibernate.orm</groupId>\n      <artifactId>hibernate-core</artifactId>\n    </dependency>\n  </dependencies>\n</project>",
            encoding="utf-8"
        )
        stk_java = stack_detect.detect_stack(java_dir)
        assert stk_java["language"] == "Java", f"Expected Java, got {stk_java['language']}"
        assert stk_java["framework"] == "Spring Boot", f"Expected Spring Boot, got {stk_java['framework']}"
        assert "Hibernate" in stk_java["data_layer"], f"Expected Hibernate, got {stk_java['data_layer']}"
        print("  [PASS] Java ecosystem: Detected Java + Spring Boot + Hibernate")

        # 1D. C# / .NET (ASP.NET Core + EF Core)
        dotnet_dir = base_test / "dotnet_app"
        dotnet_dir.mkdir()
        (dotnet_dir / "Backend.csproj").write_text(
            '<Project Sdk="Microsoft.NET.Sdk.Web">\n  <ItemGroup>\n    <PackageReference Include="Microsoft.EntityFrameworkCore" Version="8.0.0" />\n  </ItemGroup>\n</Project>',
            encoding="utf-8"
        )
        stk_dotnet = stack_detect.detect_stack(dotnet_dir)
        assert stk_dotnet["language"] == "C#", f"Expected C#, got {stk_dotnet['language']}"
        assert stk_dotnet["framework"] == "ASP.NET Core", f"Expected ASP.NET Core, got {stk_dotnet['framework']}"
        assert "Entity Framework" in stk_dotnet["data_layer"], f"Expected EF Core, got {stk_dotnet['data_layer']}"
        print("  [PASS] C# / .NET ecosystem: Detected C# + ASP.NET Core + Entity Framework Core")

        # 1E. PHP (Laravel + Eloquent)
        php_dir = base_test / "php_app"
        php_dir.mkdir()
        (php_dir / "composer.json").write_text(
            json.dumps({"require": {"laravel/framework": "^11.0"}}, indent=2),
            encoding="utf-8"
        )
        stk_php = stack_detect.detect_stack(php_dir)
        assert stk_php["language"] == "PHP", f"Expected PHP, got {stk_php['language']}"
        assert stk_php["framework"] == "Laravel", f"Expected Laravel, got {stk_php['framework']}"
        assert stk_php["data_layer"] == "Eloquent ORM"
        print("  [PASS] PHP ecosystem: Detected PHP + Laravel + Eloquent ORM")

        # 1F. Ruby (Rails + ActiveRecord)
        ruby_dir = base_test / "ruby_app"
        ruby_dir.mkdir()
        (ruby_dir / "Gemfile").write_text("source 'https://rubygems.org'\ngem 'rails', '~> 7.1'\n", encoding="utf-8")
        stk_ruby = stack_detect.detect_stack(ruby_dir)
        assert stk_ruby["language"] == "Ruby", f"Expected Ruby, got {stk_ruby['language']}"
        assert stk_ruby["framework"] == "Ruby on Rails"
        assert stk_ruby["data_layer"] == "ActiveRecord"
        print("  [PASS] Ruby ecosystem: Detected Ruby + Ruby on Rails + ActiveRecord")

        # 1G. Kotlin (Ktor)
        kt_dir = base_test / "kt_app"
        kt_dir.mkdir()
        (kt_dir / "build.gradle.kts").write_text('plugins { kotlin("jvm") }\ndependencies { implementation("io.ktor:ktor-server-core:2.3.0") }', encoding="utf-8")
        stk_kt = stack_detect.detect_stack(kt_dir)
        assert stk_kt["language"] == "Kotlin"
        assert stk_kt["framework"] == "Ktor"
        print("  [PASS] Kotlin ecosystem: Detected Kotlin + Ktor")

        # 1H. Elixir (Phoenix)
        ex_dir = base_test / "ex_app"
        ex_dir.mkdir()
        (ex_dir / "mix.exs").write_text('defmodule App.MixProject do\n  defp deps do\n    [{:phoenix, "~> 1.7"}]\n  end\nend', encoding="utf-8")
        stk_ex = stack_detect.detect_stack(ex_dir)
        assert stk_ex["language"] == "Elixir"
        assert stk_ex["framework"] == "Phoenix"
        assert stk_ex["data_layer"] == "Ecto"
        print("  [PASS] Elixir ecosystem: Detected Elixir + Phoenix + Ecto")

        # 1I. Extension Census Fallback (Repository with no manifests)
        census_dir = base_test / "census_app"
        census_dir.mkdir()
        (census_dir / "main.go").write_text("package main\nfunc main() {}\n", encoding="utf-8")
        (census_dir / "server.go").write_text("package main\n", encoding="utf-8")
        (census_dir / "util.go").write_text("package main\n", encoding="utf-8")
        stk_census = stack_detect.detect_stack(census_dir)
        assert stk_census["language"] == "Go", f"Expected Go from census, got {stk_census['language']}"
        assert "census" in stk_census["confidence"].lower()
        print("  [PASS] Extension Census Fallback: Correctly inferred Go from 3 .go files")

        # ---------------------------------------------------------------------
        # 2. Polyglot Diff Guard: Cross-Language Bypass Detection
        # ---------------------------------------------------------------------
        print("\n--- 2. Testing Polyglot Diff Guard Bypass Detection ---")

        # Go InsecureSkipVerify bypass
        diff_go = """--- a/client.go
+++ b/client.go
@@ -10,3 +10,4 @@
+	tr := &http.Transport{TLSClientConfig: &tls.Config{InsecureSkipVerify: true}}
"""
        viol_go = diff_guard.check_diff_content(diff_go, "client.go")
        assert len(viol_go) >= 1, "Failed to catch Go InsecureSkipVerify"
        assert any("InsecureSkipVerify" in v["description"] for v in viol_go)
        print("  [PASS] Caught Go InsecureSkipVerify bypass")

        # Java CSRF disable bypass
        diff_java = """--- a/SecurityConfig.java
+++ b/SecurityConfig.java
@@ -20,3 +20,4 @@
+    http.csrf().disable();
"""
        viol_java = diff_guard.check_diff_content(diff_java, "SecurityConfig.java")
        assert len(viol_java) >= 1, "Failed to catch Java csrf().disable()"
        assert any("CSRF" in v["description"] for v in viol_java)
        print("  [PASS] Caught Java Spring Security csrf().disable() bypass")

        # C# AllowAnonymous bypass
        diff_cs = """--- a/UsersController.cs
+++ b/UsersController.cs
@@ -15,3 +15,4 @@
+    [AllowAnonymous]
+    public IActionResult GetFinancialData() {
"""
        viol_cs = diff_guard.check_diff_content(diff_cs, "UsersController.cs")
        assert len(viol_cs) >= 1, "Failed to catch C# [AllowAnonymous]"
        print("  [PASS] Caught C# ASP.NET [AllowAnonymous] bypass")

        # PHP CURLOPT_SSL_VERIFYPEER bypass
        diff_php = """--- a/api.php
+++ b/api.php
@@ -5,3 +5,4 @@
+    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
"""
        viol_php = diff_guard.check_diff_content(diff_php, "api.php")
        assert len(viol_php) >= 1, "Failed to catch PHP CURLOPT_SSL_VERIFYPEER false"
        print("  [PASS] Caught PHP CURLOPT_SSL_VERIFYPEER bypass")

        # Rust unsafe block bypass
        diff_rs = """--- a/lib.rs
+++ b/lib.rs
@@ -10,3 +10,5 @@
+    unsafe {
+        let ptr = 0x1234 as *mut u8;
+    }
"""
        viol_rs = diff_guard.check_diff_content(diff_rs, "lib.rs")
        assert len(viol_rs) >= 1, "Failed to catch Rust unsafe block"
        print("  [PASS] Caught Rust unvetted unsafe block")

        # ---------------------------------------------------------------------
        # 3. Polyglot Tenant Scoping Patterns
        # ---------------------------------------------------------------------
        print("\n--- 3. Testing Polyglot Tenant Scoping Patterns ---")
        gorm_line = 'db.Where("tenant_id = ?", tid).Find(&users)'
        linq_line = "var users = ctx.Users.Where(x => x.TenantId == tid);"
        prisma_line = "const users = await prisma.user.findMany({ where: { tenantId } });"

        assert any(p.search(gorm_line) for p in diff_guard.TENANT_FILTER_PATTERNS), "GORM tenant pattern not matched"
        assert any(p.search(linq_line) for p in diff_guard.TENANT_FILTER_PATTERNS), "LINQ tenant pattern not matched"
        assert any(p.search(prisma_line) for p in diff_guard.TENANT_FILTER_PATTERNS), "Prisma tenant pattern not matched"
        print("  [PASS] Polyglot tenant patterns recognized (GORM, LINQ, Prisma)")

        # ---------------------------------------------------------------------
        # 4. Stack-Adaptive AI IDE Rules Generation
        # ---------------------------------------------------------------------
        print("\n--- 4. Testing Stack-Adaptive AI IDE Rules Generation ---")

        # Go rules sync
        sec_data_go = {"profile": {"stack": ["Go", "Gin"]}, "patterns": []}
        rules_go = rules_sync.format_dense_security_rules(sec_data_go)
        assert "InsecureSkipVerify" in rules_go, "Go bypass invariant missing from rules"
        assert "db.Query" in rules_go, "Go parameterized query invariant missing"
        tokens_go = max(1, len(rules_go) // 4)
        assert tokens_go <= 400, f"Token budget exceeded: {tokens_go} > 400"
        print(f"  [PASS] Go stack-adaptive rules verified (~{tokens_go} tokens <= 400)")

        # Rust rules sync
        sec_data_rust = {"profile": {"stack": ["Rust", "Axum"]}, "patterns": []}
        rules_rust = rules_sync.format_dense_security_rules(sec_data_rust)
        assert "sqlx::query!" in rules_rust, "Rust query invariant missing"
        assert "unsafe" in rules_rust, "Rust unsafe invariant missing"
        tokens_rust = max(1, len(rules_rust) // 4)
        assert tokens_rust <= 400
        print(f"  [PASS] Rust stack-adaptive rules verified (~{tokens_rust} tokens <= 400)")

        # Java rules sync
        sec_data_java = {"profile": {"stack": ["Java", "Spring Boot"]}, "patterns": []}
        rules_java = rules_sync.format_dense_security_rules(sec_data_java)
        assert "csrf().disable()" in rules_java, "Java CSRF invariant missing"
        tokens_java = max(1, len(rules_java) // 4)
        assert tokens_java <= 400
        print(f"  [PASS] Java stack-adaptive rules verified (~{tokens_java} tokens <= 400)")

        # ---------------------------------------------------------------------
        # 5. Custom Rules Directory Scaffolding
        # ---------------------------------------------------------------------
        print("\n--- 5. Testing Custom Rules Scaffolding ---")
        custom_dir = ROOT_DIR / ".torusguard" / "rules" / "custom"
        assert custom_dir.is_dir(), "Missing .torusguard/rules/custom/ directory"
        assert (custom_dir / "README.md").is_file(), "Missing custom rules README.md"
        assert (custom_dir / ".gitkeep").is_file(), "Missing custom rules .gitkeep"
        print("  [PASS] Custom rules directory and documentation confirmed")

    print("\n" + "=" * 80)
    print("ALL v1.3.0 POLYGLOT CHECKS PASSED (100% REGRESSION-FREE)")
    print("=" * 80)


if __name__ == "__main__":
    test_v1_3_0_polyglot()
