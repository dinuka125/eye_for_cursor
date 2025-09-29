import asyncio
import uuid
import base64
import gc
import os
import time
from pathlib import Path
from typing import Tuple, Dict, Any, List
from io import BytesIO

# Playwright for browser automation
from playwright.async_api import async_playwright, Error

# Axe for accessibility audits
from axe_playwright_python.async_playwright import Axe

# Libraries for image processing and comparison
from skimage.metrics import structural_similarity as ssim
import numpy as np
from PIL import Image
import cv2

# Define and create a local directory for screenshots
SCREENSHOT_DIR = Path.cwd() / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)

# Memory management settings
MAX_SCREENSHOTS_IN_MEMORY = 10  # Maximum screenshots to keep in memory
SCREENSHOT_CLEANUP_INTERVAL = 300  # Clean up every 5 minutes
MAX_FILE_AGE_HOURS = 24  # Delete files older than 24 hours

# Global variables for memory management
_screenshot_cache = {}  # Store recent screenshots with timestamps
_last_cleanup = time.time()


# ----------------------------------------
# ## 🧹 Memory Management & Cleanup
# ----------------------------------------

def cleanup_old_files():
    """Remove screenshot files older than MAX_FILE_AGE_HOURS"""
    try:
        current_time = time.time()
        max_age_seconds = MAX_FILE_AGE_HOURS * 3600
        
        for file_path in SCREENSHOT_DIR.glob("*.png"):
            if current_time - file_path.stat().st_mtime > max_age_seconds:
                file_path.unlink()
                print(f"Cleaned up old file: {file_path.name}")
    except Exception as e:
        print(f"Error during file cleanup: {e}")

def cleanup_memory_cache():
    """Remove old entries from memory cache"""
    global _screenshot_cache, _last_cleanup
    
    current_time = time.time()
    
    # Remove entries older than 1 hour
    max_age = 3600  # 1 hour
    _screenshot_cache = {
        key: value for key, value in _screenshot_cache.items()
        if current_time - value.get('timestamp', 0) < max_age
    }
    
    # If still too many, remove oldest ones
    if len(_screenshot_cache) > MAX_SCREENSHOTS_IN_MEMORY:
        sorted_items = sorted(_screenshot_cache.items(), key=lambda x: x[1].get('timestamp', 0))
        items_to_remove = len(_screenshot_cache) - MAX_SCREENSHOTS_IN_MEMORY
        
        for i in range(items_to_remove):
            key = sorted_items[i][0]
            del _screenshot_cache[key]
    
    _last_cleanup = current_time
    print(f"Memory cleanup completed. Cache size: {len(_screenshot_cache)}")

def get_memory_usage():
    """Get current memory usage information"""
    import psutil
    process = psutil.Process()
    memory_info = process.memory_info()
    return {
        "rss_mb": memory_info.rss / 1024 / 1024,  # Resident Set Size
        "vms_mb": memory_info.vms / 1024 / 1024,  # Virtual Memory Size
        "cache_entries": len(_screenshot_cache)
    }

def discard_screenshot(screenshot_id: str) -> Dict[str, Any]:
    """Discard a specific screenshot from memory after Cursor analysis"""
    global _screenshot_cache
    
    if screenshot_id in _screenshot_cache:
        del _screenshot_cache[screenshot_id]
        print(f"Screenshot {screenshot_id} discarded from memory")
        return {
            "success": True,
            "message": f"Screenshot {screenshot_id} discarded",
            "remaining_cache": len(_screenshot_cache)
        }
    else:
        return {
            "success": False,
            "message": f"Screenshot {screenshot_id} not found in cache",
            "remaining_cache": len(_screenshot_cache)
        }

def cleanup_session():
    """Clean up all memory and files at the end of a session"""
    global _screenshot_cache
    
    # Clear memory cache
    _screenshot_cache.clear()
    
    # Clean up old files
    cleanup_old_files()
    
    # Force garbage collection
    gc.collect()
    
    print("Session cleanup completed")

# ----------------------------------------
# ## 👁️ Visual Analysis & "Sight"
# ----------------------------------------

