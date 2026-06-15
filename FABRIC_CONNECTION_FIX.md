# Fix for SQL Server Connection Error

This setup fixes the connection error when trying to connect to Microsoft Fabric SQL Analytics Endpoint from Python on macOS.

## The Problem

```
A network-related or instance-specific error occurred while establishing a connection to SQL Server.
(provider: TCP Provider, error: 35 - An internal exception was caught)
```

## The Solution

### Quick Start (2 steps)

1. **Run the setup script** to install ODBC Driver:
   ```bash
   ./setup_fabric_connection.sh
   ```

2. **Open the notebook** and follow the examples:
   ```bash
   jupyter notebook fabric_sql_connection.ipynb
   ```

### What Gets Installed

- **ODBC Driver 18 for SQL Server** - Required for connecting to Fabric
- **Python packages**: `pyodbc`, `pandas`, `sqlalchemy`

### Get Your Connection Details

Before running the notebook, get your SQL Analytics Endpoint connection string:

1. Go to [Microsoft Fabric Portal](https://app.fabric.microsoft.com)
2. Navigate to your workspace
3. Click on **Dp900_lakehouse**
4. Switch to **SQL analytics endpoint** view (not Lakehouse view)
5. Copy the connection string from the top (looks like: `xxx.pbidedicated.windows.net`)

### Update the Notebook

In `fabric_sql_connection.ipynb`, replace:

```python
SERVER = 'your-workspace-name.pbidedicated.windows.net'  # ← Replace this
DATABASE = 'Dp900_lakehouse'  # ← This should be correct
```

## Troubleshooting

### If setup_fabric_connection.sh fails:

```bash
# Install ODBC driver manually
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
brew install msodbcsql18 mssql-tools18

# Verify installation
odbcinst -q -d -n "ODBC Driver 18 for SQL Server"
```

### If connection still fails:

1. **Check driver installation**:
   ```bash
   python -c "import pyodbc; print(pyodbc.drivers())"
   ```
   Should show: `ODBC Driver 18 for SQL Server`

2. **Verify you have access** to the Fabric workspace

3. **Check firewall/VPN** - Make sure you can reach `*.pbidedicated.windows.net`

4. **Try the test in the notebook** - It includes a verification cell

## Files Created

- `fabric_sql_connection.ipynb` - Complete working examples with 3 connection methods
- `setup_fabric_connection.sh` - Automated installation script
- `FABRIC_CONNECTION_FIX.md` - This guide

## Need Help?

Run the verification cell in the notebook to check your setup:
```python
import pyodbc
print("Available drivers:", pyodbc.drivers())
```
