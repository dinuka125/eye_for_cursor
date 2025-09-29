# Eye for Cursor MCP Server - Setup Guide

This guide will walk you through setting up the Eye for Cursor MCP Server step by step.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** installed on your system
- **Cursor IDE** installed and running
- **Administrator/root privileges** (for installing system packages)

## 🚀 Step-by-Step Installation

### Step 1: Download the MCP Server

1. **Download the package** from the shared location
2. **Extract** the files to a convenient location (e.g., `C:\MCP_Servers\Eye_for_Cursor\`)
3. **Note the full path** - you'll need it for Cursor configuration

### Step 2: Set Up Python Environment

1. **Open Command Prompt/Terminal** in the project directory
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Verify activation** - you should see `(venv)` in your prompt

### Step 3: Install Dependencies

1. **Install Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Playwright browsers:**
   ```bash
   playwright install
   ```

3. **Verify installation:**
   ```bash
   python test_installation.py
   ```

### Step 4: Configure Cursor IDE

1. **Open Cursor IDE**

2. **Access Settings:**
   - Press `Ctrl+,` (Windows/Linux) or `Cmd+,` (macOS)
   - Go to "Features" → "Model Context Protocol"

3. **Add MCP Server Configuration:**
   
   Add this JSON configuration to your MCP settings:
   
   ```json
   {
     "mcpServers": {
       "eye-for-cursor": {
         "command": "python",
         "args": ["main.py"],
         "cwd": "C:\\MCP_Servers\\Eye_for_Cursor",
         "env": {
           "PYTHONPATH": "C:\\MCP_Servers\\Eye_for_Cursor"
         }
       }
     }
   }
   ```
   
   **Important:** Replace `C:\\MCP_Servers\\Eye_for_Cursor` with your actual installation path.

4. **Save the configuration**

5. **Restart Cursor IDE**

### Step 5: Test the Installation

1. **Open a new chat** in Cursor IDE

2. **Test basic functionality:**
   ```
   Take a screenshot of https://google.com
   ```

3. **Expected result:** Cursor should capture and display a screenshot of Google's homepage

## 🧪 Verification Tests

### Quick Test (Recommended)
```bash
python quick_test.py
```

### Full Installation Test
```bash
python test_installation.py
```

### Manual Cursor Test
1. Open Cursor IDE
2. Start a new chat
3. Try these commands:
   - "Take a screenshot of https://example.com"
   - "Run an accessibility audit on https://example.com"
   - "Analyze the UI components on https://example.com"

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. "Module not found" errors
**Problem:** Python can't find the required modules
**Solution:**
```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Playwright browser errors
**Problem:** Browser automation fails
**Solution:**
```bash
# Install Playwright browsers
playwright install

# Or install specific browser
playwright install chromium
```

#### 3. Permission errors
**Problem:** Can't write to directories or files
**Solution:**
- Run Command Prompt as Administrator (Windows)
- Use `sudo` for system operations (macOS/Linux)
- Check file/folder permissions

#### 4. Cursor can't connect to MCP server
**Problem:** Cursor shows MCP connection errors
**Solution:**
- Verify the `cwd` path in Cursor configuration is correct
- Ensure the virtual environment is activated
- Check that `main.py` exists in the specified directory
- Restart Cursor IDE after configuration changes

#### 5. Memory issues
**Problem:** High memory usage or slow performance
**Solution:**
- The server automatically manages memory
- Use the `cleanup_session` tool if needed
- Check memory usage with `get_memory_usage` tool

### Debug Mode

To run the MCP server in debug mode:

1. **Open Command Prompt** in the project directory
2. **Activate virtual environment**
3. **Run with debug output:**
   ```bash
   python -c "import main; main.mcp.run()"
   ```

### Log Files

Check these locations for error logs:
- **Terminal output** where you started the server
- **Cursor IDE logs** (Help → Toggle Developer Tools → Console)
- **System logs** (Windows Event Viewer, macOS Console, Linux journalctl)

## 📁 File Structure

After installation, your directory should look like this:

```
Eye_for_Cursor/
├── main.py                    # MCP server entry point
├── main_mcp_functions.py      # Core functionality
├── requirements.txt           # Python dependencies
├── test_installation.py      # Installation test script
├── quick_test.py             # Quick functionality test
├── setup_guide.md            # This file
├── README.md                 # Main documentation
├── venv/                     # Virtual environment (created during setup)
└── screenshots/              # Screenshot storage (created automatically)
```

## 🔄 Updates

To update the MCP server:

1. **Download the latest version**
2. **Replace the old files** (keep your `venv` folder)
3. **Activate virtual environment**
4. **Update dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Restart Cursor IDE**

## 🆘 Getting Help

If you encounter issues:

1. **Check this guide** for common solutions
2. **Run the test scripts** to identify specific problems
3. **Check the troubleshooting section** above
4. **Contact the development team** with:
   - Error messages
   - Test script output
   - Your system information (OS, Python version, Cursor version)

## ✅ Success Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Playwright browsers installed (`playwright install`)
- [ ] Installation test passed (`python test_installation.py`)
- [ ] Cursor IDE configured with MCP server
- [ ] Cursor IDE restarted
- [ ] Quick test passed (`python quick_test.py`)
- [ ] Manual Cursor test successful

Once all items are checked, your MCP server is ready to use! 🎉