async def capture_screenshot(url: str, viewport: Tuple[int, int] = (1920, 1080), keep_in_memory: bool = False) -> Dict[str, Any]:
    """
    Captures a screenshot of a given URL at a specific viewport size.
    Returns both file path and base64 encoded image data for Cursor integration.
    
    Args:
        url: URL to capture
        viewport: Screenshot dimensions (width, height)
        keep_in_memory: If False (default), image is discarded after returning to Cursor
                       If True, image is kept in memory cache for later use
    """
    global _screenshot_cache, _last_cleanup
    
    # Check if we need to clean up memory
    current_time = time.time()
    if current_time - _last_cleanup > SCREENSHOT_CLEANUP_INTERVAL:
        cleanup_memory_cache()
        cleanup_old_files()
    
    screenshot_path = SCREENSHOT_DIR / f"{uuid.uuid4()}.png"

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.set_viewport_size({"width": viewport[0], "height": viewport[1]})
            await page.goto(url, wait_until="networkidle")
            
            # Capture screenshot to file
            await page.screenshot(path=screenshot_path)
            
            # Also capture to memory for base64 encoding
            screenshot_bytes = await page.screenshot()
            
            await browser.close()
            
            # Convert to base64 for Cursor integration
            base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')
            
            # Only store in memory cache if explicitly requested
            screenshot_id = None
            if keep_in_memory:
                screenshot_id = str(uuid.uuid4())
                _screenshot_cache[screenshot_id] = {
                    'base64_image': base64_image,
                    'url': url,
                    'viewport': viewport,
                    'timestamp': current_time,
                    'file_path': str(screenshot_path)
                }
                print(f"Screenshot cached in memory with ID: {screenshot_id}")
            else:
                print("Screenshot will be discarded after Cursor analysis (use-and-discard mode)")
            
            # Get memory usage info
            memory_info = get_memory_usage()
            
            print(f"Screenshot saved to {screenshot_path}")
            print(f"Memory usage: {memory_info['rss_mb']:.1f}MB RSS, {memory_info['cache_entries']} cached screenshots")
            
            return {
                "success": True,
                "file_path": str(screenshot_path),
                "base64_image": base64_image,
                "url": url,
                "viewport": viewport,
                "screenshot_id": screenshot_id,
                "keep_in_memory": keep_in_memory,
                "memory_usage": memory_info,
                "error": None
            }
        except Error as e:
            print(f"Error occurred with Playwright: {e}")
            return {
                "success": False,
                "file_path": None,
                "base64_image": None,
                "url": url,
                "viewport": viewport,
                "screenshot_id": None,
                "memory_usage": get_memory_usage(),
                "error": str(e)
            }

