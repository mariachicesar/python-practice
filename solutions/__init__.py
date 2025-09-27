"""
Solutions module for Bloomberg Python Interview Practice Problems.

This module provides access to solution implementations for:
- Warmup problems (01_warmup.py)
- Algorithm problems (02_algorithms.py)  
- Financial application problems (03_financial_app.py)
"""

import importlib.util
import sys
from pathlib import Path

# Get the directory where this __init__.py file is located
solutions_dir = Path(__file__).parent

# Import 01_warmup.py as warmup module
spec = importlib.util.spec_from_file_location("warmup", solutions_dir / "01_warmup.py")
warmup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(warmup)
sys.modules["solutions.warmup"] = warmup

# Import 02_algorithms.py as algorithms module  
spec = importlib.util.spec_from_file_location("algorithms", solutions_dir / "02_algorithms.py")
algorithms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(algorithms)
sys.modules["solutions.algorithms"] = algorithms

# Import 03_financial_app.py as financial_app module
spec = importlib.util.spec_from_file_location("financial_app", solutions_dir / "03_financial_app.py") 
financial_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(financial_app)
sys.modules["solutions.financial_app"] = financial_app

__all__ = ['warmup', 'algorithms', 'financial_app']