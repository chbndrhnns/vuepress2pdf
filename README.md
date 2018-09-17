# `vuepress2pdf`

## About

As of now, vuepress has no integrated abilities to create PDFs from documents. This tool uses a headless Chrome instance to display a website and renders it to PDF.

## Usage

### Native (using pipenv)

Run `pipenv install` to install the virtual environment, then run `pyppeteer-install` to download chrome and then use the command `pipenv run python vuepress2.pdf <url>` to convert a page to pdf.

### Docker

Build the image: `make build`
Run the image: `docker run -v $(pwd)/dist:/app/dist --rm chbndhrnns/vuepress2pdf <url>`

## Configuration file

The file `config.yaml` is used to customize the PDF export.

## How to get help

Created by Johannes Rueschel. Contact him on Slack (chbndrhnns)
