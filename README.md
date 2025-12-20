<div align="center">

<a href="https://github.com/iptch/trend-radar"><img src="./assets/logo.jpeg" alt="Trend Radar" width="25%"></a>

# Trend Radar

![Devbox](https://img.shields.io/badge/built_with_devbox-true?style=flat&logo=devbox&link=https%3A%2F%2Fwww.jetify.com%2Fdocs%2Fdevbox%2F)
![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)

### A small script to generate wordclouds, meant to be used as a way to easily display our trends and their importance.

[Usage](#usage) |
[Adding Trends](#adding-trends) |
[Roadmap](#roadmap)

<hr />
</div>

This repository serves to generate a wordcloud of various trends. This is then used in Happeo for
the trend radar homepage.

<!-- TODO(@f4z3r): add link to page -->

## Usage

The easiest way to run this script is to use [Devbox](https://www.jetify.com/docs/devbox/). You can
then build the wordcloud the command below, which will generate a `trend-radar.png` file within the
`assets` directory.

```sh
devbox run generate
```

Alternatively you can use [`uv`](https://docs.astral.sh/uv/) or `pip` directly to install the
required dependencies and run the script:

```sh
# for uv
uv add --frozen -r requirements.txt
uv run --frozen python main.py

# for pip
pip install -r requirements.txt
python main.py
```

## Adding Trends

Trends can be added by modifying the [`trends.csv`](./trends.csv) file. Each line represents a
trend, which the following fields in order:

1. The name of the trend
2. Its weight. We use weights between 1 and 100 inclusive.
3. The focus area of the trend. Can be one of:
   - `cloud`
   - `ai`
   - `security`
   - `integration`
   - `dx`

Any text is ideally put into quotes. This avoids issues where the text contains a comma and is thus
interpreted in a different manner by the CSV parser.

Once you have added a trend, you can generate images. Note that the order of the trends in the CSV
has no effect.

There is no need to generate the images yourself. A [GitHub
workflow](./.github/workflows/generate-img.yml) will generate a new image when
changes are done to the repository.
