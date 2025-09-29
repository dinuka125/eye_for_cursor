#!/usr/bin/env python3
"""
Simple test script to verify MCP server installation and functionality.
Run this script to ensure everything is set up correctly.
"""

import sys
import asyncio
import subprocess
from pathlib import Path

def test_python_version():
    """Test if Python version is compatible"""
    print("Testing Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"ERROR: Python {version.major}.{version.minor} is not supported. Please use Python 3.8 or higher.")
        return False
    print(f"SUCCESS: Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("\nTesting dependencies...")
    
    required_packages = [
        'fastmcp',
        'playwright',
        'opencv-python',
        'numpy',
        'scikit-image',
        'Pillow',
        'axe-playwright-python',
        'psutil'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'opencv-python':
                __import__('cv2')
            elif package == 'scikit-image':
                __import__('skimage')
            elif package == 'axe-playwright-python':
                __import__('axe_playwright_python')
            elif package == 'Pillow':
                __import__('PIL')
            else:
                __import__(package.replace('-', '_'))
            print(f"SUCCESS: {package}")
        except ImportError:
            print(f"ERROR: {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nERROR: Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("SUCCESS: All dependencies are installed")
    return True

async def test_playwright_browsers():
    """Test if Playwright browsers are installed"""
    print("\nTesting Playwright browsers...")
    
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            await browser.close()
        print("SUCCESS: Playwright browsers are installed")
        return True
    except Exception as e:
        print(f"ERROR: Playwright browsers not installed: {e}")
        print("Run: playwright install")
        return False

def test_mcp_server_import():
    """Test if MCP server can be imported"""
    print("\nTesting MCP server import...")
    
    try:
        import main
        import main_mcp_functions
        print("SUCCESS: MCP server modules can be imported")
        return True
    except Exception as e:
        print(f"ERROR: Failed to import MCP server: {e}")
        return False

async def test_screenshot_functionality():
    """Test screenshot functionality"""
    print("\nTesting screenshot functionality...")
    
    try:
        import main_mcp_functions
        
        # Test with a simple URL
        result = await main_mcp_functions.capture_screenshot('https://example.com', keep_in_memory=False)
        
        if result['success']:
            print("SUCCESS: Screenshot capture works")
            print(f"   - File saved: {result['file_path']}")
            print(f"   - Base64 data length: {len(result['base64_image'])}")
            print(f"   - Memory usage: {result['memory_usage']['rss_mb']:.1f}MB")
            return True
        else:
            print(f"ERROR: Screenshot capture failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"ERROR: Screenshot test failed: {e}")
        return False

def test_memory_management():
    """Test memory management functions"""
    print("\nTesting memory management...")
    
    try:
        import main_mcp_functions
        
        # Test memory usage function
        memory_info = main_mcp_functions.get_memory_usage()
        print(f"SUCCESS: Memory usage tracking works: {memory_info['rss_mb']:.1f}MB RSS")
        
        # Test cleanup function
        main_mcp_functions.cleanup_session()
        print("SUCCESS: Session cleanup works")
        
        return True
    except Exception as e:
        print(f"ERROR: Memory management test failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'main.py',
        'main_mcp_functions.py',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"SUCCESS: {file}")
        else:
            print(f"ERROR: {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\nERROR: Missing files: {', '.join(missing_files)}")
        return False
    
    print("SUCCESS: All required files are present")
    return True

async def main():
    """Run all tests"""
    print("Eye for Cursor MCP Server - Installation Test")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Playwright Browsers", test_playwright_browsers),
        ("MCP Server Import", test_mcp_server_import),
        ("File Structure", test_file_structure),
        ("Memory Management", test_memory_management),
        ("Screenshot Functionality", test_screenshot_functionality),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                passed += 1
        except Exception as e:
            print(f"ERROR: {test_name} test crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All tests passed! Your MCP server is ready to use.")
        print("\nNext steps:")
        print("1. Configure Cursor IDE with the MCP server")
        print("2. Restart Cursor IDE")
        print("3. Test with: 'Take a screenshot of google.com'")
    else:
        print("ERROR: Some tests failed. Please fix the issues above before using the MCP server.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
