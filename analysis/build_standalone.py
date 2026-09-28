"""
build_standalone.py — รวมแต่ละเว็บเป็นไฟล์ HTML ไฟล์เดียว (ดับเบิลคลิกเปิดได้เลย ไม่ต้องมีเซิร์ฟเวอร์)

  dist/india-crime-d3.html        จาก web/d3/
  dist/india-crime-echarts.html   จาก web/echarts/

ฝัง style.css, common.js, charts.js และข้อมูล JSON ลงในไฟล์ ไลบรารี (D3 / ECharts) ยังโหลดจาก cdnjs จึงต้องต่ออินเทอร์เน็ต
รัน:  python analysis/build_standalone.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def build(site: str) -> Path:
    src = ROOT / "web" / site
    html = (src / "index.html").read_text(encoding="utf-8")
    css = (src / "style.css").read_text(encoding="utf-8")
    data = (src / "data" / "dashboard.json").read_text(encoding="utf-8")
    geo = (src / "data" / "india_states.geojson").read_text(encoding="utf-8")
    js = lambda name: (src / name).read_text(encoding="utf-8").replace("</script", "<\\/script")

    html = html.replace('<link rel="stylesheet" href="style.css">', f"<style>\n{css}\n</style>")
    html = html.replace('<script src="data/dashboard.js"></script>', f"<script>window.__DATA__ = {data};</script>")
    html = html.replace('<script src="data/india_states.js"></script>', f"<script>window.__GEO__ = {geo};</script>")
    html = html.replace('<script src="common.js"></script>', f"<script>\n{js('common.js')}\n</script>")
    html = html.replace('<script src="charts.js"></script>', f"<script>\n{js('charts.js')}\n</script>")
    assert 'src="data/' not in html and 'src="common.js"' not in html and 'src="charts.js"' not in html and 'href="style.css"' not in html
    DIST.mkdir(exist_ok=True)
    out = DIST / f"india-crime-{site}.html"
    out.write_text(html, encoding="utf-8")
    return out


if __name__ == "__main__":
    for s in ("d3", "echarts"):
        p = build(s)
        print(f"wrote {p.relative_to(ROOT)} ({p.stat().st_size / 1024:.0f} KB)")
