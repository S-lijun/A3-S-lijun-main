import io
import zipfile

import requests


def fetch_data() -> None:
    response = requests.get(
        "https://wustl.box.com/shared/static/fprbb446gvz5znowkrxf6nanze56nco6.zip"
    )
    z = zipfile.ZipFile(io.BytesIO(response.content))
    z.extractall("data/raw")