def get_component_boundaries(screenshot_path: str) -> List[Dict[str, Any]]:
    """
    Analyzes a screenshot to detect and return the bounding boxes of UI components.
    This is a proof-of-concept using basic contour detection.
    """
    if not Path(screenshot_path).exists():
        return []
    img = cv2.imread(str(screenshot_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 30, 200)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boundaries = []
    for contour in contours:
        if cv2.contourArea(contour) > 100:
            x, y, w, h = cv2.boundingRect(contour)
            boundaries.append({"box": [x, y, x + w, y + h], "label": "component"})
    return boundaries

def compare_with_baseline(current_screenshot_path: str, baseline_screenshot_path: str) -> Dict[str, Any]:
    """
    Performs visual regression testing by comparing two screenshots using SSIM.
    """
    try:
        current_img = Image.open(current_screenshot_path).convert("L")
        baseline_img = Image.open(baseline_screenshot_path).convert("L")
        if current_img.size != baseline_img.size:
            baseline_img = baseline_img.resize(current_img.size)
        current_array = np.array(current_img)
        baseline_array = np.array(baseline_img)
        score, _ = ssim(current_array, baseline_array, full=True)
        return {"similarity_score": score, "error": None}
    except FileNotFoundError as e:
        return {"similarity_score": 0, "error": f"File not found: {e}"}

async def check_design_system_adherence(screenshot_path: str, design_system_rules: Dict) -> List[str]:
    """
    Checks if the UI in the screenshot adheres to predefined design system rules.
    (Placeholder implementation)
    """
    violations = []
    if not Path(screenshot_path).exists():
        return ["Screenshot file not found."]
    
    allowed_colors = design_system_rules.get("colors", [])
    if not allowed_colors:
        violations.append("No colors defined in design system rules.")
    
    violations.append("NOTE: Color, font, and spacing checks are not yet fully implemented.")
    return violations


# ----------------------------------------
# ## ⚙️ Interactive Debugging & Control
# ----------------------------------------

async def get_browser_console_logs(url: str) -> List[Dict[str, str]]:
    """
    Navigates to a URL and captures all console logs (log, warn, error).
    """
    logs = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        page.on("console", lambda msg: logs.append({
            "level": msg.type, "message": msg.text, "location": msg.location
        }))
        try:
            await page.goto(url, wait_until="networkidle")
            await page.wait_for_timeout(1000)
        except Error as e:
            print(f"❌ Error navigating to {url}: {e}")
        finally:
            await browser.close()
    return logs

async def get_element_computed_style(url: str, element_selector: str) -> Dict[str, str]:
    """
    Retrieves the final, computed CSS properties for a specific DOM element.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="networkidle")
            element = await page.query_selector(element_selector)
            if not element:
                return {"error": f"Element with selector '{element_selector}' not found."}
            
            # Inject JavaScript to get computed styles
            styles = await element.evaluate('''
                (element) => {
                    const computedStyle = window.getComputedStyle(element);
                    const style = {};
                    for (let i = 0; i < computedStyle.length; i++) {
                        const prop = computedStyle[i];
                        style[prop] = computedStyle.getPropertyValue(prop);
                    }
                    return style;
                }
            ''')
            return styles
        except Error as e:
            return {"error": str(e)}
        finally:
            await browser.close()

async def execute_user_action(url: str, action: Dict) -> Dict[str, Any]:
    """
    Performs a simulated user action on a web page and returns the result.
    """
    screenshot_path = SCREENSHOT_DIR / f"{uuid.uuid4()}_action.png"
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="load")
            action_type = action.get("type")
            selector = action.get("selector")
            if not action_type or not selector:
                raise ValueError("Action 'type' and 'selector' are required.")
            if action_type == "click":
                await page.click(selector, timeout=5000)
            elif action_type == "type":
                text_to_type = action.get("text", "")
                await page.fill(selector, text_to_type, timeout=5000)
            else:
                raise ValueError(f"Unsupported action type: {action_type}")
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path=screenshot_path)
            
            # Also capture to memory for base64 encoding
            screenshot_bytes = await page.screenshot()
            base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')
            
            return {
                "status": "success", 
                "screenshot_path": str(screenshot_path),
                "base64_image": base64_image,
                "action": action,
                "error": None
            }
        except (Error, ValueError) as e:
            return {
                "status": "error", 
                "screenshot_path": None, 
                "base64_image": None,
                "action": action,
                "error": str(e)
            }
        finally:
            await browser.close()

# ----------------------------------------
# ## 🧠 Code & Component Intelligence
# ----------------------------------------

async def map_element_to_source_code(url: str, element_selector: str) -> Dict[str, Any]:
    """
    Maps a rendered DOM element back to its source code file and line number.
    (Placeholder: This is an advanced feature requiring source maps)
    """
    return {
        "file": "src/components/Button.tsx",
        "line": 25,
        "component": "Button",
        "note": "This is a placeholder. A real implementation requires build-time metadata and source map parsing."
    }

async def run_accessibility_audit(url: str) -> List[Dict[str, Any]]:
    """
    Runs an accessibility audit on the given page using axe-core.
    """
    violations = []
    axe = Axe()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="networkidle")
            results = await axe.run(page)
            violations = results.violations if hasattr(results, 'violations') else []
        except Error as e:
            print(f"Could not run audit on {url}: {e}")
        finally:
            await browser.close()
    return violations