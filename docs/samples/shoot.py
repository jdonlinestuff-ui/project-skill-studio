"""Screenshot the REAL dashboard-reference.html in each of its real schemes.

Uses Playwright (a real Chromium) against the actual file -- not a parallel mockup
system. That's deliberate: an earlier SVG-based generator drifted from the reference
build's actual scheme names (Ink/Parchment/Mono print/Dark console vs the real
Canon/Slate/Dark/Mono) and was retired in v1.7.0. Screenshot the real thing; never
re-describe it in a second renderer.

Run from the docs/samples directory: python3 shoot.py
Outputs to ./screenshots/. Requires: pip install playwright && playwright install chromium
"""
import re, os
from playwright.sync_api import sync_playwright

SRC = os.path.abspath("../../references/dashboard-reference.html")
SCHEMES = ["canon", "slate", "dark", "mono"]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1040, "height": 800})
    page.goto(f"file://{SRC}")
    page.wait_for_timeout(400)  # let loadData() resolve (no TRACKER_SOURCE -> EMBEDDED snapshot)

    # sanity: confirm the feedback section actually rendered before shooting anything
    fb_count = page.eval_on_selector("#feedback", "el => el.querySelectorAll('.row').length")
    print("feedback rows found in live DOM:", fb_count)
    banner_visible = page.eval_on_selector("#srcbanner", "el => !el.hidden")
    print("snapshot banner visible:", banner_visible)

    for scheme in SCHEMES:
        page.evaluate(f"setScheme('{scheme}')")
        page.wait_for_timeout(150)
        page.screenshot(path=f"screenshots/full_{scheme}.png", full_page=True)
        # focused crop: use Playwright's own element screenshot (handles scroll/viewport correctly)
        page.locator("#sec-feedback").screenshot(path=f"screenshots/feedback_{scheme}.png")


    browser.close()
print("done")
