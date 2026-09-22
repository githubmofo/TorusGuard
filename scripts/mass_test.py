import os
import shutil
import subprocess
import time

TEST_DIR = "test_repos"
ROOT_DIR = os.getcwd()
TG_BIN = os.path.join(ROOT_DIR, "torusguard.exe")
COMPILED_CATALOG = os.path.join(ROOT_DIR, ".torusguard", "rules_catalog.json")
REPORT_PATH = r"C:\Users\Admin\.gemini\antigravity-ide\brain\7fd5bfc4-a05b-4357-8adb-c099e2d5b900\mass_test_report.md"

REPOS = [
    {"name": "react-frontend", "file": "src/App.js", "content": 'const API_KEY = "sk" + "_live_1234567890abcdef1234567890";'},
    {"name": "nextjs-app", "file": "pages/api/auth.ts", "content": 'const jwtSecret = "super_secret_dont_share";'},
    {"name": "express-backend", "file": "index.js", "content": 'app.disable("x-powered-by");\nchild_process.exec(req.query.cmd);'},
    {"name": "django-app", "file": "settings.py", "content": 'SECRET_KEY = "django-insecure-32&*(#JH@!*&SDF"'},
    {"name": "flask-api", "file": "app.py", "content": 'db.execute(f"SELECT * FROM users WHERE id = {user_id}")'},
    {"name": "fastapi-service", "file": "main.py", "content": 'import os\nAPI_TOKEN="1234567890abcdef"'},
    {"name": "go-gin", "file": "main.go", "content": 'db.Query("SELECT * FROM table WHERE id=" + req.URL.Query().Get("id"))'},
    {"name": "java-spring", "file": "src/main/java/App.java", "content": 'String query = "SELECT * FROM users WHERE user = " + input;'},
    {"name": "ruby-on-rails", "file": "config/secrets.yml", "content": 'production:\n  secret_key_base: "1a2b3c4d5e6f7a8b9c0d"'},
    {"name": "php-laravel", "file": ".env", "content": 'APP_KEY=base64:VGVzdEtleTEyMzQ1Njc4OTA=\nDB_PASSWORD="root"'},
    {"name": "csharp-aspnet", "file": "Controllers/HomeController.cs", "content": 'SqlCommand cmd = new SqlCommand("SELECT * FROM Users WHERE Name = \'" + name + "\'");'},
    {"name": "rust-actix", "file": "src/main.rs", "content": 'let secret = "super_secret_key_123456";'},
    {"name": "vue-app", "file": "src/components/Login.vue", "content": '<script>\nconst password="admin";\n</script>'},
    {"name": "sveltekit", "file": "src/routes/+page.svelte", "content": 'let token = "eyJhbGciOi" + "JIUzI1NiIsInR5cCI6IkpXVCJ9";'},
    {"name": "angular-app", "file": "src/app/app.component.ts", "content": 'apiKey = "AIzaSy" + "B-1234567890abcdefGHIJKLMNOP";'},
    {"name": "nestjs-api", "file": "src/app.controller.ts", "content": 'jwt.sign(payload, "hardcoded_secret");'},
    {"name": "ruby-sinatra", "file": "app.rb", "content": 'system("ping " + params[:ip])'},
    {"name": "dotnet-core", "file": "Startup.cs", "content": 'app.UseCors(builder => builder.AllowAnyOrigin().AllowCredentials());'},
    {"name": "php-symfony", "file": "config/packages/security.yaml", "content": 'firewalls:\n  main:\n    secret: "change_me_later"'},
    {"name": "python-script", "file": "script.py", "content": 'eval(sys.argv[1])'},
]

def main():
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)

    report_lines = [
        "# TorusGuard Mass Testing Report",
        "",
        "| Repository | Tech Stack | Init Status | Audit Status | Output |",
        "|------------|------------|-------------|--------------|--------|"
    ]

    for repo in REPOS:
        repo_path = os.path.join(TEST_DIR, repo["name"])
        os.makedirs(repo_path)
        
        # Write dummy file
        file_path = os.path.join(repo_path, repo["file"])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(repo["content"])

        print(f"Testing {repo['name']}...")
        
        # Init
        init_res = subprocess.run([TG_BIN, "init"], cwd=repo_path, capture_output=True, text=True)
        init_status = "✅" if init_res.returncode == 0 else "❌"

        # Copy rules_catalog.json
        tg_dir = os.path.join(repo_path, ".torusguard")
        if not os.path.exists(tg_dir):
            os.makedirs(tg_dir)
        shutil.copy(COMPILED_CATALOG, os.path.join(tg_dir, "rules_catalog.json"))

        # Audit
        audit_res = subprocess.run([TG_BIN, "audit"], cwd=repo_path, capture_output=True, text=True)
        audit_status = "✅" if audit_res.returncode == 0 else "❌"
        
        out_summary = audit_res.stdout.strip().replace("\n", "<br>")
        if "Loaded 0 rules" in out_summary:
            out_summary = "Failed to load rules"
        elif "Scan complete" in out_summary:
            out_summary = "Scan completed successfully"
        
        report_lines.append(f"| {repo['name']} | Mixed | {init_status} | {audit_status} | {out_summary} |")

    # Write report
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"\nReport generated at {REPORT_PATH}")
    
    # Cleanup as requested
    print("Cleaning up test repositories...")
    shutil.rmtree(TEST_DIR)
    print("Cleanup complete.")

if __name__ == "__main__":
    main()
