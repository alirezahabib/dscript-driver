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


def get_relays() -> list[bool]:
    status = _fetch()
    return [value == '1' for key, value in status.items() if key.startswith('Rly')]


def toggle_relay(relay: int):
    logging.info(f'Toggling relay {relay}')
    response = requests.get(toggle_url(relay), timeout=connection_timeout)

    if response.status_code == 200:
        logging.info('Request successful')
    else:
        logging.error(f'Request failed with status code: {response.status_code}')

    _sleep(slowdown)


def get_relay(relay: int) -> bool:
    return get_relays()[relay - 1]


def set_relay(relay: int, state: bool):
    if get_relay(relay) != state:
        toggle_relay(relay)


def set_relay_sure(relay: int, state: bool):
    while get_relay(relay) != state:
        toggle_relay(relay)
