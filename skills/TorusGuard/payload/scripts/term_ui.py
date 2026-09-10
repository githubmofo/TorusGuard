#!/usr/bin/env python3
"""
TorusGuard Unified Terminal UI Engine (v1.3.3)
Provides mathematically exact 75-column card formatting, ANSI-stripping,
Unicode/emoji visual width calculation, and visual truncation with ellipsis.
Pure Python 3.10+ standard library (zero external dependencies).
"""

import sys
import os
import re
import unicodedata
from typing import Optional

# Ensure UTF-8 stdout/stderr on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        getattr(sys.stdout, "reconfigure")(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        getattr(sys.stderr, "reconfigure")(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ─── ANSI Colors & Styles ─────────────────────────────────────────────────────
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
WHITE = "\033[97m"
GRAY = "\033[90m"
RED = "\033[31m"
MAGENTA = "\033[35m"
BG_GREEN = "\033[42m"
BG_CYAN = "\033[46m"

ANSI_REGEX = re.compile(r'\x1b\[[0-9;]*m|\033\[[0-9;]*m')

def strip_ansi(text: str) -> str:
    """Remove all ANSI color and style escape sequences."""
    return ANSI_REGEX.sub('', text)

def get_visual_width(text: str) -> int:
    """
    Calculate the printable display width of a string in terminal columns.
    Accounts for ANSI escapes, Unicode variation selectors, emojis, and fullwidth chars.
    """
    clean = strip_ansi(text)
    width = 0
    for ch in clean:
        cp = ord(ch)
        # Variation selectors (VS1-16, VS17-256) occupy 0 terminal columns
        if (0xFE00 <= cp <= 0xFE0F) or (0xE0100 <= cp <= 0xE01EF):
            continue
        # Zero-width spaces, joiners, soft hyphens
        if cp in (0x200B, 0x200C, 0x200D, 0x00AD):
            continue
        ea = unicodedata.east_asian_width(ch)
        if ea in ('W', 'F'):
            width += 2
        elif cp >= 0x1F300: # Emojis and miscellaneous pictographs
            width += 2
        elif cp in (0x26A0, 0x2714, 0x2716, 0x2139): # ⚠, ✔, ✖, ℹ
            width += 1
        else:
            width += 1
    return width

def truncate_visual(text: str, max_w: int = 67) -> str:
    """Truncate text visually to max_w columns without breaking ANSI escape codes."""
    if get_visual_width(text) <= max_w:
        return text
    out = []
    curr_w = 0
    in_ansi = False
    ansi_buf = ''
    for ch in text:
        if ch in ('\033', '\x1b'):
            in_ansi = True
            ansi_buf = ch
            continue
        if in_ansi:
            ansi_buf += ch
            if ch == 'm':
                in_ansi = False
                out.append(ansi_buf)
            continue
        cp = ord(ch)
        if (0xFE00 <= cp <= 0xFE0F) or (0xE0100 <= cp <= 0xE01EF) or cp in (0x200B, 0x200C, 0x200D, 0x00AD):
            out.append(ch)
            continue
        ea = unicodedata.east_asian_width(ch)
        cw = 2 if (ea in ('W', 'F') or cp >= 0x1F300) else 1
        if curr_w + cw > max_w - 3:
            out.append(RESET + '...')
            curr_w += 3
            break
        out.append(ch)
        curr_w += cw
    out.append(RESET)
    return ''.join(out)

def format_box_line(content: str, width: int = 67, border: str = "│", border_color: str = CYAN) -> str:
    """
    Pad content so the card line is strictly 75 visual columns total width.
    Layout: '  ' (2) + border (1) + '  ' (2) + content/pad (width=67) + '  ' (2) + border (1) = 75 cols.
    """
    trunc = truncate_visual(content, width)
    vis = get_visual_width(trunc)
    pad = " " * max(0, width - vis)
    return f"  {border_color}{border}{RESET}  {trunc}{pad}  {border_color}{border}{RESET}"

def card_border_top(title: str = "", border_color: str = CYAN, double: bool = False) -> str:
    """Generate 75-column top border (single ┌ or double ╔) with optional title."""
    left = "╔" if double else "┌"
    right = "╗" if double else "┐"
    h = "═" if double else "─"
    if title:
        vis = get_visual_width(title)
        rem = max(0, 68 - vis)
        return f"  {border_color}{left}{h} {BOLD}{WHITE}{title}{RESET}{border_color} {h * rem}{right}{RESET}"
    return f"  {border_color}{left}{h * 71}{right}{RESET}"

def card_border_bottom(border_color: str = CYAN, double: bool = False) -> str:
    """Generate 75-column bottom border (single └ or double ╚)."""
    left = "╚" if double else "└"
    right = "╝" if double else "┘"
    h = "═" if double else "─"
    return f"  {border_color}{left}{h * 71}{right}{RESET}"

def card_divider(title: str = "", border_color: str = CYAN, double: bool = False) -> str:
    """Generate 75-column divider (single ├ or double ╠) with optional title."""
    left = "╠" if double else "├"
    right = "╣" if double else "┤"
    h = "═" if double else "─"
    if title:
        vis = get_visual_width(title)
        rem = max(0, 68 - vis)
        return f"  {border_color}{left}{h} {BOLD}{WHITE}{title}{RESET}{border_color} {h * rem}{right}{RESET}"
    return f"  {border_color}{left}{h * 71}{right}{RESET}"

def card_header(title: str, subtitle: str = "", version: str = "v1.3.4", border_color: str = CYAN) -> str:
    """Generate standardized 75-column curved header box."""
    top = f"  {border_color}╭{'─' * 71}╮{RESET}"
    bottom = f"  {border_color}╰{'─' * 71}╯{RESET}"
    empty = f"  {border_color}│{' ' * 71}│{RESET}"

    # Calculate padding between title and version
    title_vis = get_visual_width(title)
    ver_vis = get_visual_width(version)
    space_count = max(1, 67 - title_vis - ver_vis)
    title_str = f"{BOLD}{WHITE}{title}{RESET}{' ' * space_count}{GRAY}{version}{RESET}"

    lines = [top, empty, format_box_line(title_str, width=67, border_color=border_color)]
    if subtitle:
        lines.append(format_box_line(f"{DIM}{subtitle}{RESET}", width=67, border_color=border_color))
    lines.extend([empty, bottom])
    return "\n".join(lines)
