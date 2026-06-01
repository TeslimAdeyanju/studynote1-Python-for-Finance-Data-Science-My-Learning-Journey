"""
OneDrive Data Loader
====================
A simple utility to load data files from OneDrive using Microsoft Graph API.

Usage:
    # Import and use in your notebooks
    from onedrive_loader import load_csv, load_json, load_excel, load_file
    
    df = load_csv("YourFolder", "data.csv")
    
    # Or run this script directly for testing
    python onedrive_loader.py
"""

import os
import json
import requests
import pandas as pd
from io import BytesIO
from typing import Optional
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential


# ============================================================================
# CONFIGURATION - Edit these for your OneDrive setup
# ============================================================================

USER_EMAIL = "info@adeyanjuteslim.co.uk"
BASE_FOLDER = "TeslimDataLakes"  # Your root folder in OneDrive


# ============================================================================
# AUTHENTICATION - Loads credentials from .env file
# ============================================================================

def get_access_token() -> str:
    """Get Microsoft Graph API access token using credentials from .env file."""
    load_dotenv()
    
    client_id = os.getenv("SHAREPOINT_CLIENT_ID")
    tenant_id = os.getenv("SHAREPOINT_TENANT_ID")
    client_secret = os.getenv("SHAREPOINT_CLIENT_SECRET")
    
    if not all([client_id, tenant_id, client_secret]):
        raise ValueError("Missing credentials in .env file. Need: SHAREPOINT_CLIENT_ID, SHAREPOINT_TENANT_ID, SHAREPOINT_CLIENT_SECRET")
    
    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    token = credential.get_token("https://graph.microsoft.com/.default")
    return token.token


# Global token (initialized on first use)
_access_token = None

def _get_token():
    """Internal helper to cache access token."""
    global _access_token
    if _access_token is None:
        _access_token = get_access_token()
    return _access_token


# ============================================================================
# FILE LOADING FUNCTIONS
# ============================================================================

def load_csv(subfolder: str, filename: str, **kwargs) -> pd.DataFrame:
    """
    Load a CSV file from OneDrive.
    
    Args:
        subfolder: Subfolder name inside BASE_FOLDER (e.g., "FinancialData")
        filename: Name of the CSV file (e.g., "users.csv")
        **kwargs: Additional arguments passed to pd.read_csv()
    
    Returns:
        pandas DataFrame
    """
    file_path = f"{BASE_FOLDER}/{subfolder}/{filename}"
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/drive/root:/{file_path}:/content"
    
    response = requests.get(url, headers={"Authorization": f"Bearer {_get_token()}"})
    response.raise_for_status()
    
    return pd.read_csv(BytesIO(response.content), **kwargs)


def load_json(subfolder: str, filename: str, **kwargs) -> pd.DataFrame:
    """
    Load a JSON file from OneDrive.
    Handles multiple JSON structures automatically.
    
    Args:
        subfolder: Subfolder name inside BASE_FOLDER
        filename: Name of the JSON file (e.g., "data.json")
        **kwargs: Additional arguments passed to pd.read_json()
    
    Returns:
        pandas DataFrame
    """
    file_path = f"{BASE_FOLDER}/{subfolder}/{filename}"
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/drive/root:/{file_path}:/content"
    
    response = requests.get(url, headers={"Authorization": f"Bearer {_get_token()}"})
    response.raise_for_status()
    
    # Try standard pandas JSON loading first
    try:
        return pd.read_json(BytesIO(response.content), **kwargs)
    except ValueError:
        # Handle scalar-value dictionaries or nested structures
        json_data = json.loads(response.content)
        
        # If it's a dict with only scalar values, convert to single-row DataFrame
        if isinstance(json_data, dict) and all(not isinstance(v, (list, dict)) for v in json_data.values()):
            return pd.DataFrame([json_data])
        
        return pd.DataFrame(json_data)


