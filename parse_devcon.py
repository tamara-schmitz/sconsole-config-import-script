#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from urllib.parse import unquote
import requests # python3 -m pip install requests

"""
struct port
{
    "index" : -1
    "name" : ""
    "dataBits" : 0 # 7, 8
    "parity" : "" # none, odd, even
    "stopBits" : 0 # 1, 2
    "speed" : 0 # 300, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200
}
"""

devcon_tree = ET.parse('wtilog.xml')
devcon = devcon_tree.getroot()
devcon_ports = devcon.find('prt_parms')
dict_port = {}

for uart in devcon_ports.findall('uart'):
    i = int(uart.get('index'))
    port = {}
    port["index"] = i
    dict_port[i] = port

    name = uart.find('port_name').text
    if name != None:
        name = unquote(name)
    else:
        name = ""
    port["name"] = name

    match uart.find('bit_par').text:
        case '0':
            port["dataBits"] = 7
            port["parity"] = "none"
        case '1':
            port["dataBits"] = 7
            port["parity"] = "even"
        case '2':
            port["dataBits"] = 7
            port["parity"] = "odd"
        case '3':
            port["dataBits"] = 8
            port["parity"] = "none"
        case '4':
            port["dataBits"] = 8
            port["parity"] = "even"
        case '5':
            port["dataBits"] = 8
            port["parity"] = "odd"
        case _:
            port["dataBits"] = 8
            port["parity"] = "none"

    port["stopBits"] = int(uart.find('stop').text)

    match uart.find('baud').text:
        case '0':
            port["speed"] = 1200 # 300 not supported by avocent
        case '1':
            port["speed"] = 1200
        case '2':
            port["speed"] = 2400
        case '3':
            port["speed"] = 4800
        case '4':
            port["speed"] = 9600
        case '5':
            port["speed"] = 19200
        case '6':
            port["speed"] = 38400
        case '7':
            port["speed"] = 57600
        case '8':
            port["speed"] = 115200
        case _:
            port["speed"] = 9600


if __name__ == "__main__":
    print(dict_port)

    # debug: diff each port to find commonalities
    prev_uart = None
    for uart in devcon_ports.findall('uart'):
        if prev_uart != None and uart != None:
            i = 0
            for x in uart:
                if prev_uart[i].text != x.text:
                    print(x.tag, x.text)
                i += 1
        prev_uart = uart

