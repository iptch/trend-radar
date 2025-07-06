import pandas as pd
from wordcloud import WordCloud
from lxml import etree
from pathlib import Path

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
    text:hover + g.tooltip.css {
      opacity: 1;
    }
    svg {
        margin: 10px 20px;
        max-height: 100%;
        overflow: visible;
    }
"""


def tag(t):
    return f"{{http://www.w3.org/2000/svg}}{t}"


def load_data():
    return pd.read_csv("./trends.csv")


def generate_wordcloud(frequencies):
    wordcloud = WordCloud(
        width=800, height=400, background_color="white"
    ).generate_from_frequencies(frequencies)
    return etree.fromstring(wordcloud.to_svg())


def update_style(svg):
    svg.remove(svg.find(tag("style")))
    style = etree.Element("style", type="text/css")
    style.text = etree.CDATA(CSS_STYLES)
    svg.insert(0, style)
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


def add_tooltips(svg, tooltips):
    trends = svg.findall(tag("text"))
    for trend in trends:
        g = etree.Element("g")
        g.attrib["class"] = "tooltip css"
        g.attrib["transform"] = trend.attrib["transform"]
        text = etree.Element("text")
        text.attrib["fill"] = "LightSeaGreen"
        text.attrib["filter"] = "url(#solid)"
        for line in tooltips[trend.text].split("\n"):
            tspan = etree.Element("tspan")
            tspan.attrib["x"] = "0"
            tspan.attrib["dy"] = "1.2em"
            tspan.text = line
            text.append(tspan)
        g.append(text)
        trend.addnext(g)
    return svg

def main():
    data = load_data()
    frequencies = {}
    for _, row in data.iterrows():
        frequencies[row["trend"]] = float(row["weight"])
    svg = generate_wordcloud(frequencies)
    svg = update_style(svg)
    svg = add_filter(svg)
    tooltips = {}
    for _, row in data.iterrows():
        tooltips[row["trend"]] = row["description"]
    svg = add_tooltips(svg, tooltips)
    Path("svg_iter.svg").write_bytes(etree.tostring(svg))


if __name__ == "__main__":
    main()
