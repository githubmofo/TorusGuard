package main

import (
	"fmt"

	"github.com/torusguard/torusguard/internal/scanner"
	"github.com/torusguard/torusguard/internal/termui"
)

type BenchmarkCase struct {
	Name        string
	Code        string
	Ext         string
	ExpectAlert bool
	RuleID      string
}

// RunBenchmark executes the autonomous SecurityReviewBench evaluation harness
func RunBenchmark() error {
	fmt.Println()
	fmt.Println(termui.CardHeader("🎯  SECURITY REVIEW BENCHMARK", "Self-Evaluating Precision & Recall Suite", "v"+Version, termui.Cyan))

	cases := []BenchmarkCase{
		{
			Name:        "Unsafe SQL Concatenation",
			Code:        `db.query("SELECT * FROM users WHERE id = " + userId)`,
			Ext:         ".js",
			ExpectAlert: true,
			RuleID:      "TG-DB-002",
		},
		{
			Name:        "Safe Parameterized Query",
			Code:        `db.query("SELECT * FROM users WHERE id = $1", [userId])`,
			Ext:         ".js",
			ExpectAlert: false,
			RuleID:      "TG-DB-002",
		},
		{
			Name:        "Exposed OpenAI API Token",
			Code:        `const apiKey = "sk-live-abcdef1234567890abcdef1234567890"`,
			Ext:         ".ts",
			ExpectAlert: true,
			RuleID:      "TG-SEC-001",
		},
		{
			Name:        "Safe Environment Variable Secret",
			Code:        `const apiKey = process.env.OPENAI_API_KEY`,
			Ext:         ".ts",
			ExpectAlert: false,
			RuleID:      "TG-SEC-001",
		},
		{
			Name:        "Unsafe Path Traversal readFile",
			Code:        `fs.readFile(path.join("/var/data", req.query.file))`,
			Ext:         ".js",
			ExpectAlert: true,
			RuleID:      "TG-INPUT-002",
		},
		{
			Name:        "Safe Path Basename",
			Code:        `const safeFile = path.basename(req.query.file); fs.readFile(path.join("/var/data", safeFile))`,
			Ext:         ".js",
			ExpectAlert: false,
			RuleID:      "TG-INPUT-002",
		},
		{
			Name:        "Unsafe DOM XSS dangerouslySetInnerHTML",
			Code:        `<div dangerouslySetInnerHTML={{ __html: userInput }} />`,
			Ext:         ".tsx",
			ExpectAlert: true,
			RuleID:      "TG-INPUT-004",
		},
		{
			Name:        "Safe React Text Element",
			Code:        `<div>{userInput}</div>`,
			Ext:         ".tsx",
			ExpectAlert: false,
			RuleID:      "TG-INPUT-004",
		},
		{
			Name:        "Disabled TLS InsecureSkipVerify Bypass",
			Code:        "return &tls.Config{" + "Insecure" + "SkipVerify: true}",
			Ext:         ".go",
			ExpectAlert: true,
			RuleID:      "TG-DIFF-001",
		},
		{
			Name:        "Safe TLS InsecureSkipVerify False",
			Code:        `return &tls.Config{InsecureSkipVerify: false}`,
			Ext:         ".go",
			ExpectAlert: false,
			RuleID:      "TG-DIFF-001",
		},
		{
			Name:        "Catastrophic ReDoS Regex",
			Code:        `^([a-zA-Z0-9]+)+$`,
			Ext:         ".js",
			ExpectAlert: true,
			RuleID:      "TG-REDOS-001",
		},
		{
			Name:        "Safe Linear Regex",
			Code:        `^[a-zA-Z0-9]+$`,
			Ext:         ".js",
			ExpectAlert: false,
			RuleID:      "TG-REDOS-001",
		},
	}

	tp := 0
	fp := 0
	tn := 0
	fn := 0
	sim := scanner.NewThompsonNFASimulator()

	for _, bc := range cases {
		flagged := false

		if bc.RuleID == "TG-REDOS-001" {
			res := sim.Analyze(bc.Code)
			flagged = res.IsVulnerable
		} else {
			for _, r := range scanner.BuiltinRules {
				if r.RuleID != bc.RuleID {
					continue
				}

				if len(r.FileExts) > 0 {
					extMatched := false
					for _, fe := range r.FileExts {
						if bc.Ext == fe {
							extMatched = true
							break
						}
					}
					if !extMatched {
						continue
					}
				}

				if r.Regex.MatchString(bc.Code) {
					flagged = true
					break
				}
			}
		}

		if bc.ExpectAlert && flagged {
			tp++
		} else if !bc.ExpectAlert && flagged {
			fp++
		} else if !bc.ExpectAlert && !flagged {
			tn++
		} else if bc.ExpectAlert && !flagged {
			fn++
		}
	}

	total := len(cases)
	precision := 1.0
	if tp+fp > 0 {
		precision = float64(tp) / float64(tp+fp)
	}

	recall := 1.0
	if tp+fn > 0 {
		recall = float64(tp) / float64(tp+fn)
	}

	f1 := 0.0
	if precision+recall > 0 {
		f1 = 2 * (precision * recall) / (precision + recall)
	}

	fmt.Println(termui.CardBorderTop("SecurityReviewBench Benchmark Results", termui.Cyan, false))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("Evaluated Challenges: %d synthetic ground-truth pairs", total), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("True Positives: %d | True Negatives: %d", tp, tn), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("False Positives: %d | False Negatives: %d", fp, fn), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sPrecision:%s %5.1f%% (High-fidelity detection)", termui.Green, termui.Reset, precision*100), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sRecall:   %s %5.1f%% (Comprehensive coverage)", termui.Green, termui.Reset, recall*100), 67, "│", termui.Cyan))
	fmt.Println(termui.FormatBoxLine(fmt.Sprintf("%sF1 Score: %s %5.1f%% (Overall harmonic accuracy)", termui.Green, termui.Reset, f1*100), 67, "│", termui.Cyan))
	fmt.Println(termui.CardBorderBottom(termui.Cyan, false))
	fmt.Println()

	return nil
}