def load_excel(subfolder: str, filename: str, sheet_name: Optional[str] = 0, **kwargs) -> pd.DataFrame:
    """
    Load an Excel file from OneDrive.
    
    Args:
        subfolder: Subfolder name inside BASE_FOLDER
        filename: Name of the Excel file (e.g., "data.xlsx")
        sheet_name: Sheet name or index (default: 0 = first sheet)
        **kwargs: Additional arguments passed to pd.read_excel()
    
    Returns:
        pandas DataFrame
    """
    file_path = f"{BASE_FOLDER}/{subfolder}/{filename}"
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/drive/root:/{file_path}:/content"
    
    response = requests.get(url, headers={"Authorization": f"Bearer {_get_token()}"})
    response.raise_for_status()
    
    return pd.read_excel(BytesIO(response.content), sheet_name=sheet_name, **kwargs)


def load_parquet(subfolder: str, filename: str, **kwargs) -> pd.DataFrame:
    """
    Load a Parquet file from OneDrive.
    
    Args:
        subfolder: Subfolder name inside BASE_FOLDER
        filename: Name of the Parquet file (e.g., "data.parquet")
        **kwargs: Additional arguments passed to pd.read_parquet()
    
    Returns:
        pandas DataFrame
    """
    file_path = f"{BASE_FOLDER}/{subfolder}/{filename}"
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/drive/root:/{file_path}:/content"
    
    response = requests.get(url, headers={"Authorization": f"Bearer {_get_token()}"})
    response.raise_for_status()
    
    return pd.read_parquet(BytesIO(response.content), **kwargs)


def load_file(subfolder: str, filename: str, **kwargs) -> pd.DataFrame:
    """
    Smart loader - automatically detects file type and loads accordingly.
    
    Args:
        subfolder: Subfolder name inside BASE_FOLDER
        filename: Name of the file
        **kwargs: Additional arguments passed to the appropriate pandas reader
    
    Returns:
        pandas DataFrame
    """
    file_extension = filename.lower().split('.')[-1]
    
    loaders = {
        'csv': load_csv,
        'json': load_json,
        'xlsx': load_excel,
        'xls': load_excel,
        'parquet': load_parquet,
        'pq': load_parquet
    }
    
    if file_extension not in loaders:
        raise ValueError(f"Unsupported file type: .{file_extension}")
    
    return loaders[file_extension](subfolder, filename, **kwargs)


def list_files(subfolder: str) -> list:
    """
    List all files in a OneDrive subfolder.
    
    Args:
        subfolder: Subfolder name inside BASE_FOLDER
    
    Returns:
        List of file names
    """
    folder_path = f"{BASE_FOLDER}/{subfolder}"
    url = f"https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/drive/root:/{folder_path}:/children"
    
    response = requests.get(url, headers={"Authorization": f"Bearer {_get_token()}"})
    response.raise_for_status()
    
    items = response.json().get('value', [])
    return [item['name'] for item in items if 'file' in item]


# ============================================================================
# TESTING / EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("🔄 Testing OneDrive Data Loader...\n")
    
    # Example: Load a CSV file
    try:
        df = load_csv("FinancialTransactionsDatasetAnalytics(Kaggle)", "users_data.csv")
        print(f"✅ Loaded CSV: {df.shape}")
        print(df.head(2))
    except Exception as e:
        print(f"❌ CSV loading failed: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Example: Load a JSON file
    try:
        df = load_json("FinancialTransactionsDatasetAnalytics(Kaggle)", "mcc_codes.json")
        print(f"✅ Loaded JSON: {df.shape}")
        print(df.head(2))
    except Exception as e:
        print(f"❌ JSON loading failed: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Example: List files in a folder
    try:
        files = list_files("FinancialTransactionsDatasetAnalytics(Kaggle)")
        print(f"✅ Found {len(files)} files:")
        for f in files[:5]:  # Show first 5
            print(f"   - {f}")
    except Exception as e:
        print(f"❌ File listing failed: {e}")
