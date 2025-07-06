<div align="center">

<a href="https://github.com/iptch/trend-radar"><img src="./assets/logo.jpeg" alt="Trend Radar" width="25%"></a>

# Trend Radar

![Devbox](https://img.shields.io/badge/built_with_devbox-true?style=flat&logo=devbox&link=https%3A%2F%2Fwww.jetify.com%2Fdocs%2Fdevbox%2F)
![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)

### A small script to generate wordclouds with tooltips, meant to be used as a way to easily display our trends and some additional information about them.

[Usage](#usage) |
[Adding Trends](#adding-trends)

<hr />
</div>

This repository serves to generate a wordcloud of various trends. This is then used in Happeo for
the trend radar homepage.

<!-- TODO(@f4z3r): add link to page -->

## Usage

The easiest way to run this script is to use [Devbox](https://www.jetify.com/docs/devbox/). You can
then build the wordcloud the command below, which will generate a `trends-wordcloud.svg` file.

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

<!-- TODO(@f4z3r): add info -->
