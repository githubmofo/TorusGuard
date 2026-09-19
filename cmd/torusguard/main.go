// TorusGuard CLI Runner (Go Distribution)
// Provides zero-dependency command orchestration for TorusGuard governance in Go environments.
// Adheres to Ponytail principles: concise, surgical, zero fluff, 75-column terminal cards.
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

const (
	Version   = "1.4.0"
	Bold      = "\033[1m"
	Dim       = "\033[2m"
	Reset     = "\033[0m"
	Cyan      = "\033[36m"
	Green     = "\033[32m"
	Yellow    = "\033[33m"
	White     = "\033[97m"
	Gray      = "\033[90m"
	Red       = "\033[31m"
	MaxCardW  = 67
)

func formatBoxLine(content string, width int, border string, borderColor string) string {
	clean := stripAnsi(content)
	vis := visualWidth(clean)
	pad := ""
	if width > vis {
		pad = strings.Repeat(" ", width-vis)
	}
	return fmt.Sprintf("  %s%s%s  %s%s  %s%s%s", borderColor, border, Reset, content, pad, borderColor, border, Reset)
}

func cardHeader(title, subtitle, ver, borderColor string) string {
	top := fmt.Sprintf("  %s╭%s╮%s", borderColor, strings.Repeat("─", 71), Reset)
	bottom := fmt.Sprintf("  %s╰%s╮%s", borderColor, strings.Repeat("─", 71), Reset)
	bottom = fmt.Sprintf("  %s╰%s╯%s", borderColor, strings.Repeat("─", 71), Reset)
	empty := fmt.Sprintf("  %s│%s│%s", borderColor, strings.Repeat(" ", 71), Reset)

	spaceCount := 67 - visualWidth(stripAnsi(title)) - visualWidth(stripAnsi(ver))
	if spaceCount < 1 {
		spaceCount = 1
	}
	titleStr := fmt.Sprintf("%s%s%s%s%s%s%s", Bold, White, title, Reset, strings.Repeat(" ", spaceCount), Gray, ver)
	lines := []string{top, empty, formatBoxLine(titleStr, 67, "│", borderColor)}
	if subtitle != "" {
		lines = append(lines, formatBoxLine(fmt.Sprintf("%s%s%s", Dim, subtitle, Reset), 67, "│", borderColor))
	}
	lines = append(lines, empty, bottom)
	return strings.Join(lines, "\n")
}

func cardBorderTop(title string, borderColor string, double bool) string {
	left, right, h := "┌", "┐", "─"
	if double {
		left, right, h = "╔", "╗", "═"
	}
	if title != "" {
		vis := visualWidth(title)
		rem := 68 - vis
		if rem < 0 {
			rem = 0
		}
		return fmt.Sprintf("  %s%s%s %s%s%s%s %s%s%s", borderColor, left, h, Bold, White, title, Reset, borderColor, strings.Repeat(h, rem), right)
	}
	return fmt.Sprintf("  %s%s%s%s%s", borderColor, left, strings.Repeat(h, 71), right, Reset)
}

func cardBorderBottom(borderColor string, double bool) string {
	left, right, h := "└", "┘", "─"
	if double {
		left, right, h = "╚", "╝", "═"
	}
	return fmt.Sprintf("  %s%s%s%s%s", borderColor, left, strings.Repeat(h, 71), right, Reset)
}

func stripAnsi(str string) string {
	var b strings.Builder
	inEsc := false
	for _, r := range str {
		if r == '\033' {
			inEsc = true
			continue
		}
		if inEsc {
			if r == 'm' {
				inEsc = false
			}
			continue
		}
		b.WriteRune(r)
	}
	return b.String()
}

func visualWidth(str string) int {
	w := 0
	for _, r := range str {
		if r >= 0x1F300 || (r >= 0x1100 && r <= 0x115F) {
			w += 2
		} else {
			w += 1
		}
	}
	return w
}

