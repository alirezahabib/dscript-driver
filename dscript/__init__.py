import logging
import xml.etree.ElementTree
from time import sleep as _sleep

import requests

logging.basicConfig(level=logging.INFO)

# Don't modify these values here (unless you want to change the defaults)
# modify them in your script (after the import)
pulse_duration = 0.030  # in seconds
slowdown = 0.030  # in seconds
settle_down = 0.400  # in seconds
ip_address = '169.254.100.1'
port = 80
connection_timeout = 4.0  # in seconds


def toggle_url(relay):
    return 'http://' + ip_address + '/dscript.cgi?V20552=' + str(relay)


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


def pulse_relay(relay: int):
    # Not using toggle_relay() twice because the timing between the two requests is important
    url = toggle_url(relay)

    _sleep(pulse_duration)
    response1 = requests.get(url, timeout=connection_timeout)
    _sleep(pulse_duration)
    response2 = requests.get(url, timeout=connection_timeout)
    _sleep(pulse_duration)

    if response1.status_code == 200 and response2.status_code == 200:
        logging.info('Request successful')
    else:
        logging.error(f'Request failed with status codes: {response1.status_code} and {response2.status_code}')


def pulse_relay_instant1(relay: int):
    url = toggle_url(relay)

    _sleep(pulse_duration)
    requests.get(url)
    requests.get(url)
    _sleep(pulse_duration)


def pulse_relay_instant2(relay: int):
    url = toggle_url(relay)

    # Prepare the sessions and requests
    session1 = requests.Session()
    request1 = requests.Request('GET', url)
    prepped1 = session1.prepare_request(request1)

    session2 = requests.Session()
    request2 = requests.Request('GET', url)
    prepped2 = session2.prepare_request(request2)

    session1.send(prepped1)
    session2.send(prepped2)


def _check_position(position: int):
    if not (1 <= position <= 6):
        raise ValueError('Gate position should be between 1 and 6.')


def set_gate(position: int, switch: int, state: bool):
    logging.info(f'Setting gate {position} switch {switch} to {state}')

    _check_position(position)

    if switch not in (1, 2):
        raise ValueError('Gate switch should be 1 or 2.')

    static = position + 14 * (switch - 1)
    pulse = position + 7 + (1 - state)

    set_relay_sure(static, True)
    _sleep(settle_down)
    set_relay_sure(static + 1, True)
    _sleep(settle_down)
    set_relay_sure(pulse, False)

    _sleep(settle_down)
    pulse_relay(pulse)
    _sleep(settle_down)

    set_relay_sure(static, False)
    _sleep(settle_down)
    set_relay_sure(static + 1, False)


def reset_relays():
    logging.info(f'Resetting all relays to False')
    for relay, state in enumerate(get_relays()):
        if state:
            toggle_relay(relay + 1)
