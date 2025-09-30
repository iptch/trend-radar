import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

WIDTH = 1600
HEIGHT = 800

FILENAME = "trend-radar.png"

CATEGORY_COLOR = {
    "cloud": (0, 158, 179),  # Karibik T01
    "security": (84, 56, 166),  # Traube T01
    "ai&data": (228, 50, 67),  # Rouge T01
    "custom applications": (255, 110, 43),  # Orange T01
    "integration": (255, 187, 0),  # Sonne T01
}

ACRONYM_CUTOFF = 4


def load_data():
    return pd.read_csv("./trends.csv")


def to_plt_rgb(color):
    (r, g, b) = color
    return (r / 256, g / 256, b / 256)


def title_transform(title):
    return title.upper() if len(title) < ACRONYM_CUTOFF else title.title()


def main():
    data = load_data()
    frequencies = {}
    color_map = {}
    for _, row in data.iterrows():
        frequencies[row["trend"]] = float(row["weight"])
        color_map[row["trend"]] = CATEGORY_COLOR[row["focus"]]

    wordcloud = WordCloud(
        width=WIDTH,
        height=HEIGHT,
        background_color="white",
        scale=2,
        margin=6,
        relative_scaling=0.3,
        random_state=42,
        color_func=lambda word, *_, **_kw: color_map[word],
    ).generate_from_frequencies(frequencies)
    plt.figure(figsize=(30, 15))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    patches = [
        mpatches.Patch(color=to_plt_rgb(v), label=title_transform(k))
        for k, v in CATEGORY_COLOR.items()
    ]
    plt.legend(handles=patches, bbox_to_anchor=(0.075, 0))
    plt.savefig(FILENAME)


if __name__ == "__main__":
    main()
