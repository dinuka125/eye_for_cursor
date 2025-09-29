from typing import List, Dict, Any, Tuple
from functools import wraps
from fastmcp import FastMCP
import main_mcp_functions as mcp_tools

# 1. Initialize the FastMCP server
mcp = FastMCP(name="Eye for Cursor MCP Server")

# 2. Explicitly wrap and register each function, preserving docstrings with @wraps

@mcp.tool()
@wraps(mcp_tools.capture_screenshot)
async def capture_screenshot(*args, **kwargs):
    return await mcp_tools.capture_screenshot(*args, **kwargs)

@mcp.tool()
@wraps(mcp_tools.get_component_boundaries)
def get_component_boundaries(*args, **kwargs):
    return mcp_tools.get_component_boundaries(*args, **kwargs)

@mcp.tool()
@wraps(mcp_tools.compare_with_baseline)
def compare_with_baseline(*args, **kwargs):
    return mcp_tools.compare_with_baseline(*args, **kwargs)

@mcp.tool()
@wraps(mcp_tools.check_design_system_adherence)
async def check_design_system_adherence(*args, **kwargs):
    return await mcp_tools.check_design_system_adherence(*args, **kwargs)

@mcp.tool()
@wraps(mcp_tools.get_browser_console_logs)
async def get_browser_console_logs(*args, **kwargs):
    return await mcp_tools.get_browser_console_logs(*args, **kwargs)

@mcp.tool()
@wraps(mcp_tools.get_element_computed_style)
async def get_element_computed_style(*args, **kwargs):
    return await mcp_tools.get_element_computed_style(*args, **kwargs)

@mcp.tool()
@wraps(mcp_tools.execute_user_action)
async def execute_user_action(*args, **kwargs):
    return await mcp_tools.execute_user_action(*args, **kwargs)

@mcp.tool()
@wraps(mcp_tools.map_element_to_source_code)
async def map_element_to_source_code(*args, **kwargs):
    return await mcp_tools.map_element_to_source_code(*args, **kwargs)

@mcp.tool()
@wraps(mcp_tools.run_accessibility_audit)
async def run_accessibility_audit(*args, **kwargs):
    return await mcp_tools.run_accessibility_audit(*args, **kwargs)

@mcp.tool()
@wraps(mcp_tools.cleanup_session)
def cleanup_session(*args, **kwargs):
    return mcp_tools.cleanup_session(*args, **kwargs)

@mcp.tool()
@wraps(mcp_tools.get_memory_usage)
def get_memory_usage(*args, **kwargs):
    return mcp_tools.get_memory_usage(*args, **kwargs)

@mcp.tool()
@wraps(mcp_tools.discard_screenshot)
def discard_screenshot(*args, **kwargs):
    return mcp_tools.discard_screenshot(*args, **kwargs)


# 3. Add a main entry point to run the server
if __name__ == "__main__":
    # The server is started using the `fastmcp run` command,
    # and this call is necessary for it to work.
    mcp.run()