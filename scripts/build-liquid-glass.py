"""Bake CSS glass settings and SVG templates into import.css"""

import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote

root = Path(__file__).resolve().parents[1]
svg_ns = "http://www.w3.org/2000/svg"
ns = {"svg": svg_ns}
ET.register_namespace("", svg_ns)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
css_path = root / "src/import.css"
css = css_path.read_text()
settings_css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def setting(name, minimum, maximum, unit=""):
    key = "--shine-glass-" + name
    matches = re.findall(
        r"(?<![\w-])" + re.escape(key) + r"\s*:\s*([^;]+);", settings_css
    )
    if len(matches) != 1:
        raise SystemExit(f"Expected one {key} declaration")
    match = re.fullmatch(
        r"([+-]?(?:\d+(?:\.\d*)?|\.\d+))" + re.escape(unit), matches[0].strip()
    )
    if not match:
        raise SystemExit(f"{key} must be a number{(' in ' + unit) if unit else ''}")
    value = float(match[1])
    if not math.isfinite(value) or not minimum <= value <= maximum:
        raise SystemExit(f"{key} must be {minimum}..{maximum}{unit}")
    return value


def number(value):
    return format(value, ".12g")


def compact_svg(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r">\s+<", "><", text.strip())
    return re.sub(r"\s+", " ", text)


radius = setting("radius", 0, 256, "px")
distortion = setting("distortion", 0, 150)
center_distortion = setting("center-distortion", 0, 255)
center_size = setting("center-size", 0, 20)
iridescence = setting("iridescence", 0, 50)
rim_width = setting("rim-width", 0, 128, "px")

map_tree = ET.fromstring((root / "src/liquid-glass-map.svg").read_text())
outline = map_tree.find(".//svg:clipPath/svg:rect", ns)
center = map_tree.find("svg:g/svg:rect[@filter]", ns)
soften = map_tree.find(".//svg:feGaussianBlur", ns)
if outline is None or center is None or soften is None:
    raise SystemExit(
        "Displacement map template is missing its outline, center, or blur"
    )
outline.set("rx", number(radius))
center.set("x", number(rim_width))
center.set("y", number(rim_width))
center.set("rx", number(max(0, radius - rim_width)))
center.set("fill-opacity", number(1 - center_distortion / 255))
center.set(
    "style",
    f"width:calc(100% - {number(rim_width * 2)}px);height:calc(100% - {number(rim_width * 2)}px)",
)
soften.set("stdDeviation", number(20 - center_size))
map_svg = compact_svg(ET.tostring(map_tree, encoding="unicode"))
map_uri = "data:image/svg+xml," + quote(map_svg, safe="")
filter_tree = ET.fromstring((root / "src/liquid-glass.svg").read_text())
channels = filter_tree.findall(".//svg:feDisplacementMap", ns)
offset = filter_tree.find(".//svg:feOffset", ns)
if len(channels) != 3 or offset is None:
    raise SystemExit(
        "Filter template must have three RGB displacements and a neutral offset"
    )
for channel, separation in zip(channels, (1, 0, -1)):
    channel.set("scale", number(-distortion + separation * iridescence / 10))
offset.set("dx", number(distortion / 510))
offset.set("dy", number(distortion / 510))
svg = compact_svg(ET.tostring(filter_tree, encoding="unicode"))
map_reference = 'xlink:href="liquid-glass-map.svg"'
if svg.count(map_reference) != 1:
    raise SystemExit("Expected one displacement map reference")
svg = svg.replace(map_reference, 'xlink:href="' + map_uri + '"')
uri = "data:image/svg+xml," + quote(svg, safe="") + "#liquid-glass"
css, count = re.subn(
    r'--liquid-glass-filter:\s*url\("[^"\n]*"\);',
    '--liquid-glass-filter: url("' + uri + '");',
    css,
)
if count != 1:
    raise SystemExit(f"Expected one filter declaration, found {count}")
css_path.write_text(css)
print("Updated --liquid-glass-filter in src/import.css")
