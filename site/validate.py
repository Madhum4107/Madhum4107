"""Basic portfolio HTML checks using the Python standard library."""
from html.parser import HTMLParser
from pathlib import Path
import sys

HTML_PATH = Path(__file__).parent / "index.html"
CSS_PATH = Path(__file__).parent / "style.css"
JS_PATH = Path(__file__).parent / "script.js"

class PortfolioParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.title_text = []
        self.in_title = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "title":
            self.in_title = True
    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
    def handle_data(self, data):
        if self.in_title:
            self.title_text.append(data)

parser = PortfolioParser()
parser.feed(HTML_PATH.read_text(encoding="utf-8"))
parser.close()
assert parser.title_text, "Page title missing"
assert {"home", "work", "about", "signal", "contact"} <= parser.ids, "Required section IDs missing"
for href in parser.links:
    if href.startswith("#"):
        assert href[1:] in parser.ids, f"Broken internal anchor: {href}"
assert CSS_PATH.exists() and JS_PATH.exists(), "CSS or JavaScript asset missing"
for required in ["CampaignLift-AI", "modelguard-ai", "Data-Insight-AI", "Retail-Intelligence-Platform"]:
    assert required in HTML_PATH.read_text(encoding="utf-8"), f"Project link/content missing: {required}"
print(f"Portfolio HTML checks passed. {len(parser.ids)} IDs, {len(parser.links)} links.")
