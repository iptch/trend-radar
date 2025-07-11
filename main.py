import re
import pandas as pd
from wordcloud import WordCloud
from lxml import etree
from pathlib import Path

WIDTH = 1600
WIDTH_SHIFT = 400
HEIGHT = 800
HEIGHT_SHIFT = 100

FILENAME = "trend-radar.svg"

DESCRIPTION_WIDTH = 60

CSS_STYLES = """
    text {
        font-family: 'Droid Sans Mono';
        font-weight: normal;
        font-style: normal;
    }
    .tooltip {
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.3s;
    }
    svg {
        margin: 10px 20px;
        max-height: 100%;
        overflow: visible;
    }
"""

JS_SCRIPT = """
    document.addEventListener('DOMContentLoaded', () => {
      const textElements = document.querySelectorAll('text[id^="trend"]');
      textElements.forEach(textElement => {
        textElement.addEventListener('mouseover', (event) => {
          const textId = event.target.id; // Get the ID of the hovered text element
          const tooltipId = 'tooltip' + textId.replace('trend', '');
          const tooltipElement = document.getElementById(tooltipId);

          if (tooltipElement) {
            tooltipElement.style.opacity = 1;
          }
        });

        textElement.addEventListener('mouseout', (event) => {
          const textId = event.target.id;
          const tooltipId = 'tooltip' + textId.replace('trend', '');
          const tooltipElement = document.getElementById(tooltipId);

          if (tooltipElement) {
            tooltipElement.style.opacity = 0;
          }
        });
      });
    });
"""

TRANSFORM_PATTERN = re.compile(r"translate\((\d+),(\d+)\)")


def tag(t):
    return f"{{http://www.w3.org/2000/svg}}{t}"


def load_data():
    return pd.read_csv("./trends.csv")


def generate_wordcloud(frequencies):
    wordcloud = WordCloud(
        width=WIDTH, height=HEIGHT, background_color="white"
    ).generate_from_frequencies(frequencies)
    return etree.fromstring(wordcloud.to_svg())


def update_style(svg):
    svg.remove(svg.find(tag("style")))
    style = etree.Element("style", type="text/css")
    style.text = etree.CDATA(CSS_STYLES)
    svg.insert(0, style)
    return svg


def add_script(svg):
    script = etree.Element("script", type="text/javascript")
    script.text = etree.CDATA(JS_SCRIPT)
    svg.insert(0, script)
    return svg


def add_filter(svg):
    filter_defs = """
      <defs>
        <filter x="0" y="0" width="1" height="1" id="solid">
          <feFlood flood-color="black" result="bg" />
          <feMerge>
            <feMergeNode in="bg"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
    """
    node = etree.fromstring(filter_defs)
    svg.insert(1, node)
    return svg


def split_line_on_wrap(description):
    return [
        line.strip()
        for line in re.findall(r".{1," + str(DESCRIPTION_WIDTH) + r"}(?:\s+|$)", description)
    ]


def clip_translation(transform):
    x, y = map(int, TRANSFORM_PATTERN.match(transform).groups())
    if y > (HEIGHT - HEIGHT_SHIFT):
        y = y - HEIGHT_SHIFT
    if x > (WIDTH - WIDTH_SHIFT):
        x = x - WIDTH_SHIFT
    return f"translate({x}, {y})"


def add_tooltips(svg, tooltips):
    trends = svg.findall(tag("text"))
    for idx, trend in enumerate(trends):
        # see JS code regarding ids
        trend.attrib["id"] = f"trend{idx}"
        g = etree.Element("g")
        g.attrib["id"] = f"tooltip{idx}"
        g.attrib["class"] = "tooltip css"
        g.attrib["transform"] = clip_translation(trend.attrib["transform"])
        text = etree.Element("text")
        text.attrib["fill"] = "LightSeaGreen"
        text.attrib["filter"] = "url(#solid)"
        for line in split_line_on_wrap(tooltips[trend.text]):
            tspan = etree.Element("tspan")
            tspan.attrib["x"] = "0"
            tspan.attrib["dy"] = "1.2em"
            tspan.text = line
            text.append(tspan)
        g.append(text)
        svg.append(g)
    return svg


def main():
    data = load_data()
    frequencies = {}
    for _, row in data.iterrows():
        frequencies[row["trend"]] = float(row["weight"])
    svg = generate_wordcloud(frequencies)
    svg = update_style(svg)
    svg = add_script(svg)
    svg = add_filter(svg)
    tooltips = {}
    for _, row in data.iterrows():
        tooltips[row["trend"]] = row["description"]
    svg = add_tooltips(svg, tooltips)
    Path(FILENAME).write_bytes(etree.tostring(svg))


if __name__ == "__main__":
    main()
