# Renders the README images from HTML with headless Chromium.
# uv run --with playwright python assets/render.py
import base64
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
MASCOT = "data:image/png;base64," + base64.b64encode((HERE / "mascot-sticker.png").read_bytes()).decode()
FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800'
    '&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">'
)
BASE = """
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0d1117;--ink:#f0f6fc;--mute:#8b949e;--line:#30363d;--card:#161b22;--lime:#b5c858;--lime-ink:#1a1f0a}
body{background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",sans-serif;-webkit-font-smoothing:antialiased}
code{font-family:"JetBrains Mono",monospace;font-size:.86em;background:rgba(240,246,252,.08);border:1px solid rgba(240,246,252,.12);border-radius:6px;padding:1px 6px}
"""

SOCIAL = f"""<html><head>{FONTS}<style>{BASE}
body{{width:1280px;height:640px;overflow:hidden;position:relative}}
.glow{{position:absolute;right:-120px;top:-80px;width:760px;height:760px;border-radius:50%;
  background:radial-gradient(circle,rgba(181,200,88,.20),rgba(181,200,88,0) 65%)}}
.left{{position:absolute;left:84px;top:96px;width:720px}}
h1{{font-family:"Bricolage Grotesque";font-weight:800;font-size:168px;line-height:.9;letter-spacing:-5px}}
.tag{{margin-top:22px;font-family:"Bricolage Grotesque";font-weight:500;font-size:38px;color:var(--mute);letter-spacing:-.5px}}
.tag b{{color:var(--ink);font-weight:700}}
.chat{{margin-top:46px;display:flex;flex-direction:column;gap:14px;align-items:flex-start}}
.b{{border-radius:22px;padding:14px 22px;font-size:25px;line-height:1.3;max-width:640px}}
.old{{background:#21262d;color:#6e7681;text-decoration:line-through;text-decoration-color:#f85149;text-decoration-thickness:2px}}
.new{{background:var(--lime);color:var(--lime-ink);font-weight:500}}
.new code{{background:rgba(26,31,10,.12);border-color:rgba(26,31,10,.2);color:var(--lime-ink)}}
.m{{position:absolute;right:70px;bottom:28px;height:560px}}
</style></head><body><div class="glow"></div>
<div class="left">
<h1>lowkey</h1>
<div class="tag">your agent, but it <b>talks like a person</b></div>
<div class="chat">
<div class="b old">Great question! After analyzing the CI logs, I've identified the root cause.</div>
<div class="b new"><code>test_upload</code> timed out, want me to fix it?</div>
</div></div>
<img class="m" src="{MASCOT}"></body></html>"""

DEMO = f"""<html><head>{FONTS}<style>{BASE}
body{{width:1600px;padding:56px 64px 64px}}
.top{{display:flex;align-items:center;gap:18px;margin-bottom:34px}}
.top h2{{font-family:"Bricolage Grotesque";font-weight:700;font-size:40px;letter-spacing:-1px}}
.top span{{color:var(--mute);font-size:24px}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:36px}}
.col{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:30px 32px 34px}}
.label{{font-family:"JetBrains Mono";font-size:18px;letter-spacing:1px;text-transform:uppercase;color:var(--mute);margin-bottom:22px}}
.col.lk .label{{color:var(--lime)}}
.you{{display:flex;justify-content:flex-end;margin-bottom:22px}}
.you div{{background:#1f6feb;color:#fff;border-radius:20px 20px 6px 20px;padding:12px 20px;font-size:23px}}
.bot{{font-size:23px;line-height:1.55;color:#e6edf3}}
.bot p{{margin-bottom:12px}}
.bot ul{{margin:0 0 12px 26px}} .bot li{{margin-bottom:6px}}
.lk .bot{{font-size:24px}}
.lk .bot p{{margin-bottom:6px}}
.count{{margin-top:18px;font-family:"JetBrains Mono";font-size:17px;color:var(--mute)}}
.lk .count{{color:var(--lime)}}
</style></head><body>
<div class="top"><h2>same question, two agents</h2><span>example reply, same facts in both</span></div>
<div class="cols">
<div class="col"><div class="label">default</div>
<div class="you"><div>why is ci red again</div></div>
<div class="bot">
<p>Great question! After analyzing the CI logs, I've identified the root cause of the failure. The <code>test_upload</code> test is failing due to a timeout. Here's a breakdown:</p>
<ul><li><b>Cause:</b> The mock server takes longer than 5 seconds to start, which exceeds the default timeout.</li>
<li><b>Fix:</b> Increase the timeout, or start the server once per module instead of once per test.</li></ul>
<p>Let me know if you'd like me to implement this fix!</p></div>
<div class="count">70 words · 1 opener · 2 bold headers · 1 closer</div></div>
<div class="col lk"><div class="label">with lowkey</div>
<div class="you"><div>why is ci red again</div></div>
<div class="bot">
<p><code>test_upload</code> timed out, the mock server takes longer than 5s to boot</p>
<p>i can start it once per module instead of per test, want me to?</p></div>
<div class="count">26 words · same facts · no tells</div></div>
</div></body></html>"""


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/Applications/Chromium.app/Contents/MacOS/Chromium", headless=True)
        page = b.new_page(viewport={"width": 1280, "height": 640}, device_scale_factor=1)
        page.set_content(SOCIAL, wait_until="networkidle")
        page.wait_for_timeout(500)
        page.screenshot(path=str(HERE / "social-preview.png"))

        page = b.new_page(viewport={"width": 1600, "height": 600}, device_scale_factor=2)
        page.set_content(DEMO, wait_until="networkidle")
        page.wait_for_timeout(500)
        page.screenshot(path=str(HERE / "demo.png"), full_page=True)
        b.close()


if __name__ == "__main__":
    main()
