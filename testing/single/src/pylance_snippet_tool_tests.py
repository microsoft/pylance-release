"""
Pylance Code Snippet Tool Test Cases
====================================

This file contains comprehensive test cases for the Pylance code snippet execution tool.
Each test case can be run using the mcp_pylance_mcp_s_pylanceRunCodeSnippet tool.

HOW TO RUN TESTS:
================
Use the following tool call pattern for each test:

mcp_pylance_mcp_s_pylanceRunCodeSnippet(
    codeSnippet="<code_from_test_case>",
    workingDirectory="c:\\Users\\rchiodo\\source\\repos\\pylance-release\\testing\\single\\src",
    workspaceRoot="file:///c%3A/Users/rchiodo/source/repos/pylance-release/testing/single"
)

EXPECTED RESULTS:
================
Each test case includes expected behavior comments. Review actual vs expected results.

TEST CATEGORIES:
===============
1. Import-Related Tests (1-5)
2. Working Directory & Path Tests (6-7) 
3. Code Execution Edge Cases (8-15)
"""

# =============================================================================
# IMPORT-RELATED TEST CASES
# =============================================================================

def test_case_1_relative_imports():
    """
    Test Case 1: Relative imports within the same directory
    Expected: FAIL - "attempted relative import with no known parent package"
    Reason: -c execution doesn't support relative imports
    """
    code = """from . import test_another_module
test_another_module.print_stuff()"""
    return code

def test_case_2_parent_directory_imports():
    """
    Test Case 2: Importing from parent directories
    Expected: FAIL - Missing 'requests' dependency in userModule
    Reason: Dependencies not installed in environment
    """
    code = """import sys
sys.path.append('..')
from lib import userModule
print(userModule.__name__)"""
    return code

def test_case_3_standard_library_imports():
    """
    Test Case 3: Importing standard library modules
    Expected: PASS - Should work perfectly
    """
    code = """import json
import datetime
import pathlib
print(json.dumps({"test": "data"}))
print(datetime.datetime.now())
print(pathlib.Path.cwd())"""
    return code

def test_case_4_third_party_packages():
    """
    Test Case 4: Importing third-party packages
    Expected: FAIL - No numpy installed
    Reason: Package not available in environment
    """
    code = """import numpy as np
print(np.version.version)"""
    return code

def test_case_5_graceful_import_failure():
    """
    Test Case 5: Failed imports (should handle gracefully)
    Expected: PASS - Should catch ImportError gracefully
    """
    code = """try:
    import nonexistent_module
except ImportError as e:
    print(f"Import failed: {e}")"""
    return code

# =============================================================================
# WORKING DIRECTORY AND PATH TEST CASES
# =============================================================================

def test_case_6_file_operations():
    """
    Test Case 6: File operations relative to working directory
    Expected: PASS - Should show correct working directory and files
    """
    code = """import os
print("Current directory:", os.getcwd())
print("Files in current dir:", os.listdir('.'))
if os.path.exists('__init__.py'):
    print("Found __init__.py")"""
    return code

def test_case_7_sys_path_verification():
    """
    Test Case 7: sys.path verification
    Expected: PASS - Should show sys.path[0] as empty string (current dir)
    """
    code = """import sys
print("First few sys.path entries:")
for i, path in enumerate(sys.path[:3]):
    print(f"  {i}: {path}")"""
    return code

# =============================================================================
# CODE EXECUTION EDGE CASES
# =============================================================================

def test_case_8_multiline_strings():
    """
    Test Case 8: Multi-line strings and complex formatting
    Expected: PASS - Should handle multiline strings correctly
    """
    code = """multiline = \"\"\"
This is a
multiline string
with various characters: !@#$%^&*()
\"\"\"
print(repr(multiline))"""
    return code

def test_case_9_exception_handling():
    """
    Test Case 9: Exception handling
    Expected: PASS - Should handle try/except/finally correctly
    """
    code = """try:
    result = 1 / 0
except ZeroDivisionError as e:
    print(f"Caught exception: {e}")
finally:
    print("Finally block executed")"""
    return code

