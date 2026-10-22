from pathlib import Path
from PIL import Image, ImageStat
from playwright.sync_api import sync_playwright

out = Path("docs/screenshots")
out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    for name, page_path, width, height in [("desktop", "", 1280, 840), ("mobile", "career.html", 390, 844)]:
        context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1, locale="ru-RU", reduced_motion="reduce")
        page = context.new_page()
        response = page.goto("http://127.0.0.1:8765/" + page_path, wait_until="networkidle")
        if response is None or response.status >= 400:
            raise RuntimeError("Page unavailable: " + page_path)
        page.locator("h1").first.wait_for(state="visible")
        png = out / (name + ".png")
        page.screenshot(path=str(png), animations="disabled")
        with Image.open(png) as im:
            rgb = im.convert("RGB")
            if max(ImageStat.Stat(rgb.resize((64, 64))).stddev) < 4:
                raise RuntimeError("Screenshot appears blank")
            rgb.save(out / (name + ".webp"), "WEBP", quality=76, method=6)
        png.unlink()
        context.close()
    browser.close()
