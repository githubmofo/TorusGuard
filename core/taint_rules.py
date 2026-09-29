"""
TorusGuard Taint Engine — Polyglot Source, Sink, and Sanitizer Catalogs
Covers Python, JavaScript/TypeScript, Go, Rust, Java, Ruby, PHP, and C#.
"""

from typing import Dict, List, Any, Optional

TAINT_SOURCES: Dict[str, List[Dict[str, Any]]] = {
    "python": [
        {"pattern": "request.GET", "framework": "Django", "label": "HTTP Query Param", "category": "user_input"},
        {"pattern": "request.POST", "framework": "Django", "label": "HTTP POST Body", "category": "user_input"},
        {"pattern": "request.data", "framework": "DRF", "label": "DRF Request Data", "category": "user_input"},
        {"pattern": "request.query_params", "framework": "DRF", "label": "DRF Query Params", "category": "user_input"},
        {"pattern": "request.json", "framework": "Flask", "label": "Flask JSON Body", "category": "user_input"},
        {"pattern": "request.args", "framework": "Flask", "label": "Flask Query Param", "category": "user_input"},
        {"pattern": "request.form", "framework": "Flask", "label": "Flask Form Data", "category": "user_input"},
        {"pattern": "request.values", "framework": "Flask", "label": "Flask Form/Args Data", "category": "user_input"},
        {"pattern": "request.headers", "framework": "Flask/Django", "label": "HTTP Headers", "category": "header"},
        {"pattern": "sys.argv", "framework": "stdlib", "label": "CLI Argument", "category": "cli"},
        {"pattern": "os.environ", "framework": "stdlib", "label": "Environment Variable", "category": "env"},
        {"pattern": "os.getenv", "framework": "stdlib", "label": "Environment Variable", "category": "env"},
        {"pattern": "input(", "framework": "stdlib", "label": "User Console Input", "category": "user_input"},
        {"pattern": "Body(", "framework": "FastAPI", "label": "FastAPI Body Param", "category": "user_input"},
        {"pattern": "Query(", "framework": "FastAPI", "label": "FastAPI Query Param", "category": "user_input"},
        {"pattern": "Header(", "framework": "FastAPI", "label": "FastAPI Header Param", "category": "header"},
        {"pattern": "Path(", "framework": "FastAPI", "label": "FastAPI Path Param", "category": "user_input"},
    ],
    "javascript": [
        {"pattern": "req.body", "framework": "Express", "label": "Express Request Body", "category": "user_input"},
        {"pattern": "req.query", "framework": "Express", "label": "Express Query Params", "category": "user_input"},
        {"pattern": "req.params", "framework": "Express", "label": "Express Route Params", "category": "user_input"},
        {"pattern": "req.headers", "framework": "Express", "label": "Express Headers", "category": "header"},
        {"pattern": "request.json()", "framework": "Next.js", "label": "Next.js Request JSON", "category": "user_input"},
        {"pattern": "request.formData()", "framework": "Next.js", "label": "Next.js FormData", "category": "user_input"},
        {"pattern": "formData", "framework": "Next.js", "label": "Server Action FormData", "category": "user_input"},
        {"pattern": "cookies()", "framework": "Next.js", "label": "Next.js Cookies", "category": "user_input"},
        {"pattern": "searchParams", "framework": "Web API", "label": "URL Search Params", "category": "user_input"},
        {"pattern": "event.body", "framework": "Lambda", "label": "AWS Lambda Event Body", "category": "user_input"},
        {"pattern": "event.queryStringParameters", "framework": "Lambda", "label": "Lambda Query Params", "category": "user_input"},
        {"pattern": "process.argv", "framework": "Node stdlib", "label": "CLI Arguments", "category": "cli"},
        {"pattern": "process.env", "framework": "Node stdlib", "label": "Environment Variables", "category": "env"},
        {"pattern": "location.search", "framework": "DOM", "label": "DOM Search Query", "category": "dom"},
        {"pattern": "location.hash", "framework": "DOM", "label": "DOM Hash Fragment", "category": "dom"},
        {"pattern": "window.name", "framework": "DOM", "label": "DOM Window Name", "category": "dom"},
    ],
    "go": [
        {"pattern": "r.URL.Query()", "framework": "net/http", "label": "HTTP Query Params", "category": "user_input"},
        {"pattern": "r.FormValue(", "framework": "net/http", "label": "HTTP Form Value", "category": "user_input"},
        {"pattern": "r.PostFormValue(", "framework": "net/http", "label": "HTTP Post Form Value", "category": "user_input"},
        {"pattern": "r.Body", "framework": "net/http", "label": "HTTP Request Body", "category": "user_input"},
        {"pattern": "r.Header.Get(", "framework": "net/http", "label": "HTTP Header", "category": "header"},
        {"pattern": "c.Param(", "framework": "Gin", "label": "Gin Route Param", "category": "user_input"},
        {"pattern": "c.Query(", "framework": "Gin", "label": "Gin Query Param", "category": "user_input"},
        {"pattern": "c.PostForm(", "framework": "Gin", "label": "Gin Form Param", "category": "user_input"},
        {"pattern": "c.BindJSON(", "framework": "Gin", "label": "Gin JSON Binding", "category": "user_input"},
        {"pattern": "os.Args", "framework": "stdlib", "label": "CLI Arguments", "category": "cli"},
        {"pattern": "os.Getenv(", "framework": "stdlib", "label": "Environment Variable", "category": "env"},
    ],
    "rust": [
        {"pattern": "web::Query", "framework": "actix-web", "label": "Actix Query Extractor", "category": "user_input"},
        {"pattern": "web::Json", "framework": "actix-web", "label": "Actix JSON Extractor", "category": "user_input"},
        {"pattern": "web::Path", "framework": "actix-web", "label": "Actix Path Extractor", "category": "user_input"},
        {"pattern": "axum::extract::Query", "framework": "axum", "label": "Axum Query Extractor", "category": "user_input"},
        {"pattern": "axum::extract::Json", "framework": "axum", "label": "Axum JSON Extractor", "category": "user_input"},
        {"pattern": "std::env::args", "framework": "stdlib", "label": "CLI Arguments", "category": "cli"},
        {"pattern": "std::env::var", "framework": "stdlib", "label": "Environment Variable", "category": "env"},
    ],
    "java": [
        {"pattern": "@RequestParam", "framework": "Spring", "label": "Spring Request Param", "category": "user_input"},
        {"pattern": "@RequestBody", "framework": "Spring", "label": "Spring Request Body", "category": "user_input"},
        {"pattern": "@PathVariable", "framework": "Spring", "label": "Spring Path Variable", "category": "user_input"},
        {"pattern": "@RequestHeader", "framework": "Spring", "label": "Spring Header", "category": "header"},
        {"pattern": "request.getParameter(", "framework": "Servlet", "label": "Servlet Param", "category": "user_input"},
        {"pattern": "request.getInputStream(", "framework": "Servlet", "label": "Servlet Stream", "category": "user_input"},
        {"pattern": "System.getenv(", "framework": "stdlib", "label": "Environment Variable", "category": "env"},
    ],
    "ruby": [
        {"pattern": "params[", "framework": "Rails", "label": "Rails Parameters", "category": "user_input"},
        {"pattern": "request.body", "framework": "Rails", "label": "Rails Request Body", "category": "user_input"},
        {"pattern": "request.headers", "framework": "Rails", "label": "Rails Headers", "category": "header"},
        {"pattern": "ENV[", "framework": "stdlib", "label": "Environment Variable", "category": "env"},
        {"pattern": "ARGV[", "framework": "stdlib", "label": "CLI Argument", "category": "cli"},
    ],
    "php": [
        {"pattern": "$_GET", "framework": "PHP Superglobals", "label": "GET Parameters", "category": "user_input"},
        {"pattern": "$_POST", "framework": "PHP Superglobals", "label": "POST Parameters", "category": "user_input"},
        {"pattern": "$_REQUEST", "framework": "PHP Superglobals", "label": "REQUEST Parameters", "category": "user_input"},
        {"pattern": "$_COOKIE", "framework": "PHP Superglobals", "label": "Cookie Parameters", "category": "user_input"},
        {"pattern": "$_SERVER['HTTP_", "framework": "PHP Superglobals", "label": "HTTP Headers", "category": "header"},
        {"pattern": "$request->input(", "framework": "Laravel", "label": "Laravel Input", "category": "user_input"},
        {"pattern": "$request->query(", "framework": "Laravel", "label": "Laravel Query", "category": "user_input"},
    ],
    "csharp": [
        {"pattern": "[FromQuery]", "framework": "ASP.NET Core", "label": "Query Parameter", "category": "user_input"},
        {"pattern": "[FromBody]", "framework": "ASP.NET Core", "label": "Body Parameter", "category": "user_input"},
        {"pattern": "[FromRoute]", "framework": "ASP.NET Core", "label": "Route Parameter", "category": "user_input"},
        {"pattern": "[FromHeader]", "framework": "ASP.NET Core", "label": "Header Parameter", "category": "header"},
        {"pattern": "Request.Query[", "framework": "ASP.NET Core", "label": "Request Query", "category": "user_input"},
        {"pattern": "Request.Form[", "framework": "ASP.NET Core", "label": "Request Form", "category": "user_input"},
        {"pattern": "Environment.GetEnvironmentVariable(", "framework": "stdlib", "label": "Environment Variable", "category": "env"},
    ]
}

