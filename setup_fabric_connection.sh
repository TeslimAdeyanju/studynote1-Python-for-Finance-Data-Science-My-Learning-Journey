#!/bin/bash

echo "=========================================="
echo "Fabric SQL Connection Setup for macOS"
echo "=========================================="
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✓ Homebrew is installed"
fi

echo ""
echo "Installing Microsoft ODBC Driver 18 for SQL Server..."
echo ""

# Add Microsoft tap
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release 2>/dev/null

# Update Homebrew
brew update

# Install ODBC driver
echo "Installing msodbcsql18..."
HOMEBREW_NO_ENV_FILTERING=1 ACCEPT_EULA=Y brew install msodbcsql18 mssql-tools18

echo ""
echo "Verifying installation..."
echo ""

# Check if driver is installed
if odbcinst -q -d -n "ODBC Driver 18 for SQL Server" &> /dev/null; then
    echo "✓ ODBC Driver 18 for SQL Server is installed"
else
    echo "❌ ODBC Driver installation may have failed"
    echo "Try running: brew reinstall msodbcsql18"
    exit 1
fi

echo ""
echo "Installing Python packages..."
echo ""

# Install Python packages
pip install pyodbc pandas sqlalchemy

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Open fabric_sql_connection.ipynb"
echo "2. Get your SQL Analytics Endpoint connection string from Fabric portal:"
echo "   - Go to https://app.fabric.microsoft.com"
echo "   - Navigate to your workspace"
echo "   - Click on 'Dp900_lakehouse'"
echo "   - Switch to 'SQL analytics endpoint' view"
echo "   - Copy the connection string (looks like: xxx.pbidedicated.windows.net)"
echo "3. Replace the SERVER variable in the notebook with your connection string"
echo "4. Run the cells to connect!"
echo ""
echo "Available ODBC drivers on your system:"
odbcinst -q -d
