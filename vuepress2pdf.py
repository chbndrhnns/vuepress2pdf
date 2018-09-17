#!/usr/bin/env python
import asyncio
import logging
import datetime
import os
import sys
from sys import argv
from pyppeteer import launch

import cfg_load

config = cfg_load.load('config.yaml')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

format_string = '%(asctime)s - %(levelname)s - %(message)s'

level = os.getenv('LOG_LEVEL', logging.INFO)
logging.basicConfig(stream=sys.stdout, level=level,
                    format=format_string)
log = logging.getLogger(__name__)  # pylint: disable=C0103

MARGIN_LEFT = config['layout']['margin']['left']
MARGIN_TOP = config['layout']['margin']['top']
MARGIN_RIGHT = config['layout']['margin']['right']
MARGIN_BOTTOM = config['layout']['margin']['bottom']
NO_MARGIN = False
NOW = str(datetime.datetime.now().strftime("%Y-%m-%d"))

LEGAL_ENTITY = config['layout']['legal_entity']

with open('style.html', 'r') as style_file:
    style = style_file.read()
    HEADER = """{}{}""".format(style, config['layout']['header'])
    FOOTER = config['layout']['footer'].format(LEGAL_ENTITY, NOW)
    FOOTER = style + FOOTER


def is_docker():
    """Detect if we are running Docker. Found at https://stackoverflow.com/a/48710609/6112272"""
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )


def err_and_exit(err):
    log.error(err)
    sys.exit(1)


async def create_pdf(url=None):
    """Screenshot routine"""
    launch_options = None

    if is_docker():
        launch_options = {
            'executablePath': '/usr/bin/chromium-browser',
            'args': [
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox'
            ],
        }
        log.info('Launch options: %s', launch_options)

    if not url:
        err_and_exit('We need an url or a file as source!')

    output = '{}.pdf'.format(url.split('/')[-1:][0].replace('.html', ''))
    output_path = os.path.join(ROOT_DIR, 'dist')
    full_path = os.path.join(output_path, output)

    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    log.info('Print to file %s', full_path)

    log.info('Launching browser...')
    browser = await launch(launch_options)
    page = await browser.newPage()

    log.info('Loading page %s', url)
    await page.goto(url, {'waitUntil': 'networkidle0'})

    for hide in config['hide_elements']:
        await page.waitForSelector(hide)
        await page.evaluate("""() => {{ document.querySelector('{}').style.display = 'none'; }}""".format(hide))

    log.info('Creating PDF...')
    await page.pdf({
        'path': full_path,
        'printBackground': True,
        'format': 'A4',
        'displayHeaderFooter': True,
        'footerTemplate': FOOTER,
        'headerTemplate': HEADER,
        'margin': {'top': MARGIN_TOP, 'bottom': MARGIN_BOTTOM, 'left': MARGIN_LEFT, 'right': MARGIN_RIGHT}})
    await browser.close()


def main(argv):
    if len(argv) != 2:
        err_and_exit(
            'Could not understand command line options. Please provide a URL for conversion.')
    asyncio.get_event_loop().run_until_complete(create_pdf(argv[1]))


if __name__ == '__main__':
    main(argv)
