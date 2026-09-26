package scanner

import (
	"os"
	"path/filepath"
	"testing"
)

func TestContainerScanner(t *testing.T) {
	tempDir, err := os.MkdirTemp("", "tg_test_container_*")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tempDir)

	// 1. Create vulnerable Dockerfile (missing USER and has build secret)
	dockerfileContent := `FROM node:18-alpine
WORKDIR /app
COPY . .
ARG GITHUB_TOKEN=ghp_1234567890abcdef1234567890abcdef
CMD ["node", "index.js"]`

	err = os.WriteFile(filepath.Join(tempDir, "Dockerfile"), []byte(dockerfileContent), 0644)
	if err != nil {
		t.Fatal(err)
	}

	// 2. Create vulnerable docker-compose.yml
	composeContent := `version: '3.8'
services:
  web:
    image: web:latest
    privileged: true
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock`

	err = os.WriteFile(filepath.Join(tempDir, "docker-compose.yml"), []byte(composeContent), 0644)
	if err != nil {
		t.Fatal(err)
	}

	findings, err := ScanContainerFiles(tempDir)
	if err != nil {
		t.Fatalf("ScanContainerFiles failed: %v", err)
	}

	foundRoot := false
	foundSock := false
	foundPriv := false
	foundArg := false

	for _, f := range findings {
		switch f.RuleID {
		case "TG-CONT-001":
			foundRoot = true
		case "TG-CONT-002":
			foundSock = true
		case "TG-CONT-003":
			foundPriv = true
		case "TG-CONT-004":
			foundArg = true
		}
	}

	if !foundRoot {
		t.Errorf("Expected TG-CONT-001 for missing USER directive")
	}
	if !foundSock {
		t.Errorf("Expected TG-CONT-002 for docker.sock mount")
	}
	if !foundPriv {
		t.Errorf("Expected TG-CONT-003 for privileged container mode")
	}
	if !foundArg {
		t.Errorf("Expected TG-CONT-004 for GITHUB_TOKEN in ARG")
	}
}

func TestReDoSScanner(t *testing.T) {
	tempDir, err := os.MkdirTemp("", "tg_test_redos_*")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tempDir)

	jsContent := `// Vulnerable regex with nested quantifier
const emailRegex = /^([a-zA-Z0-9_\.\-])+@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
`
	err = os.WriteFile(filepath.Join(tempDir, "validator.js"), []byte(jsContent), 0644)
	if err != nil {
		t.Fatal(err)
	}

	findings, err := ScanReDoS(tempDir)
	if err != nil {
		t.Fatalf("ScanReDoS failed: %v", err)
	}

	foundReDoS := false
	for _, f := range findings {
		if f.RuleID == "TG-REDOS-001" {
			foundReDoS = true
			break
		}
	}

	if !foundReDoS {
		t.Errorf("Expected TG-REDOS-001 finding for nested quantifier pattern")
	}
}

func TestAIGuardScanner(t *testing.T) {
	tempDir, err := os.MkdirTemp("", "tg_test_aiguard_*")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tempDir)

	pyContent := `def execute_rag(user_query):
    docs = vector_db.similarity_search(query)
    context = "\n".join([d.page_content for d in docs])
    messages = [
        {"role": "system", "content": f"System prompt with context: {context}"},
        {"role": "user", "content": user_query}
    ]
    return client.chat.completions.create(messages=messages)

def run_agent_tool(args):
    return os.system(args["cmd"])
`
	err = os.WriteFile(filepath.Join(tempDir, "rag_service.py"), []byte(pyContent), 0644)
	if err != nil {
		t.Fatal(err)
	}

	findings, err := ScanAIGuard(tempDir)
	if err != nil {
		t.Fatalf("ScanAIGuard failed: %v", err)
	}

	foundRAG := false
	foundTool := false
	foundVector := false

	for _, f := range findings {
		switch f.RuleID {
		case "TG-RAG-001":
			foundRAG = true
		case "TG-RAG-002":
			foundTool = true
		case "TG-RAG-003":
			foundVector = true
		}
	}

	if !foundRAG {
		t.Errorf("Expected TG-RAG-001 for RAG context in system prompt")
	}
	if !foundTool {
		t.Errorf("Expected TG-RAG-002 for os.system tool execution")
	}
	if !foundVector {
		t.Errorf("Expected TG-RAG-003 for unpartitioned vector search")
	}
}
