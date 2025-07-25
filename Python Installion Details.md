# 🐍 Python Installation Guide

This guide explains how to install Python on Windows, macOS, and Linux.

---

## ✅ Check If Python Is Already Installed

Open a terminal or command prompt and type:

```bash
python --version
```

or

```bash
python3 --version
```

If you see a version number like `Python 3.11.5`, you’re good to go.

---

## 💻 Windows Installation

1. Go to the official site: [https://www.python.org/downloads](https://www.python.org/downloads)
2. Click on **Download Python 3.x.x**.
3. Open the installer.
4. ✅ Check **"Add Python to PATH"**.
5. Click **Install Now**.
6. After installation, confirm with:
   ```cmd
   python --version
   ```

---

## 🍎 macOS Installation

### Option 1: Using Homebrew (Recommended)
1. Install Homebrew (if not already):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Python:
   ```bash
   brew install python
   ```

### Option 2: From Python.org
1. Visit: [https://www.python.org/downloads/mac-osx](https://www.python.org/downloads/mac-osx)
2. Download the `.pkg` installer.
3. Install it and confirm with:
   ```bash
   python3 --version
   ```

---

## 🐧 Linux Installation

Most distros come with Python pre-installed. To install or update manually:

### Debian / Ubuntu
```bash
sudo apt update
sudo apt install python3
```

### Fedora
```bash
sudo dnf install python3
```

### Arch
```bash
sudo pacman -S python
```

Confirm:
```bash
python3 --version
```

---

## 🧪 Verify Installation

Run the Python shell:
```bash
python   # or python3
```

You should see something like:
```
Python 3.x.x (default, ...)
>>> 
```

To exit:
```python
exit()
```
or press `Ctrl + D` / `Ctrl + Z` (Windows)

---

## 🎉 You’re All Set!

Python is now installed. You can start writing code using:
- Built-in `IDLE`
- Code editors like **VS Code**, **PyCharm**, or **Sublime Text**

---

## 🔧 Optional: Install `pip` and Virtual Environment

```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m venv myenv
```

Then activate:
- Windows: `myenv\Scripts\activate`
- macOS/Linux: `source myenv/bin/activate`

---

Happy coding, legend! 🧑‍💻🔥
