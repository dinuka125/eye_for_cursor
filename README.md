# Eye for Cursor MCP Server

A powerful Model Context Protocol (MCP) server that provides visual analysis capabilities for Cursor IDE, including screenshot capture, accessibility auditing, and UI component analysis.

## 🚀 Features

- **Screenshot Capture**: Take screenshots of any website with customizable viewport sizes
- **Visual Analysis**: Detect UI component boundaries and analyze layouts
- **Accessibility Auditing**: Run comprehensive accessibility audits using axe-core
- **Memory Management**: Intelligent memory cleanup with "use-and-discard" pattern
- **Console Logging**: Capture browser console logs for debugging
- **User Actions**: Simulate user interactions (click, type) on web pages
- **Design System Validation**: Check adherence to design system rules

## 📋 Prerequisites

- Python 3.8 or higher
- Cursor IDE
- Windows/macOS/Linux

## 🛠️ Installation

### 1. Clone or Download
```bash
# If using git
git clone <repository-url>
cd Eye_for_Cursor

# Or download and extract the ZIP file
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers
```bash
playwright install
```

### 5. Test Installation
```bash
python test_installation_simple.py
```

## ⚙️ Cursor Configuration

### 1. Open Cursor Settings
- Press `Ctrl+,` (Windows/Linux) or `Cmd+,` (macOS)
- Go to "Features" → "Model Context Protocol"

### 2. Add MCP Server
Add this configuration to your MCP settings:

```json
{
  "mcpServers": {
    "eye-for-cursor": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "D:\\MCP Servers\\Eye_for_Cursor",
      "env": {
        "PYTHONPATH": "D:\\MCP Servers\\Eye_for_Cursor"
      }
    }
  }
}
```

**Important**: Update the `cwd` path to match your installation directory.

### 3. Restart Cursor
Restart Cursor IDE to load the MCP server.

## 🧪 Testing

### Quick Test
```bash
python quick_test.py
```

### Manual Test
1. Open Cursor IDE
2. Start a new chat
3. Ask: "Take a screenshot of google.com"
4. Cursor should capture and display the screenshot

## 📖 Usage Examples

### Basic Screenshot
```
Take a screenshot of https://example.com
```

### Screenshot with Custom Viewport
```
Take a screenshot of https://example.com with viewport 1920x1080
```

### Accessibility Audit
```
Run an accessibility audit on https://example.com
```

### UI Component Analysis
```
Analyze the UI components on https://example.com
```

## 🔧 Available Tools

| Tool | Description |
|------|-------------|
| `capture_screenshot` | Take screenshots of websites |
| `get_component_boundaries` | Detect UI component boundaries |
| `run_accessibility_audit` | Run accessibility audits |
| `get_browser_console_logs` | Capture browser console logs |
| `execute_user_action` | Simulate user interactions |
| `get_element_computed_style` | Get CSS computed styles |
| `compare_with_baseline` | Compare screenshots for visual regression |
| `check_design_system_adherence` | Validate design system compliance |
| `cleanup_session` | Clean up memory and files |
| `get_memory_usage` | Check memory usage |
| `discard_screenshot` | Discard specific screenshots from memory |

## 🧹 Memory Management

The server uses intelligent memory management:

- **Default**: Screenshots are discarded after Cursor analysis (use-and-discard pattern)
- **Optional**: Screenshots can be kept in memory for comparison workflows
- **Automatic**: Old files and memory cache are cleaned up automatically
- **Manual**: Session cleanup available when needed

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **Playwright browser errors**
   - Run `playwright install`

3. **Permission errors**
   - Ensure you have write permissions to the project directory

4. **Memory issues**
   - The server automatically manages memory
   - Use `cleanup_session` if needed

### Getting Help

1. Check the logs in the terminal where you started the server
2. Run `python test_installation_simple.py` to verify setup
3. Check memory usage with `get_memory_usage` tool

## 📁 Project Structure

```
Eye_for_Cursor/
├── main.py                    # MCP server entry point
├── main_mcp_functions.py      # Core functionality
├── requirements.txt           # Python dependencies
├── test_installation_simple.py # Installation test script
├── quick_test.py              # Quick functionality test
├── setup_guide.md            # Detailed setup instructions
├── screenshots/              # Screenshot storage directory
└── README.md                 # This file
```

## 🔄 Updates

To update the MCP server:

1. Pull latest changes or download new version
2. Activate virtual environment
3. Run `pip install -r requirements.txt`
4. Restart Cursor IDE

## 📝 License

[Add your license information here]

## 🤝 Contributing

We welcome contributions! Follow these steps to propose changes:

1) Fork and clone
- Fork the repository on GitHub
- Clone your fork and create a feature branch
  - `git checkout -b feat/<short-feature-name>`

2) Local setup
- Create and activate a virtual environment
- Install dependencies: `pip install -r requirements.txt`
- Install Playwright browsers: `playwright install`

3) Make your changes
- Keep code clear, typed, and well-structured
- Add or update docstrings where helpful
- Prefer small, focused commits with clear messages (Conventional Commits recommended:
  - `feat: ...`, `fix: ...`, `docs: ...`, `refactor: ...`, `test: ...`)

4) Validate your changes
- Run the quick tests: `python quick_test.py`
- Run the installation check: `python test_installation_simple.py`
- Manually verify key flows if applicable (e.g., screenshot capture in Cursor)

5) Update documentation
- Update `README.md` and/or `setup_guide.md` if behavior or setup changes
- Add examples where it improves clarity

6) Open a Pull Request
- Push your branch and open a PR from your fork to `master`
- Fill in a clear description: what changed, why, and how it was tested
- Link any related issues

7) Review process
- Be ready to address review comments
- Squash or clean up commits if requested

Code style and quality
- Match existing formatting and naming conventions
- Avoid introducing linter errors (run locally if you use a linter)
- Keep functions small and purposeful; add types where possible

Security & privacy
- Do not commit secrets or credentials
- Avoid logging sensitive data

By contributing, you agree your code will be licensed under this project’s license.

---

**Need help?** Check the troubleshooting section or contact the development team.
