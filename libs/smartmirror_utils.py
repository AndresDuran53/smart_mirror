import requests
import json

def log(mensaje,nombre="smartMirror.mainFail"):
    print(mensaje)
    with open(nombre+'.log', 'a') as f:
        print(mensaje, file=f)

def get_ip(self):
    result = None
    try:
        ip_url = "http://jsonip.com/"
        req = requests.get(ip_url)
        ip_json = json.loads(req.text)
        result = ip_json['ip']
    except Exception as e:
        log("Error: Cannot get ip. " + str(e))
    finally:
        return result