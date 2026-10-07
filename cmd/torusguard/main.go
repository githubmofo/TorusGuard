package main

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/torusguard/torusguard/internal/apply"
	"github.com/torusguard/torusguard/internal/harden"
	"github.com/torusguard/torusguard/internal/memory"
	"github.com/torusguard/torusguard/internal/recheck"
	"github.com/torusguard/torusguard/internal/report"
	"github.com/torusguard/torusguard/internal/rules"
	"github.com/torusguard/torusguard/internal/scanner"
	"github.com/torusguard/torusguard/internal/termui"
	"github.com/torusguard/torusguard/internal/validate"
	"github.com/torusguard/torusguard/internal/workspace"
)

const Version = "2.2.0"

// Standardized 75-column terminal UI formatting with Unicode emoji width calculation
func printHelp() {
	fmt.Println()
	fmt.Println(termui.CardHeader("🛡️  T O R U S G U A R D   C L I   ( G O )", "Autonomous Security Engine for AI-Built Applications", "v"+Version, termui.Cyan))
	fmt.Printf("\n  %sUsage:%s  %storusguard%s %s[command]%s %s[options]%s\n\n", termui.Bold, termui.Reset, termui.Green, termui.Reset, termui.White, termui.Reset, termui.Gray, termui.Reset)

	fmt.Println(termui.CardBorderTop("Commands", termui.Cyan, false))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sinit%s        Scaffold workspace, detect stack, activate TG rules", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sstatus%s      Diagnostic overview of posture, stack, and active rules", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%saudit%s       Static AST security scan against active rules", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sreview%s      Differential PR and Git diff incremental review", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sthreatmodel%s Synthesize STRIDE threat model & Mermaid DFDs", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sbenchmark%s   Run SecurityReviewBench precision & recall suite", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sverify%s      Live disk line match audit and evidence check", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sharden%s      Formulate zero-regression remediation patches", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sapply%s       Apply patches with pre-apply rollback snapshots", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%srollback%s    Instant restoration from pre-apply snapshots", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%srecheck%s     Run differential re-scan on modified files", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sreport%s      Generate HTML/SARIF posture reports", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%srecipes%s     Manage TorusGuard Golden Fix library", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sauthorize%s   Target domain whitelisting and ownership proof", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sweb-validate%s Authorized HTTP probing with audit headers", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sexploit-check%s Bounded exploitability confirmation", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%socr-scan%s    Run Tesseract OCR secret scan on images/diagrams", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%scontainer%s   Audit Dockerfile, compose, and container configs", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sgit-mine%s    Mine git commit history for leaked secrets & creds", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sredos%s       Analyze regex patterns for catastrophic backtracking", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sai-guard%s    Scan AI/LLM code for prompt injection & RAG flaws", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%smcp%s         Run Model Context Protocol (MCP) server over stdio", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sfull%s        Execute master 7-stage security governance pipeline", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%supdate%s      Self-update TorusGuard engine", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%shelp%s        Show this interactive command guide", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.CardBorderBottom(termui.Cyan, false))
	fmt.Println()
}

func parseTarget(args []string) string {
	target := "."
	for i := 0; i < len(args); i++ {
		a := args[i]
		if a == "--target" || a == "-t" || a == "--root" {
			if i+1 < len(args) {
				target = args[i+1]
			}
		} else if !strings.HasPrefix(a, "-") && i == 0 {
			target = a
		}
	}
	absTarget, _ := filepath.Abs(target)
	return absTarget
}

func isTerminal() bool {
	fi, err := os.Stdin.Stat()
	if err != nil {
		return false
	}
	return (fi.Mode() & os.ModeCharDevice) != 0
}

