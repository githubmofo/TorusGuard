package main

import (
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

const Version = "2.0.0-alpha"

func printHelp() {
	fmt.Println()
	fmt.Println(termui.CardHeader("🛡️  T O R U S G U A R D   C L I   ( G O )", "Autonomous Security Engine for AI-Built Applications", "v"+Version, termui.Cyan))
	fmt.Printf("\n  %sUsage:%s  %storusguard%s %s[command]%s %s[options]%s\n\n", termui.Bold, termui.Reset, termui.Green, termui.Reset, termui.White, termui.Reset, termui.Gray, termui.Reset)

	fmt.Println(termui.CardBorderTop("Commands", termui.Cyan, false))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sinit%s        Scaffold workspace, detect stack, activate TG rules", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sstatus%s      Diagnostic overview of posture, stack, and active rules", termui.Green, termui.Reset), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%saudit%s       Static AST security scan against active rules", termui.Green, termui.Reset), 67, "│", termui.Cyan))
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
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%smcp%s         Run Model Context Protocol (MCP) server over stdio", termui.Green, termui.Reset), 67, "│", termui.Cyan))
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

func main() {
	if len(os.Args) < 2 {
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
		if err := validate.RunWebValidate(target); err != nil {
			fmt.Printf("Web validate failed: %v\n", err)
			os.Exit(1)
		}
	case "exploit-check":
		if err := validate.RunExploitCheck(target); err != nil {
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
		tessPath, err := scanner.FindTesseract()
		if err != nil {
			fmt.Printf("OCR scan aborted: %v\n", err)
			os.Exit(1)
		}
		info, err := os.Stat(target)
		if err != nil {
			fmt.Printf("Cannot access target %s: %v\n", target, err)
			os.Exit(1)
		}
		var findings []string
		if info.IsDir() {
			findings, err = scanner.ScanImagesInDir(target, int64(maxMB)*1024*1024)
		} else {
			findings, err = scanner.ScanImageFile(target, tessPath, int64(maxMB)*1024*1024)
		}
		if err != nil {
			fmt.Printf("OCR scan failed: %v\n", err)
			os.Exit(1)
		}
		fmt.Printf("Scanned image target '%s' (Tesseract: %s)\n", target, tessPath)
		fmt.Printf("Detected %d findings:\n", len(findings))
		for _, f := range findings {
			fmt.Printf(" - %s\n", f)
		}
	default:
		fmt.Fprintf(os.Stderr, "\n  %s✖ Unknown command:%s %s%s%s\n", termui.Red, termui.Reset, termui.White, command, termui.Reset)
		fmt.Fprintf(os.Stderr, "  Run %storusguard help%s for available commands.\n\n", termui.Green, termui.Reset)
		os.Exit(1)
	}
}
