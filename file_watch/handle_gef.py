from pathlib import Path
import requests

URL = "http://10.64.32.62:8080/api/cpt/"


def post_gef_file(file: Path) -> requests.Response:
    return requests.post(URL, files={"gef": open(file, 'rb')})