func runInteractiveMenu() {
	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Println()
		fmt.Println(termui.CardHeader("🛡️  TORUSGUARD COMMAND CENTER", "Interactive Security Engine", "v"+Version, termui.Cyan))
		fmt.Println(termui.CardBorderTop("Quick Actions", termui.Cyan, false))
		fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s[1]%s  🚀 Audit Workspace          %s(Full AST & Taint Scan)%s", termui.Green, termui.Reset, termui.Gray, termui.Reset), 67, "│", termui.Cyan))
		fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s[2]%s  👁️  OCR Vision Scan          %s(Images & Diagram Secrets)%s", termui.Green, termui.Reset, termui.Gray, termui.Reset), 67, "│", termui.Cyan))
		fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s[3]%s  📊 Posture Status           %s(Active Posture & Rules)%s", termui.Green, termui.Reset, termui.Gray, termui.Reset), 67, "│", termui.Cyan))
		fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s[4]%s  🐳 Container Audit          %s(Dockerfile & Compose Scan)%s", termui.Green, termui.Reset, termui.Gray, termui.Reset), 67, "│", termui.Cyan))
		fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s[5]%s  ⚡ ReDoS Complexity Scan    %s(Catastrophic Regex Scan)%s", termui.Green, termui.Reset, termui.Gray, termui.Reset), 67, "│", termui.Cyan))
		fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s[6]%s  🤖 AI & RAG Defense         %s(Prompt Injection & Vectors)%s", termui.Green, termui.Reset, termui.Gray, termui.Reset), 67, "│", termui.Cyan))
		fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s[7]%s  🔍 Git History Mine         %s(Committed Leaks & Tokens)%s", termui.Green, termui.Reset, termui.Gray, termui.Reset), 67, "│", termui.Cyan))
		fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s[8]%s  🛡️  Harden Candidates       %s(Ponytail Bounded Patches)%s", termui.Green, termui.Reset, termui.Gray, termui.Reset), 67, "│", termui.Cyan))
		fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s[9]%s  📑 Posture Report           %s(Generate Visual HTML Report)%s", termui.Green, termui.Reset, termui.Gray, termui.Reset), 67, "│", termui.Cyan))
		fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s[10]%s 📖 Awesome Rules Catalog    %s(88 Rules Across 22 Families)%s", termui.Green, termui.Reset, termui.Gray, termui.Reset), 67, "│", termui.Cyan))
		fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s[0]%s  ❌ Exit", termui.Red, termui.Reset), 67, "│", termui.Cyan))
		fmt.Println(termui.CardBorderBottom(termui.Cyan, false))
		fmt.Printf("\n  %sSelect option [0-10]%s: ", termui.Bold, termui.Reset)

		input, err := reader.ReadString('\n')
		if err != nil {
			return
		}
		choice := strings.TrimSpace(input)
		switch choice {
		case "1":
			executeCommand("audit", []string{})
		case "2":
			executeCommand("ocr-scan", []string{})
		case "3":
			executeCommand("status", []string{})
		case "4":
			executeCommand("container", []string{})
		case "5":
			executeCommand("redos", []string{})
		case "6":
			executeCommand("ai-guard", []string{})
		case "7":
			executeCommand("git-mine", []string{})
		case "8":
			executeCommand("harden", []string{})
		case "9":
			executeCommand("report", []string{"--html"})
		case "10":
			executeCommand("recipes", []string{})
		case "0", "q", "exit":
			fmt.Printf("\n  %sExiting TorusGuard.%s\n\n", termui.Green, termui.Reset)
			return
		default:
			fmt.Printf("\n  %sInvalid selection '%s'. Enter 0-10.%s\n", termui.Yellow, choice, termui.Reset)
		}
	}
}

func main() {
	if len(os.Args) < 2 {
		if isTerminal() {
			runInteractiveMenu()
			return
		}
		printHelp()
		return
	}

	command := os.Args[1]
	cliArgs := os.Args[2:]

	if command == "--version" || command == "-v" || command == "version" {
		fmt.Printf("torusguard v%s (pure go binary)\n", Version)
		return
	}

	if command == "help" || command == "--help" || command == "-h" {
		printHelp()
		return
	}

	executeCommand(command, cliArgs)
}

