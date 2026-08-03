"""Load OneDrive datasets into pandas with one simple function.

Notebook examples
-----------------
from onedrive_loader import files, load

files()                                      # folders/files in TeslimDataLakes
files("MyDataset")                           # files inside a dataset folder
df = load("MyDataset/data.csv")              # CSV
df = load("MyDataset/data.xlsx")             # Excel
df = load("MyDataset/data.json")              # JSON
df = load("MyDataset/data.parquet")           # Parquet
"""

import json
import os
from io import BytesIO
from pathlib import Path
from typing import Optional
from urllib.parse import quote

import pandas as pd
import requests
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv


# Change these two values only if your OneDrive account or data-lake folder changes.
USER_EMAIL = "info@adeyanjuteslim.co.uk"
BASE_FOLDER = "TeslimDataLakes"

_access_token = None


def _get_token() -> str:
    """Create and cache a Microsoft Graph access token."""
    global _access_token
    if _access_token is not None:
        return _access_token

    # Load the .env beside this module, regardless of the notebook's directory.
    load_dotenv(Path(__file__).with_name(".env"))
    client_id = os.getenv("SHAREPOINT_CLIENT_ID")
    tenant_id = os.getenv("SHAREPOINT_TENANT_ID")
    client_secret = os.getenv("SHAREPOINT_CLIENT_SECRET")

    if not all((client_id, tenant_id, client_secret)):
        raise ValueError(
            "Credentials are missing. Add SHAREPOINT_CLIENT_ID, "
            "SHAREPOINT_TENANT_ID, and SHAREPOINT_CLIENT_SECRET to "
            f"{Path(__file__).with_name('.env')}."
        )

    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    _access_token = credential.get_token(
        "https://graph.microsoft.com/.default"
    ).token
    return _access_token


def _onedrive_path(relative_path: str = "") -> str:
    """Join a user-friendly relative path to BASE_FOLDER."""
    relative_path = str(relative_path).strip().strip("/")
    return "/".join(part for part in (BASE_FOLDER.strip("/"), relative_path) if part)


def _graph_url(relative_path: str, operation: str) -> str:
    """Build a safely encoded Microsoft Graph URL."""
    path = quote(_onedrive_path(relative_path), safe="/")
    user = quote(USER_EMAIL, safe="@")
    return (
        f"https://graph.microsoft.com/v1.0/users/{user}"
        f"/drive/root:/{path}:/{operation}"
    )


def _request(relative_path: str, operation: str) -> requests.Response:
    """Make a Graph request and return a useful error if it fails."""
    response = requests.get(
        _graph_url(relative_path, operation),
        headers={"Authorization": f"Bearer {_get_token()}"},
        timeout=60,
    )
    if not response.ok:
        try:
            detail = response.json().get("error", {}).get("message", response.text)
        except ValueError:
            detail = response.text
        raise FileNotFoundError(
            f"OneDrive could not open '{_onedrive_path(relative_path)}' "
            f"(HTTP {response.status_code}): {detail}"
        )
    return response


def files(folder: str = "") -> list[str]:
    """List both files and folders in BASE_FOLDER or one of its subfolders."""
    items = _request(folder, "children").json().get("value", [])
    return [item["name"] for item in items]


def load(path: str, **kwargs) -> pd.DataFrame:
    """Load a CSV, Excel, JSON, or Parquet OneDrive file into a DataFrame.

    Args:
        path: File path relative to BASE_FOLDER, for example
              ``"Sales/transactions.csv"``.
        **kwargs: Optional settings passed to the matching pandas reader,
                  such as ``sep=";"`` or ``sheet_name="January"``.
    """
    content = BytesIO(_request(path, "content").content)
    extension = Path(path).suffix.lower()

    if extension in {".csv", ".txt"}:
        return pd.read_csv(content, **kwargs)
    if extension in {".xlsx", ".xls"}:
        return pd.read_excel(content, **kwargs)
    if extension in {".parquet", ".pq"}:
        return pd.read_parquet(content, **kwargs)
    if extension == ".json":
        try:
            return pd.read_json(content, **kwargs)
        except ValueError:
            content.seek(0)
            data = json.load(content)
            if isinstance(data, dict) and all(
                not isinstance(value, (list, dict)) for value in data.values()
            ):
                return pd.DataFrame([data])
            return pd.DataFrame(data)

    raise ValueError(
        f"Unsupported file type '{extension}'. "
        "Supported types: CSV, Excel, JSON, and Parquet."
    )


# Familiar names for users who prefer an explicit loader.
def load_csv(folder: str, filename: Optional[str] = None, **kwargs) -> pd.DataFrame:
    return load(_legacy_path(folder, filename), **kwargs)


def load_excel(folder: str, filename: Optional[str] = None, **kwargs) -> pd.DataFrame:
    return load(_legacy_path(folder, filename), **kwargs)


def load_json(folder: str, filename: Optional[str] = None, **kwargs) -> pd.DataFrame:
    return load(_legacy_path(folder, filename), **kwargs)


def load_parquet(folder: str, filename: Optional[str] = None, **kwargs) -> pd.DataFrame:
    return load(_legacy_path(folder, filename), **kwargs)


def _legacy_path(folder: str, filename: Optional[str]) -> str:
    return f"{folder.strip('/')}/{filename}" if filename else folder


def load_file(folder: str, filename: Optional[str] = None, **kwargs) -> pd.DataFrame:
    """Compatibility wrapper; new code can use ``load("folder/file.csv")``."""
    return load(_legacy_path(folder, filename), **kwargs)


list_files = files


if __name__ == "__main__":
    print(f"Contents of {BASE_FOLDER}:")
    for name in files():
        print(f"  - {name}")