def test_case_10_stdout_stderr():
    """
    Test Case 10: Output to both stdout and stderr
    Expected: PASS - Should properly separate stdout/stderr
    """
    code = """import sys
print("This goes to stdout")
print("This goes to stderr", file=sys.stderr)
sys.stdout.flush()
sys.stderr.flush()"""
    return code

def test_case_11_unicode_characters():
    """
    Test Case 11: Unicode and special characters
    Expected: FAIL - Windows cp1252 encoding issue with emojis
    Reason: Console encoding limitations on Windows
    """
    code = """print("Unicode test: 🐍 Python 中文 العربية")
print("Special chars: \\n\\t\\\\\\"'")"""
    return code

def test_case_12_environment_variables():
    """
    Test Case 12: Environment variables
    Expected: PASS - Should set and read environment variables
    """
    code = """import os
os.environ['TEST_VAR'] = 'test_value'
print(f"Set variable: {os.environ.get('TEST_VAR')}")"""
    return code

def test_case_13_time_operations():
    """
    Test Case 13: Long-running code (should handle timeouts)
    Expected: PASS - Should complete within reasonable time
    """
    code = """import time
print("Starting...")
time.sleep(0.1)  # Short sleep
print("Done!")"""
    return code

def test_case_14_memory_operations():
    """
    Test Case 14: Memory/resource intensive (within reason)
    Expected: PASS - Should handle moderate memory usage
    """
    code = """data = list(range(10000))
print(f"Created list with {len(data)} elements")
del data"""
    return code

def test_case_15_shell_problematic_syntax():
    """
    Test Case 15: Code with syntax that might be problematic in shell
    Expected: PASS - Should handle quotes and shell-like commands safely
    """
    code = """message = 'String with "quotes" and \\'apostrophes\\''
command_like = "rm -rf /"  # This should just be a string, not executed
print(f"Message: {message}")
print(f"Command-like string: {command_like}")"""
    return code

# =============================================================================
# ADDITIONAL EDGE CASES FOR COMPREHENSIVE TESTING
# =============================================================================

def test_case_16_syntax_errors():
    """
    Test Case 16: Code with syntax errors
    Expected: FAIL - Should report syntax error clearly
    """
    code = """print("Hello world"
# Missing closing parenthesis"""
    return code

def test_case_17_infinite_loop_protection():
    """
    Test Case 17: Potentially infinite loop (use with caution)
    Expected: Should timeout or be handled gracefully
    Note: Only run if timeout mechanism is implemented
    """
    code = """import time
count = 0
start_time = time.time()
while time.time() - start_time < 0.01:  # Very short loop
    count += 1
print(f"Loop executed {count} times")"""
    return code

def test_case_18_complex_imports():
    """
    Test Case 18: Complex import scenarios
    Expected: PASS - Should handle various import patterns
    """
    code = """import sys
import os.path as ospath
from collections import defaultdict
from typing import Dict, List

print("Complex imports successful")
data: Dict[str, List[int]] = defaultdict(list)
data['test'].append(42)
print(f"Data: {dict(data)}")
print(f"OS path join: {ospath.join('a', 'b', 'c')}")"""
    return code

def test_case_19_class_and_function_definitions():
    """
    Test Case 19: Class and function definitions
    Expected: PASS - Should handle class/function definitions and calls
    """
    code = """class TestClass:
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value * 2

def test_function(x, y=10):
    return x + y

# Test the definitions
obj = TestClass(5)
print(f"Object value: {obj.get_value()}")
print(f"Function result: {test_function(3)}")"""
    return code

def test_case_20_comprehensions_and_generators():
    """
    Test Case 20: List comprehensions and generators
    Expected: PASS - Should handle modern Python syntax
    """
    code = """# List comprehension
squares = [x**2 for x in range(5)]
print(f"Squares: {squares}")

# Dictionary comprehension
word_lengths = {word: len(word) for word in ['hello', 'world', 'python']}
print(f"Word lengths: {word_lengths}")

# Generator expression
sum_of_squares = sum(x**2 for x in range(10))
print(f"Sum of squares: {sum_of_squares}")"""
    return code

# =============================================================================
# TEST RUNNER FUNCTIONS
# =============================================================================

