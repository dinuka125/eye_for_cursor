#!/usr/bin/env python3
"""
Quick test script to verify MCP server functionality.
This script demonstrates the main features without requiring Cursor IDE.
"""

import asyncio
import json
from pathlib import Path

async def test_screenshot_capture():
    """Test screenshot capture functionality"""
    print("📸 Testing Screenshot Capture...")
    
    try:
        import main_mcp_functions
        
        # Test basic screenshot
        result = await main_mcp_functions.capture_screenshot('https://example.com')
        
        if result['success']:
            print(f"✅ Screenshot captured successfully")
            print(f"   - URL: {result['url']}")
            print(f"   - Viewport: {result['viewport']}")
            print(f"   - File: {result['file_path']}")
            print(f"   - Base64 length: {len(result['base64_image'])} characters")
            print(f"   - Memory usage: {result['memory_usage']['rss_mb']:.1f}MB")
            return True
        else:
            print(f"❌ Screenshot failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Screenshot test error: {e}")
        return False

async def test_accessibility_audit():
    """Test accessibility audit functionality"""
    print("\n♿ Testing Accessibility Audit...")
    
    try:
        import main_mcp_functions
        
        violations = await main_mcp_functions.run_accessibility_audit('https://example.com')
        
        print(f"✅ Accessibility audit completed")
        print(f"   - Violations found: {len(violations)}")
        
        if violations:
            print("   - Sample violations:")
            for i, violation in enumerate(violations[:3]):  # Show first 3
                print(f"     {i+1}. {violation.get('description', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Accessibility audit error: {e}")
        return False

def test_component_analysis():
    """Test component boundary analysis"""
    print("\n🔍 Testing Component Analysis...")
    
    try:
        import main_mcp_functions
        
        # First take a screenshot
        screenshot_result = asyncio.run(main_mcp_functions.capture_screenshot('https://example.com'))
        
        if screenshot_result['success']:
            # Analyze the screenshot
            components = main_mcp_functions.get_component_boundaries(screenshot_result['file_path'])
            
            print(f"✅ Component analysis completed")
            print(f"   - Components detected: {len(components)}")
            
            if components:
                print("   - Sample components:")
                for i, component in enumerate(components[:3]):  # Show first 3
                    box = component.get('box', [])
                    print(f"     {i+1}. Box: {box}, Label: {component.get('label', 'N/A')}")
            
            return True
        else:
            print("❌ Could not take screenshot for component analysis")
            return False
            
    except Exception as e:
        print(f"❌ Component analysis error: {e}")
        return False

async def test_console_logs():
    """Test console log capture"""
    print("\n📝 Testing Console Log Capture...")
    
    try:
        import main_mcp_functions
        
        logs = await main_mcp_functions.get_browser_console_logs('https://example.com')
        
        print(f"✅ Console log capture completed")
        print(f"   - Logs captured: {len(logs)}")
        
        if logs:
            print("   - Sample logs:")
            for i, log in enumerate(logs[:3]):  # Show first 3
                print(f"     {i+1}. [{log.get('level', 'N/A')}] {log.get('message', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Console log test error: {e}")
        return False

def test_memory_management():
    """Test memory management features"""
    print("\n🧹 Testing Memory Management...")
    
    try:
        import main_mcp_functions
        
        # Test memory usage
        memory_info = main_mcp_functions.get_memory_usage()
        print(f"✅ Memory usage tracking works")
        print(f"   - RSS Memory: {memory_info['rss_mb']:.1f}MB")
        print(f"   - VMS Memory: {memory_info['vms_mb']:.1f}MB")
        print(f"   - Cached screenshots: {memory_info['cache_entries']}")
        
        # Test cleanup
        main_mcp_functions.cleanup_session()
        print("✅ Session cleanup works")
        
        return True
        
    except Exception as e:
        print(f"❌ Memory management test error: {e}")
        return False

async def test_user_actions():
    """Test user action simulation"""
    print("\n🖱️ Testing User Actions...")
    
    try:
        import main_mcp_functions
        
        # Test a simple click action
        action = {
            "type": "click",
            "selector": "body"  # Click on body element
        }
        
        result = await main_mcp_functions.execute_user_action('https://example.com', action)
        
        if result['status'] == 'success':
            print(f"✅ User action simulation works")
            print(f"   - Action: {result['action']}")
            print(f"   - Screenshot: {result['screenshot_path']}")
            print(f"   - Base64 length: {len(result['base64_image'])} characters")
            return True
        else:
            print(f"❌ User action failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ User action test error: {e}")
        return False

async def main():
    """Run all quick tests"""
    print("🚀 Eye for Cursor MCP Server - Quick Test")
    print("=" * 50)
    
    tests = [
        ("Screenshot Capture", test_screenshot_capture),
        ("Accessibility Audit", test_accessibility_audit),
        ("Component Analysis", test_component_analysis),
        ("Console Logs", test_console_logs),
        ("Memory Management", test_memory_management),
        ("User Actions", test_user_actions),
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
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Quick Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All quick tests passed! The MCP server is working correctly.")
        print("\nThe server is ready for use with Cursor IDE!")
    else:
        print("❌ Some tests failed. Please check the installation.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
