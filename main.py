import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pathlib import Path

df = pd.read_csv("./trends.csv")

frequencies = {}

for _, row in df.iterrows():
    frequencies[row["trend"]] = float(row["weight"])


wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(
    frequencies,
)

Path("trends-wordcloud.svg").write_text(wordcloud.to_svg())

# plt.figure(figsize=(10, 5))
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.title("ipt Trend Radar")
# plt.show()