func parseTargetAndArgs(args []string) (string, []string) {
	target := "."
	var remaining []string
	for i := 0; i < len(args); i++ {
		a := args[i]
		if a == "--target" || a == "-t" || a == "--root" {
			if i+1 < len(args) {
				target = args[i+1]
				i++
			}
		} else if strings.HasPrefix(a, "--target=") {
			target = strings.TrimPrefix(a, "--target=")
		} else if strings.HasPrefix(a, "--root=") {
			target = strings.TrimPrefix(a, "--root=")
		} else {
			remaining = append(remaining, a)
		}
	}
	if target == "." && len(remaining) > 0 && !strings.HasPrefix(remaining[0], "-") {
		target = remaining[0]
		remaining = remaining[1:]
	}
	return target, remaining
}

func findPython() string {
	for _, cmd := range []string{"python", "python3"} {
		if path, err := exec.LookPath(cmd); err == nil {
			return path
		}
	}
	return "python"
}

func printHelp() {
	fmt.Println()
	fmt.Println(cardHeader("🛡️  T O R U S G U A R D   C L I   ( G O )", "Autonomous Security Engine for AI-Built Applications", "v"+Version, Cyan))
	fmt.Printf("\n  %sUsage:%s  %storusguard%s %s[command]%s %s[options]%s\n\n", Bold, Reset, Green, Reset, White, Reset, Gray, Reset)

	fmt.Println(cardBorderTop("Commands", Cyan, false))
	fmt.Println(formatBoxLine(fmt.Sprintf("%sinit%s        Scaffold %s.torusguard/%s workspace + unlock rules", Green, Reset, Bold, Reset), 67, "│", Cyan))
	fmt.Println(formatBoxLine(fmt.Sprintf("%sstatus%s      Display active security posture, memory, rules, & stack", Green, Reset), 67, "│", Cyan))
	fmt.Println(formatBoxLine(fmt.Sprintf("%supdate%s      Check npm registry / releases for updates", Green, Reset), 67, "│", Cyan))
	fmt.Println(formatBoxLine(fmt.Sprintf("%saudit%s       Run static AST security scan on target project", Green, Reset), 67, "│", Cyan))
	fmt.Println(formatBoxLine(fmt.Sprintf("%sharden%s      Formulate minimal candidate patches (Ponytail bounded)", Green, Reset), 67, "│", Cyan))
	fmt.Println(formatBoxLine(fmt.Sprintf("%sapply%s       Apply candidate patches with automatic .bak snapshots", Green, Reset), 67, "│", Cyan))
	fmt.Println(formatBoxLine(fmt.Sprintf("%srecheck%s     Targeted differential verification of applied fixes", Green, Reset), 67, "│", Cyan))
	fmt.Println(formatBoxLine(fmt.Sprintf("%srecipes%s     List & inspect distilled Golden Fix Recipes in memory", Green, Reset), 67, "│", Cyan))
	fmt.Println(formatBoxLine(fmt.Sprintf("%srollback%s    Instantly revert files from latest pre-apply snapshot", Green, Reset), 67, "│", Cyan))
	fmt.Println(formatBoxLine(fmt.Sprintf("%sreport%s      Export OASIS SARIF v2.1.0 or single-file visual HTML report", Green, Reset), 67, "│", Cyan))
	fmt.Println(formatBoxLine(fmt.Sprintf("%shelp%s        Show this interactive command guide", Green, Reset), 67, "│", Cyan))
	fmt.Println(cardBorderBottom(Cyan, false))
	fmt.Println()
}

