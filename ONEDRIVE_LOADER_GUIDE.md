# OneDrive Loader Guide

This guide explains how to load datasets from your OneDrive directly into
pandas.

## 1. How your OneDrive should be organised

The loader uses this main OneDrive folder:

```text
TeslimDataLakes/
├── FinancialTransactionsDatasetAnalytics(Kaggle)/
│   ├── users_data.csv
│   ├── transactions_data.csv
│   └── mcc_codes.json
├── SalesDataset/
│   └── sales.xlsx
└── CustomerDataset/
    └── customers.parquet
```

Put each project or dataset inside its own folder under `TeslimDataLakes`.

## 2. Import the loader

At the top of a Jupyter notebook, run:

```python
from onedrive_loader import files, load
```

You only need two main functions:

- `files()` shows the contents of a OneDrive folder.
- `load()` loads a file into a pandas DataFrame.

## 3. See your available datasets

Run `files()` without a folder name:

```python
files()
```

Example result:

```python
[
    "FinancialTransactionsDatasetAnalytics(Kaggle)",
    "SalesDataset",
    "CustomerDataset"
]
```

Do not write `files("TeslimDataLakes")`. The loader already starts inside
`TeslimDataLakes`.

## 4. See files inside a dataset folder

Pass the dataset folder name to `files()`:

```python
files("FinancialTransactionsDatasetAnalytics(Kaggle)")
```

Example result:

```python
[
    "users_data.csv",
    "transactions_data.csv",
    "mcc_codes.json"
]
```

You can also inspect a nested folder:

```python
files("SalesDataset/2026")
```

## 5. Load a dataset into pandas

Give `load()` the folder and filename as one path:

```python
df = load(
    "FinancialTransactionsDatasetAnalytics(Kaggle)/users_data.csv"
)
```

Check that the data loaded correctly:

```python
df.head()
```

Other useful checks:

```python
df.shape
df.columns
df.info()
df.describe()
```

## 6. Change to another dataset

Change only the path passed to `load()`:

```python
df = load("SalesDataset/sales.xlsx")
```

Or:

```python
df = load("CustomerDataset/customers.parquet")
```

The loader detects the file type automatically.

## 7. Supported file types

### CSV

```python
df = load("MyDataset/data.csv")
```

You can pass normal `pandas.read_csv()` options:

```python
df = load("MyDataset/data.csv", sep=";")
```

```python
df = load("MyDataset/data.csv", encoding="latin-1")
```

```python
df = load("MyDataset/data.csv", parse_dates=["transaction_date"])
```

### Excel

Load the first worksheet:

```python
df = load("MyDataset/report.xlsx")
```

Load a worksheet by name:

```python
df = load("MyDataset/report.xlsx", sheet_name="January")
```

Load a worksheet by position:

```python
df = load("MyDataset/report.xlsx", sheet_name=1)
```

### JSON

```python
df = load("MyDataset/data.json")
```

For line-delimited JSON:

```python
df = load("MyDataset/data.json", lines=True)
```

### Parquet

```python
df = load("MyDataset/data.parquet")
```

Parquet files may require `pyarrow`:

```python
%pip install pyarrow
```

Restart the notebook kernel after installing it.

## 8. Load several files

```python
users = load(
    "FinancialTransactionsDatasetAnalytics(Kaggle)/users_data.csv"
)

transactions = load(
    "FinancialTransactionsDatasetAnalytics(Kaggle)/transactions_data.csv"
)

mcc_codes = load(
    "FinancialTransactionsDatasetAnalytics(Kaggle)/mcc_codes.json"
)
```

You can then combine or analyse them with pandas:

```python
transactions.head()
transactions.groupby("client_id").size()
```

## 9. A reusable notebook starter

Copy this into a new training notebook:

```python
from onedrive_loader import files, load

# 1. Choose a dataset folder
dataset_folder = "FinancialTransactionsDatasetAnalytics(Kaggle)"

# 2. Check its available files
print(files(dataset_folder))

# 3. Choose and load one file
filename = "users_data.csv"
df = load(f"{dataset_folder}/{filename}")

# 4. Explore the data
print("Rows and columns:", df.shape)
display(df.head())
df.info()
```

To change datasets, edit only these two variables:

```python
dataset_folder = "AnotherDataset"
filename = "another_file.csv"
```

## 10. Older function names

The older functions are still supported:

```python
from onedrive_loader import load_csv, list_files

list_files("MyDataset")
df = load_csv("MyDataset", "data.csv")
```

For new notebooks, prefer the simpler `files()` and `load()` functions.

## 11. Troubleshooting

### `ModuleNotFoundError: No module named 'onedrive_loader'`

Make sure `/Users/teslim/OneDriveFileLoader` is available to Python.

Temporary notebook solution:

```python
import sys

sys.path.append("/Users/teslim/OneDriveFileLoader")

from onedrive_loader import files, load
```

If you add the directory after an import has already failed, rerun the import.

### HTTP 404 or `FileNotFoundError`

The folder or filename does not exactly match OneDrive.

Inspect each level:

```python
files()
```

```python
files("MyDataset")
```

Copy the exact folder and filename displayed, including spaces, brackets and
capital letters.

Remember that paths are relative to `TeslimDataLakes`:

```python
# Correct
files("MyDataset")

# Incorrect
files("TeslimDataLakes/MyDataset")
```

### Missing credentials

The loader expects this file:

```text
/Users/teslim/OneDriveFileLoader/.env
```

It must contain:

```text
SHAREPOINT_CLIENT_ID=your-client-id
SHAREPOINT_TENANT_ID=your-tenant-id
SHAREPOINT_CLIENT_SECRET=your-client-secret
```

Do not place these secret values directly in notebooks or share the `.env`
file.

### Excel dependency error

Install the Excel reader:

```python
%pip install openpyxl
```

Restart the notebook kernel afterward.

### The loader was updated but the notebook uses the old version

Restart the notebook kernel. Alternatively, reload it:

```python
import onedrive_loader
import importlib

importlib.reload(onedrive_loader)

from onedrive_loader import files, load
```

## Quick reference

```python
from onedrive_loader import files, load

files()                              # List all dataset folders
files("MyDataset")                   # List a dataset's contents
df = load("MyDataset/data.csv")      # Load CSV
df = load("MyDataset/data.xlsx")     # Load Excel
df = load("MyDataset/data.json")     # Load JSON
df = load("MyDataset/data.parquet")  # Load Parquet
df.head()                            # Preview data
```
