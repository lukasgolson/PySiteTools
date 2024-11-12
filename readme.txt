

# Sindex Package Installation Guide for Windows

## Installation Steps

### 1. Clone or Download the Repository
To obtain the `sindex` package, start by downloading or cloning the repository:

```bash
git clone https://github.com/lukasgolson/PySiteTools.git
cd PySiteTools
```

### 2. Install the Package
With your terminal open in the `PySiteTools` directory (the location containing `setup.py`), run the following command to install the package:

```bash
pip install .
```

If you'd like to install the package in **editable mode** (for development purposes), use:

```bash
pip install -e .
```

## Troubleshooting (Windows)

- **Permission Issues**: If you encounter permission-related issues, try running the command with administrative privileges (e.g., using `Run as Administrator`).

- **Internet Access**: Ensure you have an active internet connection during installation, as the necessary DLL file will be downloaded automatically.
