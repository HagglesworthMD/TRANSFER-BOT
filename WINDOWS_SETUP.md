# Windows Batch File Setup Instructions

## If you get "system cannot find the path specified" error:

### Option 1: Install dependencies globally
```bash
pip install streamlit pandas plotly python-dateutil
```

Then the bat files will use your system Python.

### Option 2: Create virtual environment (recommended)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Then the bat files will automatically use the venv.

### Option 3: Install Python (if not installed)
Download from: https://www.python.org/downloads/
Make sure to check "Add Python to PATH" during installation.

## Current Status:
The bat files are smart - they try venv first, then fall back to system Python.

## Quick Test:
```bash
# Check if Python is installed
python --version

# Check if streamlit is installed
python -m streamlit --version

# If not, install it:
pip install streamlit pandas plotly python-dateutil
```