func runUpdate() {
	fmt.Println()
	fmt.Println(cardHeader("🛡️  TORUSGUARD UPDATE CHECK", "Package Distribution & Registry Verifier", "v"+Version, Cyan))
	fmt.Printf("\n  %sChecking npm registry for updates...%s\n\n", Dim, Reset)

	client := http.Client{Timeout: 6 * time.Second}
	resp, err := client.Get("https://registry.npmjs.org/torusguard/latest")
	if err != nil {
		fmt.Printf("  %s⚠ Registry unreachable: %v%s\n", Yellow, err, Reset)
		fmt.Printf("  %sRun: go install github.com/torusguard/torusguard/cmd/torusguard@latest%s\n\n", Cyan, Reset)
		return
	}
	defer resp.Body.Close()

	var data struct {
		Version string `json:"version"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		fmt.Printf("  %s⚠ Could not parse registry response%s\n\n", Yellow, Reset)
		return
	}

	fmt.Println(cardBorderTop("Version Telemetry", Cyan, false))
	fmt.Println(formatBoxLine(fmt.Sprintf("Installed Version: %sv%s%s", White, Version, Reset), 67, "│", Cyan))
	fmt.Println(formatBoxLine(fmt.Sprintf("Latest on NPM:     %s%sv%s%s", Bold, Green, data.Version, Reset), 67, "│", Cyan))
	fmt.Println(cardBorderBottom(Cyan, false))
	fmt.Println()

	if data.Version > Version {
		fmt.Println(cardBorderTop("Update Available", Yellow, true))
		fmt.Println(formatBoxLine(fmt.Sprintf("%sA new version of TorusGuard is available!%s", Yellow, Reset), 67, "║", Yellow))
		fmt.Println(formatBoxLine(fmt.Sprintf("Go:  %s%sgo install github.com/torusguard/torusguard/cmd/torusguard@latest%s", Bold, White, Reset), 67, "║", Yellow))
		fmt.Println(formatBoxLine(fmt.Sprintf("NPM: %s%snpm install -g torusguard@latest%s", Bold, White, Reset), 67, "║", Yellow))
		fmt.Println(cardBorderBottom(Yellow, true))
		fmt.Println()
	} else {
		fmt.Println(cardBorderTop("Status: Up To Date", Green, true))
		fmt.Println(formatBoxLine(fmt.Sprintf("%s✔ TorusGuard is up to date (v%s)%s", Green, Version, Reset), 67, "║", Green))
		fmt.Println(cardBorderBottom(Green, true))
		fmt.Println()
	}
}

func main() {
	if len(os.Args) < 2 {
		printHelp()
		return
	}

	command := os.Args[1]
	cliArgs := os.Args[2:]

	if command == "--version" || command == "-v" || command == "version" {
		fmt.Printf("torusguard v%s (go binary)\n", Version)
		return
	}

	if command == "help" || command == "--help" || command == "-h" {
		printHelp()
		return
	}

	if command == "update" {
		runUpdate()
		return
	}

	target, remaining := parseTargetAndArgs(cliArgs)
	absTarget, _ := filepath.Abs(target)
	pythonCmd := findPython()

	// Locate repo root or active workspace
	cwd, _ := os.Getwd()
	var scriptName string
	switch command {
	case "audit":
		scriptName = "audit_runner.py"
	case "status":
		scriptName = "status_runner.py"
	case "harden":
		scriptName = "harden_runner.py"
	case "apply":
		scriptName = "apply_runner.py"
	case "rollback":
		scriptName = "apply_runner.py"
		remaining = append([]string{"--rollback"}, remaining...)
	case "recheck", "verify":
		scriptName = "recheck_runner.py"
	case "recipes":
		scriptName = "recipes_runner.py"
	case "report":
		scriptName = "html_reporter.py"
	case "init":
		scriptPath := filepath.Join(cwd, "skills", "torusguard", "bootstrap.py")
		if _, err := os.Stat(scriptPath); err != nil {
			scriptPath = filepath.Join(cwd, "install.py")
		}
		pyArgs := append([]string{scriptPath, "--full-commands", "--target", absTarget}, remaining...)
		cmd := exec.Command(pythonCmd, pyArgs...)
		cmd.Dir = absTarget
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		cmd.Stdin = os.Stdin
		if err := cmd.Run(); err != nil {
			os.Exit(1)
		}
		return
	default:
		fmt.Fprintf(os.Stderr, "\n  %s✖ Unknown command:%s %s%s%s\n", Red, Reset, White, command, Reset)
		fmt.Fprintf(os.Stderr, "  Run %storusguard help%s for available commands.\n\n", Green, Reset)
		os.Exit(1)
	}

	// Resolve runner script path
	scriptPath := filepath.Join(absTarget, ".torusguard", "scripts", scriptName)
	if _, err := os.Stat(scriptPath); err != nil {
		scriptPath = filepath.Join(cwd, ".torusguard", "scripts", scriptName)
	}

	pyArgs := append([]string{scriptPath, absTarget}, remaining...)
	cmd := exec.Command(pythonCmd, pyArgs...)
	cmd.Dir = absTarget
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.Stdin = os.Stdin
	if err := cmd.Run(); err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok {
			os.Exit(exitErr.ExitCode())
		}
		os.Exit(1)
	}
}
