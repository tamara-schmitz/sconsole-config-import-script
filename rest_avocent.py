#!/usr/bin/env python3

import requests # python3 -m pip install requests
import json
import parse_devcon

api_url_base = "https://sconsole.local:48048/api/v1"
usercredentials = {"username": "admin", "password": "admin"}
session = requests.Session()
session.headers.update({"Content-Type": "application/json"})
#session.verify = "cert.pem"
session.verify = False

def send_post(url : str, postkeys : dict) -> requests.models.Response:
    return session.post(api_url_base + url, data=json.dumps(postkeys))

def send_get(url : str, getparams : dict) -> requests.models.Response:
    return session.get(api_url_base + url, params=getparams)

def send_put(url : str, putkeys : dict) -> requests.models.Response:
    return session.put(api_url_base + url, data=json.dumps(putkeys))

def print_response(response):
    try:
        print(response.json())
    except requests.exceptions.JSONDecodeError:
        print(response.text)
    print(response.status_code)

login = send_post("/sessions/login", usercredentials)
login_token = login.json().get('token')
session.headers.update({"Authorization": "Bearer " + login_token})
print_response(login)


info = send_get("/system/info", {})
print_response(info)

info = send_get("/serialPorts/1", {})
print_response(info)

put = send_put("/serialPorts/4", {"profile": "cas"})
print_response(put)

put = send_put("/serialPorts/4", {"physical": {"speed": 1200}})
print_response(put)

put = send_put("/serialPorts/4", {"physical": parse_devcon.dict_port[1]})
print_response(put)

for port in parse_devcon.dict_port.values():
    print(port["index"], port["name"])
    di = {"physical": port, 
          "cas": {
                        "name": port["name"],
                        "speedAutoDetection": "disabled",
                        "protocol": "ssh",
                        "sshAliasPort": str(2200 + port["index"])
                 }
    }

    put = send_put("/serialPorts/" + str(port["index"]), di)
    print_response(put)

logout = send_post("/sessions/logout", {})
print_response(logout)

session.close()
