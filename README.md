# dScript Python driver
Driver for the dscript switches at LPQM

## Documentation

> Example
> ```python
> import dscript
> 
> dscript.ip_address = '169.254.100.1'
> 
> dscript.reset_relays()
> dscript.get_relays()
> dscript.toggle_relay(2)
> dscript.get_relays()
> ```
> ```
> INFO:root:Resetting all relays to False
> INFO:root:Fetching data from 169.254.100.2
> INFO:root:Toggling relay 2
> INFO:root:Request successful
> INFO:root:Fetching data from 169.254.100.2
> INFO:root:Toggling relay 2
> [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
> INFO:root:Request successful
> INFO:root:Fetching data from 169.254.100.2
> [False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
> ```

### set_gate

```python
set_gate(position: int, switch: int, state: bool)
```
Sets two gates and pulses another gate according to the table below. Then resets the gates to False.

| Position | Active Relays Switch 1 | Active Relays Switch 2 | Pulse to Connect | Pulse to Disconnect |
|----------|------------------------|------------------------|------------------|---------------------|
| 1        | 1, 2                   | 15, 16                 | 8                | 9                   |
| 2        | 2, 3                   | 16, 17                 | 9                | 10                  |
| 3        | 3, 4                   | 17, 18                 | 10               | 11                  |
| 4        | 4, 5                   | 18, 19                 | 11               | 12                  |
| 5        | 5, 6                   | 19, 20                 | 12               | 13                  |
| 6        | 6, 7                   | 20, 21                 | 13               | 14                  |

### set_relay
```python 
set_relay(relay: int, state: bool)
```

> Example
> ```pycon
> >>> dscript.set_relay(1, True)
> ```

### toggle_relay
```python
toggle_relay(relay: int)
```

Faster than `set_relay(relay, state)`

> Example
> ```pycon
> >>> dscript.toggle_relay(1)
> ```

### set_relay_sure
```python
set_relay_sure(relay: int, state: bool)
```

Sets the relay and checks if it was successful. If not, it will try again.

### pulse_relay
```python
pulse_relay(relay: int)
```

Toggles the relay, waits for `pulse_duration` seconds, then toggles the relay and waits for `pulse_duration` seconds again.

### reset_relays
```python
set_relays()
```

Resets all relays to False.

### get_relays
```python
get_relays() -> list[bool]
```

> Example
> ```pycon
> >>> dscript.set_relay(2, True)
> >>> dscript.get_relays()
> [False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
> ```

### get_relay 
```python
get_relay(relay: int) -> bool
```
Same performance as `get_relays()`

> Example
> ```pycon
> >>> dscript.set_relay(5, True)
> >>> dscript.get_relay(5)
> True
> ```

### _fetch()
```python
_fetch() -> dict[str, str]
```

Fetches the data from the switch and returns it as a dictionary.
Data is in raw format. Meant to be used by other functions or debugging.

> Example
> ```pycon
> >>> dscript._fetch()
> {
> 'response': '\n', 
> 'Rly1': '0', 'Rly2': '0', 'Rly3': '0', 'Rly4': '0', 'Rly5': '0', 'Rly6': '0', 'Rly7': '0', 'Rly8': '0', 'Rly9': '0', 'Rly10': '0', 'Rly11': '0', 'Rly12': '0', 'Rly13': '0', 'Rly14': '0', 'Rly15': '0', 'Rly16': '0', 'Rly17': '0', 'Rly18': '0', 'Rly19': '0', 'Rly20': '0', 'Rly21': '0', 'Rly22': '0', 'Rly23': '0', 'Rly24': '0', 'Rly25': '0', 'Rly26': '0', 'Rly27': '0', 'Rly28': '0', 'Rly29': '0', 'Rly30': '0', 'Rly31': '0', 'Rly32': '0', 
> 'IO1': '0', 'IO1_s': '1', 'IO2': '0', 'IO2_s': '1', 'IO3': '0', 'IO3_s': '1', 'IO4': '0', 'IO4_s': '1', 'IO5': '0', 'IO5_s': '1', 'IO6': '0', 'IO6_s': '1', 'IO7': '0', 'IO7_s': '1', 'IO8': '0', 'IO8_s': '1', 
> 'System_CtrVal1': '0', 'System_CtrVal2': '0', 'System_CtrVal3': '0', 'System_CtrVal4': '0', 'System_CtrCapt1': '0', 'System_CtrCapt2': '0', 'System_CtrCapt3': '0', 'System_CtrCapt4': '0', 
> 'PingTime1': '0', 'PingTime2': '0', 'PingTime3': '0', 'PingTime4': '0'
> }
> ```

## Changing the defaults

You can change any of the following defaults after the import or anywhere in the code. The current defaults are shown below.
If not specified, the defaults will be used.

To find the ip address of the switch, look at the ip table in the OneNote.
Right now the main switch is `169.254.100.1` and the spare is `169.254.100.2`.

```python
import dscript

dscript.ip_address = '169.254.100.2'
dscript.port = 80
dscript.pulse_duration = 0.150  # in seconds
dscript.slowdown = 0.010  # in seconds
```

### Logging
Logging is set to `INFO` by default. You can change the logging level by using the following code. From least to most verbose:
```python
dscript.logging.basicConfig(level=dscript.logging.CRITICAL + 1) # disables logging
```
```python
dscript.logging.basicConfig(level=dscript.logging.CRITICAL)
```
```python
dscript.logging.basicConfig(level=dscript.logging.ERROR) # recommended
```
```python
dscript.logging.basicConfig(level=dscript.logging.WARNING)
```
```python
dscript.logging.basicConfig(level=dscript.logging.INFO) # default
```
```python
dscript.logging.basicConfig(level=dscript.logging.DEBUG)
```


## Requirements
- `requests`
- `logging`
- `setuptools`
- `streamlit`
- `Pillow`
