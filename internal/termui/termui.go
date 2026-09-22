package termui

import (
	"fmt"
	"strings"
)

const (
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

func StripAnsi(str string) string {
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

func VisualWidth(str string) int {
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

func FormatBoxLine(content string, width int, border string, borderColor string) string {
	clean := StripAnsi(content)
	vis := VisualWidth(clean)
	pad := ""
	if width > vis {
		pad = strings.Repeat(" ", width-vis)
	}
	return fmt.Sprintf("  %s%s%s  %s%s  %s%s%s", borderColor, border, Reset, content, pad, borderColor, border, Reset)
}

func CardHeader(title, subtitle, ver, borderColor string) string {
	top := fmt.Sprintf("  %s╭%s╮%s", borderColor, strings.Repeat("─", 71), Reset)
	bottom := fmt.Sprintf("  %s╰%s╯%s", borderColor, strings.Repeat("─", 71), Reset)
	empty := fmt.Sprintf("  %s│%s│%s", borderColor, strings.Repeat(" ", 71), Reset)

	spaceCount := 67 - VisualWidth(StripAnsi(title)) - VisualWidth(StripAnsi(ver))
	if spaceCount < 1 {
		spaceCount = 1
	}
	titleStr := fmt.Sprintf("%s%s%s%s%s%s%s", Bold, White, title, Reset, strings.Repeat(" ", spaceCount), Gray, ver)
	lines := []string{top, empty, FormatBoxLine(titleStr, 67, "│", borderColor)}
	if subtitle != "" {
		lines = append(lines, FormatBoxLine(fmt.Sprintf("%s%s%s", Dim, subtitle, Reset), 67, "│", borderColor))
	}
	lines = append(lines, empty, bottom)
	return strings.Join(lines, "\n")
}

func CardBorderTop(title string, borderColor string, double bool) string {
	left, right, h := "┌", "┐", "─"
	if double {
		left, right, h = "╔", "╗", "═"
	}
	if title != "" {
		vis := VisualWidth(title)
		rem := 68 - vis
		if rem < 0 {
			rem = 0
		}
		return fmt.Sprintf("  %s%s%s %s%s%s%s %s%s%s", borderColor, left, h, Bold, White, title, Reset, borderColor, strings.Repeat(h, rem), right)
	}
	return fmt.Sprintf("  %s%s%s%s%s", borderColor, left, strings.Repeat(h, 71), right, Reset)
}

func CardBorderBottom(borderColor string, double bool) string {
	left, right, h := "└", "┘", "─"
	if double {
		left, right, h = "╚", "╝", "═"
	}
	return fmt.Sprintf("  %s%s%s%s%s", borderColor, left, strings.Repeat(h, 71), right, Reset)
}
