package scanner

import (
	"testing"
)

func TestAnalyzeFileTaintGo(t *testing.T) {
	lines := []string{
		`package main`,
		`import "net/http"`,
		`func handleSearch(w http.ResponseWriter, r *http.Request) {`,
		`    userInput := r.URL.Query().Get("q")`,
		`    query := "SELECT * FROM items WHERE name=" + userInput`,
		`    db.Query(query)`,
		`}`,
	}

	findings := AnalyzeFileTaint("search.go", lines, nil)
	if len(findings) == 0 {
		t.Fatalf("expected multi-hop taint finding in Go code, got 0")
	}

	f := findings[0]
	if f.RuleID != "TG-DB-002" {
		t.Errorf("expected rule TG-DB-002, got %s", f.RuleID)
	}
	if f.Line != 6 {
		t.Errorf("expected finding on line 6 (sink), got %d", f.Line)
	}
}

func TestAnalyzeFileTaintPython(t *testing.T) {
	lines := []string{
		`def run_cmd(request):`,
		`    target_file = request.args.get("file")`,
		`    path = "/data/" + target_file`,
		`    f = open(path)`,
		`    return f.read()`,
	}

	findings := AnalyzeFileTaint("views.py", lines, nil)
	if len(findings) == 0 {
		t.Fatalf("expected multi-hop taint finding in Python code, got 0")
	}

	f := findings[0]
	if f.RuleID != "TG-INPUT-002" {
		t.Errorf("expected rule TG-INPUT-002, got %s", f.RuleID)
	}
	if f.Line != 4 {
		t.Errorf("expected finding on line 4 (sink), got %d", f.Line)
	}
}

func TestAnalyzeFileTaintSanitizer(t *testing.T) {
	lines := []string{
		`function getFile(req, res) {`,
		`    const rawPath = req.query.path;`,
		`    const safePath = filepath.Base(rawPath);`,
		`    const data = fs.readFile(safePath);`,
		`}`,
	}

	findings := AnalyzeFileTaint("api.js", lines, nil)
	if len(findings) != 0 {
		t.Errorf("expected 0 findings when sanitized with filepath.Base, got %d", len(findings))
	}
}