TAINT_SINKS: Dict[str, List[Dict[str, Any]]] = {
    "python": [
        {"pattern": "execute(", "category": "sql-injection", "rule": "TG-INPUT-002", "severity": "Critical"},
        {"pattern": "raw(", "category": "sql-injection", "rule": "TG-INPUT-002", "severity": "Critical"},
        {"pattern": "cursor.execute(", "category": "sql-injection", "rule": "TG-INPUT-002", "severity": "Critical"},
        {"pattern": "os.system(", "category": "command-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "subprocess.call(", "category": "command-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "subprocess.Popen(", "category": "command-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "subprocess.run(", "category": "command-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "eval(", "category": "code-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "exec(", "category": "code-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "open(", "category": "path-traversal", "rule": "TG-INPUT-006", "severity": "High"},
        {"pattern": "send_file(", "category": "path-traversal", "rule": "TG-INPUT-006", "severity": "High"},
        {"pattern": "redirect(", "category": "open-redirect", "rule": "TG-INPUT-007", "severity": "Medium"},
        {"pattern": "mark_safe(", "category": "xss", "rule": "TG-INPUT-005", "severity": "High"},
        {"pattern": "render_template_string(", "category": "ssti", "rule": "TG-INPUT-005", "severity": "High"},
        {"pattern": "pickle.loads(", "category": "deserialization", "rule": "TG-INPUT-008", "severity": "Critical"},
        {"pattern": "yaml.load(", "category": "deserialization", "rule": "TG-INPUT-008", "severity": "High"},
        {"pattern": "requests.get(", "category": "ssrf", "rule": "TG-SSRF-001", "severity": "High"},
        {"pattern": "requests.post(", "category": "ssrf", "rule": "TG-SSRF-001", "severity": "High"},
        {"pattern": "httpx.get(", "category": "ssrf", "rule": "TG-SSRF-001", "severity": "High"},
        {"pattern": "urllib.request.urlopen(", "category": "ssrf", "rule": "TG-SSRF-001", "severity": "High"},
        {"pattern": "jwt.decode(", "category": "jwt-integrity", "rule": "TG-AUTH-006", "severity": "High"},
    ],
    "javascript": [
        {"pattern": "innerHTML", "category": "xss", "rule": "TG-INPUT-003", "severity": "High"},
        {"pattern": "dangerouslySetInnerHTML", "category": "xss", "rule": "TG-INPUT-003", "severity": "High"},
        {"pattern": "document.write(", "category": "xss", "rule": "TG-INPUT-003", "severity": "High"},
        {"pattern": ".query(", "category": "sql-injection", "rule": "TG-INPUT-002", "severity": "Critical"},
        {"pattern": "$queryRawUnsafe", "category": "sql-injection", "rule": "TG-INPUT-002", "severity": "Critical"},
        {"pattern": "child_process.exec(", "category": "command-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "child_process.spawn(", "category": "command-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "eval(", "category": "code-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "new Function(", "category": "code-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "fetch(", "category": "ssrf", "rule": "TG-SSRF-001", "severity": "High"},
        {"pattern": "axios.get(", "category": "ssrf", "rule": "TG-SSRF-001", "severity": "High"},
        {"pattern": "axios.post(", "category": "ssrf", "rule": "TG-SSRF-001", "severity": "High"},
        {"pattern": "res.redirect(", "category": "open-redirect", "rule": "TG-INPUT-007", "severity": "Medium"},
        {"pattern": "fs.readFile(", "category": "path-traversal", "rule": "TG-INPUT-006", "severity": "High"},
        {"pattern": "fs.createReadStream(", "category": "path-traversal", "rule": "TG-INPUT-006", "severity": "High"},
    ],
    "go": [
        {"pattern": "db.Query(", "category": "sql-injection", "rule": "TG-INPUT-002", "severity": "Critical"},
        {"pattern": "db.Exec(", "category": "sql-injection", "rule": "TG-INPUT-002", "severity": "Critical"},
        {"pattern": "exec.Command(", "category": "command-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "http.Get(", "category": "ssrf", "rule": "TG-SSRF-001", "severity": "High"},
        {"pattern": "http.Post(", "category": "ssrf", "rule": "TG-SSRF-001", "severity": "High"},
        {"pattern": "os.Open(", "category": "path-traversal", "rule": "TG-INPUT-006", "severity": "High"},
        {"pattern": "os.ReadFile(", "category": "path-traversal", "rule": "TG-INPUT-006", "severity": "High"},
        {"pattern": "template.HTML(", "category": "xss", "rule": "TG-INPUT-005", "severity": "High"},
        {"pattern": "http.Redirect(", "category": "open-redirect", "rule": "TG-INPUT-007", "severity": "Medium"},
    ],
    "rust": [
        {"pattern": "sqlx::query(", "category": "sql-injection", "rule": "TG-INPUT-002", "severity": "Critical"},
        {"pattern": "Command::new(", "category": "command-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "reqwest::get(", "category": "ssrf", "rule": "TG-SSRF-001", "severity": "High"},
        {"pattern": "std::fs::read(", "category": "path-traversal", "rule": "TG-INPUT-006", "severity": "High"},
    ],
    "java": [
        {"pattern": "statement.executeQuery(", "category": "sql-injection", "rule": "TG-INPUT-002", "severity": "Critical"},
        {"pattern": "Runtime.getRuntime().exec(", "category": "command-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "new ProcessBuilder(", "category": "command-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "new URL(", "category": "ssrf", "rule": "TG-SSRF-001", "severity": "High"},
        {"pattern": "new FileInputStream(", "category": "path-traversal", "rule": "TG-INPUT-006", "severity": "High"},
    ],
    "ruby": [
        {"pattern": "ActiveRecord::Base.connection.execute(", "category": "sql-injection", "rule": "TG-INPUT-002", "severity": "Critical"},
        {"pattern": "system(", "category": "command-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "send_file ", "category": "path-traversal", "rule": "TG-INPUT-006", "severity": "High"},
        {"pattern": "redirect_to ", "category": "open-redirect", "rule": "TG-INPUT-007", "severity": "Medium"},
    ],
    "php": [
        {"pattern": "mysqli_query(", "category": "sql-injection", "rule": "TG-INPUT-002", "severity": "Critical"},
        {"pattern": "PDO::query(", "category": "sql-injection", "rule": "TG-INPUT-002", "severity": "Critical"},
        {"pattern": "system(", "category": "command-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "shell_exec(", "category": "command-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "include(", "category": "path-traversal", "rule": "TG-INPUT-006", "severity": "High"},
        {"pattern": "header('Location:", "category": "open-redirect", "rule": "TG-INPUT-007", "severity": "Medium"},
    ],
    "csharp": [
        {"pattern": "SqlCommand(", "category": "sql-injection", "rule": "TG-INPUT-002", "severity": "Critical"},
        {"pattern": "Process.Start(", "category": "command-injection", "rule": "TG-INPUT-003", "severity": "Critical"},
        {"pattern": "File.OpenRead(", "category": "path-traversal", "rule": "TG-INPUT-006", "severity": "High"},
        {"pattern": "Redirect(", "category": "open-redirect", "rule": "TG-INPUT-007", "severity": "Medium"},
    ]
}

TAINT_SANITIZERS: Dict[str, List[Dict[str, Any]]] = {
    "python": [
        {"pattern": "int(", "cleans": ["sql-injection", "command-injection", "path-traversal", "ssrf"]},
        {"pattern": "float(", "cleans": ["sql-injection", "command-injection"]},
        {"pattern": "escape(", "cleans": ["xss", "ssti"]},
        {"pattern": "html.escape(", "cleans": ["xss", "ssti"]},
        {"pattern": "bleach.clean(", "cleans": ["xss"]},
        {"pattern": "shlex.quote(", "cleans": ["command-injection"]},
        {"pattern": "secure_filename(", "cleans": ["path-traversal"]},
        {"pattern": "os.path.basename(", "cleans": ["path-traversal"]},
        {"pattern": "Path.resolve()", "cleans": ["path-traversal"]},
        {"pattern": "validators.url(", "cleans": ["ssrf", "open-redirect"]},
        {"pattern": "Depends(", "cleans": ["auth-bypass"]},
        {"pattern": "SafeLoader", "cleans": ["deserialization"]},
        {"pattern": ".safeParse(", "cleans": ["sql-injection", "xss", "command-injection"]},
    ],
    "javascript": [
        {"pattern": "parseInt(", "cleans": ["sql-injection", "command-injection", "path-traversal", "ssrf"]},
        {"pattern": "Number(", "cleans": ["sql-injection", "command-injection", "path-traversal"]},
        {"pattern": "encodeURIComponent(", "cleans": ["xss", "open-redirect"]},
        {"pattern": "DOMPurify.sanitize(", "cleans": ["xss"]},
        {"pattern": "z.string().parse(", "cleans": ["sql-injection", "xss"]},
        {"pattern": "z.number()", "cleans": ["sql-injection", "command-injection"]},
        {"pattern": "path.basename(", "cleans": ["path-traversal"]},
        {"pattern": "path.normalize(", "cleans": ["path-traversal"]},
        {"pattern": "escapeHtml(", "cleans": ["xss"]},
        {"pattern": "validator.isURL(", "cleans": ["ssrf", "open-redirect"]},
    ],
    "go": [
        {"pattern": "strconv.Atoi(", "cleans": ["sql-injection", "command-injection", "path-traversal"]},
        {"pattern": "strconv.ParseInt(", "cleans": ["sql-injection", "command-injection"]},
        {"pattern": "filepath.Base(", "cleans": ["path-traversal"]},
        {"pattern": "filepath.Clean(", "cleans": ["path-traversal"]},
        {"pattern": "html.EscapeString(", "cleans": ["xss"]},
        {"pattern": "url.Parse(", "cleans": ["open-redirect", "ssrf"]},
    ],
    "rust": [
        {"pattern": "parse::<i32>", "cleans": ["sql-injection", "command-injection"]},
        {"pattern": "parse::<u32>", "cleans": ["sql-injection", "command-injection"]},
        {"pattern": "Path::new(", "cleans": ["path-traversal"]},
    ],
    "java": [
        {"pattern": "Integer.parseInt(", "cleans": ["sql-injection", "command-injection"]},
        {"pattern": "Long.parseLong(", "cleans": ["sql-injection", "command-injection"]},
        {"pattern": "Paths.get(", "cleans": ["path-traversal"]},
        {"pattern": "ESAPI.encoder()", "cleans": ["xss", "sql-injection"]},
    ],
    "ruby": [
        {"pattern": ".to_i", "cleans": ["sql-injection", "command-injection"]},
        {"pattern": "File.basename(", "cleans": ["path-traversal"]},
        {"pattern": "CGI.escapeHTML(", "cleans": ["xss"]},
    ],
    "php": [
        {"pattern": "intval(", "cleans": ["sql-injection", "command-injection"]},
        {"pattern": "(int)", "cleans": ["sql-injection", "command-injection"]},
        {"pattern": "htmlspecialchars(", "cleans": ["xss"]},
        {"pattern": "basename(", "cleans": ["path-traversal"]},
        {"pattern": "filter_var(", "cleans": ["ssrf", "xss", "sql-injection"]},
    ],
    "csharp": [
        {"pattern": "int.Parse(", "cleans": ["sql-injection", "command-injection"]},
        {"pattern": "int.TryParse(", "cleans": ["sql-injection", "command-injection"]},
        {"pattern": "Path.GetFileName(", "cleans": ["path-traversal"]},
        {"pattern": "HttpUtility.HtmlEncode(", "cleans": ["xss"]},
    ]
}


def get_sources_for_language(lang: str) -> List[Dict[str, Any]]:
    return TAINT_SOURCES.get(lang.lower(), [])


def get_sinks_for_language(lang: str) -> List[Dict[str, Any]]:
    return TAINT_SINKS.get(lang.lower(), [])


def get_sanitizers_for_language(lang: str) -> List[Dict[str, Any]]:
    return TAINT_SANITIZERS.get(lang.lower(), [])
