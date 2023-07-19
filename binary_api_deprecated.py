"""
Binary API instead of the web api (deprecated because it doesn't work)

The switch api port is not allowing connections, so this is not working.
"""

import logging
import socket

logging.basicConfig(level=logging.INFO)

# Don't modify these values here (unless you want to change the defaults)
# modify them in your script (after the import)
pulse_duration = 150  # in ms


def _four_byte_format(n: int):
    hex_value = hex(n)[2:].zfill(8)  # Convert to hex, remove the leading '0x', and pad to ensure 4 bytes
    encoded_str = bytes.fromhex(hex_value).decode("ISO-8859-1")  # Decode each byte to a character
    return encoded_str


def _check_gate_number(gate: int):
    if not (1 <= gate <= 7):
        raise ValueError("Gate should be between 1 and 7.")


class Connection:
    def __init__(self, ip_address, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_address = ip_address
        self.port = port

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        logging.info(f"Connecting to {self.ip_address}:{self.port}")

        try:
            self.client_socket.connect((self.ip_address, self.port))
            logging.info(f"Connected to {self.ip_address}:{self.port}")

        except ConnectionRefusedError:
            logging.error(f"Connection refused to {self.ip_address}:{self.port}")
        except Exception as e:
            logging.error(f"{type(e).__name__}: {str(e)}")

    def disconnect(self):
        self.client_socket.close()
        logging.info("Socket closed.")

    def _send_read_data(self, data, read_bytes=2):
        try:
            self.client_socket.sendall(data)
            logging.info(f"Sent data: {data}")

            response = self.client_socket.recv(read_bytes)
            logging.info(f"Received response: {response}")

            return response

        except ConnectionRefusedError:
            logging.error(f"Connection refused.")
        except Exception as e:
            logging.error(f"{type(e).__name__}: {str(e)}")

        return None

    def set_gate(self, gate: int, switch: int, state: bool):
        logging.info(f"Setting gate {gate} switch {switch} to {state}")

        _check_gate_number(gate)
        assert 1 <= switch <= 2  # TODO: add error handling or use enum

        static = gate + 14 * (switch - 1)
        pulse = gate + 7 + (1 - state)

        self.set_relay(static, True)
        self.set_relay(static + 1, True)
        self.pulse_relay(pulse)

    def pulse_relay(self, relay: int, duration: int = pulse_duration):
        # \x31 \[relay] \x00 \[duration] \[duration] \[duration] \[duration]
        # pulse relay 5 for 1 second: \x31 \x05 \x00 \x00 \x00 \x03 \xe8

        command = '\x31' + chr(relay) + '\x00' + _four_byte_format(duration)
        self._send_read_data(command)

    def set_relay(self, relay: int, state: bool):
        # \x31 \[relay] \[state] \x00 \x00 \x00 \x00
        # Set relay 5 to on: \x31 \x05 \x01 \x00 \x00 \x00 \x00
        logging.info(f"Setting relay {relay} to {state}")

        command = '\x31' + chr(relay) + chr(state) + '\x00\x00\x00\x00'
        self._send_read_data(command)

    def get_relay(self, relay: int) -> bool:
        command = '\x33' + chr(relay)
        response = self._send_read_data(command, 5)

        return response[0] > 0

    def get_input(self, input_num: int) -> bool:
        # TODO: add error handling

        command = '\x34' + chr(input_num)
        response = self._send_read_data(command)

        return response[0] > 0

    def get_status(self):
        command = '\x30'
        response = self._send_read_data(command, 9)

        return {'Module ID': str(response[0]),
                'System Firmware Version': f'{response[1]}.{response[2]}',
                'Application Firmware Version': f'{response[3]}.{response[4]}',
                'Voltage': int(response[5]) / 10,
                'Internal Temperature Celsius': int.from_bytes(response[6:8], byteorder='big', signed=True) / 10,
                }

    def toggle_relay(self, relay: int):
        if self.get_relay(relay):
            self.set_relay(relay, False)
        else:
            self.set_relay(relay, True)

    def get_all_relays(self) -> list:
        command = '\x33\01'
        response = self._send_read_data(command)

        binary = bin(response[1])[2:].zfill(8)
        return _bin_to_list(binary)

    def get_all_inputs(self) -> list:
        command = '\x34\01'
        response = self._send_read_data(command, 5)

        binary = bin(int.from_bytes(response[1:5], byteorder='big', signed=True))[2:].zfill(32)
        return _bin_to_list(binary)


def _bin_to_list(binary):
    return [i == '1' for i in reversed(binary)]

