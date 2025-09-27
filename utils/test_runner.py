#!/usr/bin/env python3
"""
Test Runner Utility for Bloomberg Python Interview

This script provides a convenient way to run tests for individual problems
or all problems at once, with detailed reporting.
"""

import subprocess
import sys
import time
from pathlib import Path
import argparse


def run_tests(test_file=None, verbose=False, coverage=False):
    """
    Run pytest for specified test file or all tests.
    
    Args:
        test_file (str): Specific test file to run, or None for all
        verbose (bool): Enable verbose output
        coverage (bool): Enable coverage reporting
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    cmd = ["python", "-m", "pytest"]
    
    if test_file:
        cmd.append(f"tests/{test_file}")
    else:
        cmd.append("tests/")
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=solutions", "--cov-report=term-missing"])
    
    # Add colored output
    cmd.append("--color=yes")
    
    print(f"Running command: {' '.join(cmd)}")
    print("=" * 60)
    
    start_time = time.time()
    result = subprocess.run(cmd)
    end_time = time.time()
    
    print("=" * 60)
    print(f"Tests completed in {end_time - start_time:.2f} seconds")
    
    return result.returncode


def run_problem_tests():
    """Run tests for each problem individually with summary."""
    problems = [
        ("test_warmup.py", "Problem 1: Stock Ticker Parser"),
        ("test_algorithms.py", "Problem 2: Market Data Processor"),
        ("test_financial_app.py", "Problem 3: Portfolio Risk Calculator")
    ]
    
    results = {}
    
    print("🧪 Bloomberg Python Interview - Test Suite")
    print("=" * 60)
    
    for test_file, description in problems:
        print(f"\n📋 Running {description}")
        print("-" * 40)
        
        start_time = time.time()
        exit_code = run_tests(test_file, verbose=True)
        end_time = time.time()
        
        results[description] = {
            'exit_code': exit_code,
            'duration': end_time - start_time,
            'status': '✅ PASS' if exit_code == 0 else '❌ FAIL'
        }
    
    # Print summary
    print("\n📊 Test Results Summary")
    print("=" * 60)
    
    total_time = 0
    passed = 0
    
    for problem, result in results.items():
        status = result['status']
        duration = result['duration']
        total_time += duration
        
        if result['exit_code'] == 0:
            passed += 1
            
        print(f"{status} {problem:<40} ({duration:.2f}s)")
    
    print("-" * 60)
    print(f"Overall: {passed}/{len(problems)} problems passed ({total_time:.2f}s total)")
    
    if passed == len(problems):
        print("🎉 All tests passed! Ready for the interview!")
    else:
        print("⚠️  Some tests failed. Please review and fix issues.")
    
    return passed == len(problems)


def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'pytest',
        'numpy',
        'scipy',
        'sortedcontainers',
        'matplotlib',
        'pandas'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies are installed!")
        return True


def setup_environment():
    """Set up the testing environment."""
    print("🔧 Setting up test environment...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check if solutions directory exists
    solutions_dir = Path("solutions")
    if not solutions_dir.exists():
        print("❌ Solutions directory not found")
        return False
    else:
        print("✅ Solutions directory found")
    
    return True


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(
        description="Bloomberg Python Interview Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python utils/test_runner.py                    # Run all tests
  python utils/test_runner.py --problem warmup   # Run warmup tests only
  python utils/test_runner.py --coverage         # Run with coverage
  python utils/test_runner.py --setup           # Check environment setup
        """
    )
    
    parser.add_argument(
        "--problem", 
        choices=["warmup", "algorithms", "financial"],
        help="Run tests for a specific problem"
    )
    
    parser.add_argument(
        "--coverage", 
        action="store_true",
        help="Enable coverage reporting"
    )
    
    parser.add_argument(
        "--setup", 
        action="store_true",
        help="Check environment setup"
    )
    
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Change to project root directory
    project_root = Path(__file__).parent.parent
    import os
    os.chdir(project_root)
    
    if args.setup:
        if setup_environment():
            print("🚀 Environment is ready for testing!")
            return 0
        else:
            print("❌ Environment setup failed")
            return 1
    
    if not setup_environment():
        return 1
    
    if args.problem:
        test_file_map = {
            "warmup": "test_warmup.py",
            "algorithms": "test_algorithms.py", 
            "financial": "test_financial_app.py"
        }
        test_file = test_file_map[args.problem]
        return run_tests(test_file, verbose=True, coverage=args.coverage)
    else:
        if run_problem_tests():
            return 0
        else:
            return 1


if __name__ == "__main__":
    sys.exit(main())