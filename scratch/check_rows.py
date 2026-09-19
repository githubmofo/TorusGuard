from pathlib import Path
import re

html = Path("report.html").read_text(encoding="utf-8")

p_mid = html.find('<div class="row-middle">')
p_bot = html.find('<div class="row-bottom">')
p_foot = html.find('<footer class="footer-compact">')

print("--- ROW MIDDLE ---")
print(html[p_mid:p_bot])

print("--- ROW BOTTOM ---")
print(html[p_bot:p_foot])
