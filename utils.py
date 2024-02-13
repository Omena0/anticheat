"""Utils functions lmao
"""

from datetime import timezone, datetime
import time as t
import sys
import requests


def exit(msg,code=0):
    print(msg)
    sys.exit(code)
    
def get_font_size(text,space=1500):
    size = 50
    while round(size*len(text)) > space:
        size -= 1
    return size

pprint = print

def print(*args):
    try:
        date = datetime.now(timezone.utc) - datetime(1970, 1, 1)
        ms = round(date.total_seconds()*1000)%1000
        time = f'{t.strftime(f"%H:%M:%S:{ms}"):<12}'
        pprint(f'{time} {" ".join(args)}')
    except Exception:
        pprint(*args)


defaultConfig = """
# Config file for Fr-client
# Lines starting with # are ignored.
# Options starting with [PREMIUM] only work when you are a premium user.

# [PREMIUM] Enable or disable addons (Default: False)
addons = False
"""

class Config:
    """Config"""
    def __init__(self, file: str) -> None:
        self.file = file
        try:
            self.load()
        except Exception:
            with open(file, 'w') as file:
                file.write(defaultConfig)
            self.load()

    def load(self) -> None:
        """Load the configuration from the file."""
        with open(self.file) as file:
            for i in file.read().split('\n'):
                if i.startswith('#') or i == '':
                    continue
                key, value = i.split('=')
                key = key.strip()
                value = value.strip()
                exec(f'self.{key} = value')
                print(f'{key} = {value}')


API_URL = 'https://omena0.github.io/api'

def apiGet(path):
    """Get a string from api

    Args:
        path (str): api path

    Returns:
        str: string from api
    """
    response = requests.get(f"{API_URL}/{path}")
    response.raise_for_status()
    return response.text.strip()






