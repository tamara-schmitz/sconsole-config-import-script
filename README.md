# sconsole-config-import-script
If you ever happen to have a wti TSM-24 Console Server and want to migrate its
config to an Avocent ACS800/8000 Advanced Console System, this script is for you.

## Project Goal

The
[wti TSM-24 Console Server](https://www.wti.com/products/tsm-24-console-server-24-port-rj45)
has a config export function that produces a device specific XML file that
requires some parsing to be useful for other applications. If you now wish to
migrate that data onto your
[Avocent ACS800/8000 Advanced Console System](https://www.vertiv.com/en-us/products-catalog/monitoring-control-and-management/serial-consoles-and-gateways/avocent-acs-8000-serial-consoles/)
, this script will use its RESTful API to transfer your configuration to the new
system.

**It is explicitly a quick and dirty script written in a day and not as a program that takes
command line arguments or parses config files etc. It is provided as is without
warranties nor guarantees.**

## Usage

Assuming you have a working Python 3 installation with pip, install the module dependency:
```bash
python3 -m pip install requests
```

In `parse_devcon.py` adjust the line `devcon_tree = ET.parse('wtilog.xml')` to
match your XML's name and path. Execute `python3 parse_devcon.py` to test
parsing and check that the output is ok.

In `rest_avocent.py` adjust these variables to match your hostname and
credentials on the console system:
```python
api_url_base = "https://sconsole.local:48048/api/v1"
usercredentials = {"username": "admin", "password": "admin"}
```

Now execute `python3 rest_avocent.py` to transfer your console port
configuration over. Note that this overwrites existing configuration and a
backup prior to execution is advised.

## Components

`parse_devcon.py` takes care of parsing the XML file and turning it into a
dictionary for later use in the program. The dictionary is optimised for the
RESTful API, for example translating menu selections into actual Serial speeds.

`rest_avocent.py` uses the Avocent RESTful API to execute the transfer. Due to a
hostname mismatch, the included TLS certificate cannot be used to verify the
host's integrity.