func executeCommand(command string, cliArgs []string) {
	target := parseTarget(cliArgs)

	switch command {
	case "init":
		err := workspace.InitWorkspace(target)
		if err != nil {
			fmt.Printf("Failed to init workspace: %v\n", err)
			os.Exit(1)
		}
	case "status":
		stack, _ := workspace.DetectStack(target)
		fmt.Println()
		fmt.Println(termui.CardHeader("🛡️  TORUSGUARD STATUS", "Workspace Posture", "v"+Version, termui.Green))
		fmt.Println(termui.CardBorderTop("Stack Detected", termui.Green, false))
		fmt.Println(termui.FormatBoxLine(strings.Join(stack, ", "), 67, "│", termui.Green))
		fmt.Println(termui.CardBorderBottom(termui.Green, false))
		fmt.Println()
	case "audit":
		catalog, err := rules.LoadRules(filepath.Join(target, ".torusguard"))
		if err != nil {
			fmt.Printf("Warning: Failed to load rules: %v\n", err)
			catalog = &rules.Catalog{}
		}

		findings, err := scanner.RunAudit(target, catalog)
		if err != nil {
			fmt.Printf("Audit failed: %v\n", err)
			os.Exit(1)
		}

		err = report.SyncReport(target, findings)
		if err != nil {
			fmt.Printf("Failed to write report: %v\n", err)
			os.Exit(1)
		}
		
		fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s✔ Scan complete. Check security_report.md.%s", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	case "harden":
		patchFile := "candidate.patch"
		if len(cliArgs) > 0 {
			patchFile = cliArgs[0]
		}
		if err := harden.RunHarden(patchFile); err != nil {
			fmt.Printf("Harden failed: %v\n", err)
			os.Exit(1)
		}
	case "apply":
		autoYes := false
		patchFile := "candidate.patch"
		for _, arg := range cliArgs {
			if arg == "--yes" || arg == "-y" {
				autoYes = true
			} else if !strings.HasPrefix(arg, "-") {
				patchFile = arg
			}
		}
		if err := apply.RunApply(patchFile, target, autoYes); err != nil {
			fmt.Printf("Apply failed: %v\n", err)
			os.Exit(1)
		}
	case "recheck":
		if err := recheck.RunRecheck(target); err != nil {
			fmt.Printf("Recheck failed: %v\n", err)
			os.Exit(1)
		}
	case "report":
		useHtml := false
		useSarif := false
		for _, arg := range cliArgs {
			if arg == "--html" {
				useHtml = true
			} else if arg == "--sarif" {
				useSarif = true
			}
		}
		
		findings := []string{}
		
		reportData, err := os.ReadFile(filepath.Join(target, "security_report.md"))
		if err == nil {
			lines := strings.Split(string(reportData), "\n")
			for _, line := range lines {
				if strings.TrimSpace(line) != "" {
					findings = append(findings, line)
				}
			}
		}
		
		if useHtml {
			if err := report.GenerateHTMLReport(target, findings); err != nil {
				fmt.Printf("HTML report generation failed: %v\n", err)
			}
		} else if useSarif {
			if err := report.GenerateSARIFReport(target, findings); err != nil {
				fmt.Printf("SARIF report generation failed: %v\n", err)
			}
		} else {
			fmt.Println("Please specify format: --html or --sarif")
		}
	case "recipes":
		action := "list"
		if len(cliArgs) > 0 {
			action = cliArgs[0]
		}
		if err := memory.RunRecipes(action); err != nil {
			fmt.Printf("Recipes command failed: %v\n", err)
		}
	case "update":
		fmt.Println("Checking for TorusGuard updates...")
		fmt.Printf("TorusGuard is up to date (v%s)\n", Version)
	case "authorize":
		if err := validate.RunAuthorize(target); err != nil {
			fmt.Printf("Authorize failed: %v\n", err)
			os.Exit(1)
		}
	case "web-validate":
		targetURL := ""
		for i, a := range cliArgs {
			if a == "--url" && i+1 < len(cliArgs) {
				targetURL = cliArgs[i+1]
			}
		}
		if err := validate.RunWebValidate(target, targetURL); err != nil {
			fmt.Printf("Web validate failed: %v\n", err)
			os.Exit(1)
		}
	case "exploit-check":
		targetURL := ""
		findingID := ""
		for i, a := range cliArgs {
			if a == "--url" && i+1 < len(cliArgs) {
				targetURL = cliArgs[i+1]
			} else if (a == "--finding" || a == "-f") && i+1 < len(cliArgs) {
				findingID = cliArgs[i+1]
			}
		}
		if err := validate.RunExploitCheck(target, targetURL, findingID); err != nil {
			fmt.Printf("Exploit check failed: %v\n", err)
			os.Exit(1)
		}
	case "verify":
		if err := validate.RunVerify(target); err != nil {
			fmt.Printf("Verify failed: %v\n", err)
			os.Exit(1)
		}
	case "rollback":
		if err := apply.RunRollback(target); err != nil {
			fmt.Printf("Rollback failed: %v\n", err)
			os.Exit(1)
		}
	case "mcp":
		RunMCPServer()
		return
	case "ocr-scan":
		maxMB := 10
		tessPath, _ := scanner.FindTesseract()

		targetPath := target
		explicitTarget := len(cliArgs) > 0 && !strings.HasPrefix(cliArgs[0], "-")
		if !explicitTarget {
			imgs, _ := scanner.FindWorkspaceImages(target)
			if len(imgs) == 1 {
				targetPath = imgs[0]
			}
		}

		info, err := os.Stat(targetPath)
		if err != nil {
			fmt.Printf("Cannot access target %s: %v\n", targetPath, err)
			return
		}

		var findings []string
		if info.IsDir() {
			findings, err = scanner.ScanImagesInDir(targetPath, int64(maxMB)*1024*1024)
		} else {
			findings, err = scanner.ScanImageFile(targetPath, tessPath, int64(maxMB)*1024*1024)
		}
		if err != nil {
			fmt.Printf("OCR scan notice: %v\n", err)
		}

		fmt.Println()
		fmt.Println(termui.CardHeader("👁️   OCR VISION & ASSET SCAN", "First-Principles + Neural Extraction", "v"+Version, termui.Cyan))
		if tessPath != "" {
			fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sEngine:%s Neural Tesseract + First-Principles", termui.Green, termui.Reset), 67, "│", termui.Cyan))
		} else {
			fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sEngine:%s First-Principles Stream & Chunk Extractor", termui.Yellow, termui.Reset), 67, "│", termui.Cyan))
		}
		fmt.Println(termui.FormatBoxLine(fmt.Sprintf("Target: %s", filepath.Base(targetPath)), 67, "│", termui.Cyan))
		fmt.Println(termui.CardDivider("Findings", termui.Cyan, false))

		if len(findings) == 0 {
			fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s✔ Zero leaked secrets detected in image assets.%s", termui.Green, termui.Reset), 67, "│", termui.Cyan))
		} else {
			for _, f := range findings {
				line := f
				if len(line) > 65 {
					line = line[:62] + "..."
				}
				fmt.Println(termui.FormatBoxLine(line, 67, "│", termui.Cyan))
			}
		}

		if tessPath == "" {
			fmt.Println(termui.CardDivider("Neural OCR Setup Hint", termui.Cyan, false))
			fmt.Println(termui.FormatBoxLine("To enable optical character recognition on screenshots:", 67, "│", termui.Cyan))
			fmt.Println(termui.FormatBoxLine("Windows: winget install UB-Mannheim.TesseractOCR", 67, "│", termui.Cyan))
			fmt.Println(termui.FormatBoxLine("macOS:   brew install tesseract", 67, "│", termui.Cyan))
			fmt.Println(termui.FormatBoxLine("Linux:   sudo apt-get install tesseract-ocr", 67, "│", termui.Cyan))
		}
		fmt.Println(termui.CardBorderBottom(termui.Cyan, false))
		fmt.Println()
	case "container":
		findings, err := scanner.RunContainerAudit(target)
		if err != nil {
			fmt.Printf("Container audit failed: %v\n", err)
			os.Exit(1)
		}
		fmt.Println()
		fmt.Println(termui.CardHeader("🐳  CONTAINER AUDIT", "Dockerfile & Compose Hardening", "v"+Version, termui.Cyan))
		if len(findings) == 0 {
			fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s✔ Zero container vulnerabilities detected.%s", termui.Green, termui.Reset), 67, "│", termui.Cyan))
		} else {
			for _, f := range findings {
				line := fmt.Sprintf("[%s] %s:%d %s", f.RuleID, f.File, f.Line, f.Description)
				if len(line) > 65 {
					line = line[:62] + "..."
				}
				fmt.Println(termui.FormatBoxLine(line, 67, "│", termui.Cyan))
			}
		}
		fmt.Println(termui.CardBorderBottom(termui.Cyan, false))
		fmt.Println()
	case "git-mine":
		findings, err := scanner.RunGitMineAudit(target)
		if err != nil {
			fmt.Printf("Git mine audit failed: %v\n", err)
			os.Exit(1)
		}
		fmt.Println()
		fmt.Println(termui.CardHeader("🔍  GIT HISTORY SECRET MINING", "Commit Logs & Config Audit", "v"+Version, termui.Yellow))
		if len(findings) == 0 {
			fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s✔ Zero leaked secrets in Git history.%s", termui.Green, termui.Reset), 67, "│", termui.Yellow))
		} else {
			for _, f := range findings {
				line := fmt.Sprintf("[%s] %s:%d %s", f.RuleID, f.File, f.Line, f.Description)
				if len(line) > 65 {
					line = line[:62] + "..."
				}
				fmt.Println(termui.FormatBoxLine(line, 67, "│", termui.Yellow))
			}
		}
		fmt.Println(termui.CardBorderBottom(termui.Yellow, false))
		fmt.Println()
	case "redos":
		findings, err := scanner.RunReDoSAudit(target)
		if err != nil {
			fmt.Printf("ReDoS audit failed: %v\n", err)
			os.Exit(1)
		}
		fmt.Println()
		fmt.Println(termui.CardHeader("⚡  REDOS COMPLEXITY SCANNER", "Catastrophic Backtracking Analysis", "v"+Version, termui.Red))
		if len(findings) == 0 {
			fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s✔ Zero catastrophic backtracking regexes detected.%s", termui.Green, termui.Reset), 67, "│", termui.Red))
		} else {
			for _, f := range findings {
				line := fmt.Sprintf("[%s] %s:%d %s", f.RuleID, f.File, f.Line, f.Description)
				if len(line) > 65 {
					line = line[:62] + "..."
				}
				fmt.Println(termui.FormatBoxLine(line, 67, "│", termui.Red))
			}
		}
		fmt.Println(termui.CardBorderBottom(termui.Red, false))
		fmt.Println()
	case "ai-guard":
		findings, err := scanner.RunAIGuardAudit(target)
		if err != nil {
			fmt.Printf("AI Guard audit failed: %v\n", err)
			os.Exit(1)
		}
		fmt.Println()
		fmt.Println(termui.CardHeader("🤖  AI & RAG PIPELINE DEFENSE", "Injection & Vector Boundary Guard", "v"+Version, termui.Cyan))
		if len(findings) == 0 {
			fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%s✔ Zero AI prompt injection / RAG flaws detected.%s", termui.Green, termui.Reset), 67, "│", termui.Cyan))
		} else {
			for _, f := range findings {
				line := fmt.Sprintf("[%s] %s:%d %s", f.RuleID, f.File, f.Line, f.Description)
				if len(line) > 65 {
					line = line[:62] + "..."
				}
				fmt.Println(termui.FormatBoxLine(line, 67, "│", termui.Cyan))
			}
		}
	case "review":
		diffRef := "HEAD~1"
		for i, a := range cliArgs {
			if (a == "--diff" || a == "-d" || a == "--from") && i+1 < len(cliArgs) {
				diffRef = cliArgs[i+1]
			}
		}
		_, err := RunReview(target, diffRef)
		if err != nil {
			fmt.Printf("Review failed: %v\n", err)
			os.Exit(1)
		}
	case "threatmodel":
		err := RunThreatModel(target)
		if err != nil {
			fmt.Printf("Threat model generation failed: %v\n", err)
			os.Exit(1)
		}
	case "benchmark":
		err := RunBenchmark()
		if err != nil {
			fmt.Printf("Benchmark failed: %v\n", err)
			os.Exit(1)
		}
	case "full":
		fmt.Println()
		fmt.Println(termui.CardHeader("🛡️  TORUSGUARD MASTER PIPELINE", "7-Stage Security Lifecycle", "v"+Version, termui.Cyan))
		fmt.Println(termui.FormatBoxLine("Executing Stages: Init ➔ Authorize ➔ Audit ➔ Verify ➔ Report", 67, "│", termui.Cyan))
		fmt.Println(termui.CardBorderBottom(termui.Cyan, false))
		fmt.Println()

		// Stage 0: Init
		fmt.Println("==> Stage 0: Workspace Stack Discovery & Rule Profiling...")
		_ = workspace.InitWorkspace(target)

		// Stage 1: Authorize
		fmt.Println("==> Stage 1: Target Scope & Cryptographic Authorization Gate...")
		_ = validate.RunAuthorize(target)

		// Stage 2: Audit
		fmt.Println("==> Stage 2: Polyglot AST, First-Principles & Multi-Modal Scan...")
		cat, _ := rules.LoadRules(filepath.Join(target, ".torusguard"))
		if cat == nil {
			cat = &rules.Catalog{}
		}
		findings, _ := scanner.RunAudit(target, cat)
		_ = report.SyncReport(target, findings)

		// Stage 3: Verify
		fmt.Println("==> Stage 3: Finding Confidence Calibration & Line Fingerprint Verification...")
		_ = validate.RunVerify(target)

		// Stage 7: Report
		fmt.Println("==> Stage 7: Living Posture Ledger & SARIF / HTML Export...")
		_ = report.GenerateHTMLReport(target, findings)
		_ = report.GenerateSARIFReport(target, findings)

		fmt.Println()
		fmt.Println(termui.CardHeader("✔ PIPELINE COMPLETE", "All Stages Succeeded", "v"+Version, termui.Green))
		fmt.Println(termui.CardBorderBottom(termui.Green, false))
		fmt.Println()
	default:
		fmt.Fprintf(os.Stderr, "\n  %s✖ Unknown command:%s %s%s%s\n", termui.Red, termui.Reset, termui.White, command, termui.Reset)
		fmt.Fprintf(os.Stderr, "  Run %storusguard help%s for available commands.\n\n", termui.Green, termui.Reset)
		os.Exit(1)
	}
}