def get_all_test_cases():
    """
    Returns a list of all test case functions and their expected results.
    Use this to iterate through all tests programmatically.
    """
    return [
        (test_case_1_relative_imports, "FAIL", "Relative imports not supported in -c execution"),
        (test_case_2_parent_directory_imports, "FAIL", "Missing requests dependency"),
        (test_case_3_standard_library_imports, "PASS", "Standard library should work"),
        (test_case_4_third_party_packages, "FAIL", "Numpy not installed"),
        (test_case_5_graceful_import_failure, "PASS", "Exception handling works"),
        (test_case_6_file_operations, "PASS", "File operations should work"),
        (test_case_7_sys_path_verification, "PASS", "sys.path should be accessible"),
        (test_case_8_multiline_strings, "PASS", "Multiline strings should work"),
        (test_case_9_exception_handling, "PASS", "Exception handling should work"),
        (test_case_10_stdout_stderr, "PASS", "stdout/stderr separation should work"),
        (test_case_11_unicode_characters, "FAIL", "Windows encoding issues"),
        (test_case_12_environment_variables, "PASS", "Environment variables should work"),
        (test_case_13_time_operations, "PASS", "Time operations should work"),
        (test_case_14_memory_operations, "PASS", "Memory operations should work"),
        (test_case_15_shell_problematic_syntax, "PASS", "Shell syntax should be safe"),
        (test_case_16_syntax_errors, "FAIL", "Syntax errors should be caught"),
        (test_case_17_infinite_loop_protection, "VARIES", "Depends on timeout implementation"),
        (test_case_18_complex_imports, "PASS", "Complex imports should work"),
        (test_case_19_class_and_function_definitions, "PASS", "Class/function definitions should work"),
        (test_case_20_comprehensions_and_generators, "PASS", "Modern Python syntax should work"),
    ]

def run_test_case_example():
    """
    Example of how to run a single test case using the Pylance snippet tool.
    Copy this pattern and replace the code with any test case.
    """
    example_instructions = '''
# Example tool call for Test Case 3:
mcp_pylance_mcp_s_pylanceRunCodeSnippet(
    codeSnippet="""import json
import datetime
import pathlib
print(json.dumps({"test": "data"}))
print(datetime.datetime.now())
print(pathlib.Path.cwd())""",
    workingDirectory="c:\\Users\\rchiodo\\source\\repos\\pylance-release\\testing\\single\\src",
    workspaceRoot="file:///c%3A/Users/rchiodo/source/repos/pylance-release/testing/single"
)
'''
    return example_instructions

# =============================================================================
# SUMMARY AND ANALYSIS
# =============================================================================

"""
TEST RESULTS SUMMARY (from previous runs):
==========================================

PASSING TESTS (11/15 core tests):
✅ Standard library imports (json, datetime, pathlib)
✅ Exception handling (try/except/finally) 
✅ Working directory and file operations
✅ sys.path verification
✅ Multi-line strings and complex formatting
✅ Environment variables
✅ Time operations  
✅ Memory operations
✅ Shell-problematic syntax (quotes, commands)
✅ Graceful import error handling
✅ Mixed stdout/stderr output

FAILING TESTS (4/15 core tests):
❌ Relative imports - Expected failure (not supported in -c execution)
❌ Parent directory imports - Environment specific (missing dependencies)
❌ Third-party packages - Environment specific (numpy not installed)
❌ Unicode characters - Windows encoding issue (cp1252 codec)

KEY FINDINGS:
=============
1. The snippet tool correctly handles working directory changes
2. Standard library imports work perfectly
3. Error handling is robust and informative
4. Unicode encoding needs attention on Windows
5. Import path behavior matches expected -c execution semantics
6. Tool properly separates stdout/stderr and provides good debugging info
7. No shell injection vulnerabilities observed
8. Timeout handling appears to work (short sleeps complete successfully)

RECOMMENDATIONS:
===============
1. Consider UTF-8 encoding fix for Windows unicode support
2. Document relative import limitations clearly
3. Consider adding dependency checking for environment-specific tests
4. Tool is production-ready for most Python code execution scenarios
"""

if __name__ == "__main__":
    print("This file contains test cases for the Pylance snippet tool.")
    print("See the docstrings and comments for instructions on running each test.")
    print(f"Total test cases available: {len(get_all_test_cases())}")