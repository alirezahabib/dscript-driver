import logging
import xml.etree.ElementTree
from time import sleep as _sleep

import requests

from config import *

logging.basicConfig(level=logging.INFO)


def _fetch() -> dict[str, str]:
    logging.info(f'Fetching data from {ip_address}')
    xml_url = f'http://{ip_address}:{port}/index.xml'

    # Fetch the XML data
    response = requests.get(xml_url, timeout=connection_timeout)

    if response.status_code == 200:  # successful
        # Parse the XML data
        xml_data = response.content
        root = xml.etree.ElementTree.fromstring(xml_data)

        return {element.tag: element.text for element in root.iter()}

    raise ConnectionError(f'Failed to fetch data. Status code: {response.status_code}')
