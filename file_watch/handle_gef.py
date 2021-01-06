from pathlib import Path
import requests

URL = "http://10.64.32.62:8080/api/cpt/"


def post_gef_file(file: Path, url=URL) -> requests.Response:
    return requests.post(url, files={"gef": open(file, 'rb')})

