"""
Bloomberg Python Interview - Starter Code Template

This file contains starter templates for all interview problems.
Candidates should implement their solutions here.

Instructions:
1. Read the problem description in the problems/ directory
2. Implement your solution in the corresponding section below
3. Test your solution using the provided test cases
4. Run tests with: python -m pytest tests/test_[problem].py -v

Time allocation:
- Problem 1 (Warmup): 10 minutes
- Problem 2 (Algorithms): 25 minutes  
- Problem 3 (Financial): 30 minutes
"""

# ==============================================================================
# PROBLEM 1: STRING MANIPULATION - STOCK TICKER PARSER (10 minutes)
# ==============================================================================

def parse_stock_data(data_string):
    """
    Parse stock ticker and price changes.
    
    Args:
        data_string (str): Format "TICKER:change1,change2,..."
    
    Returns:
        dict: Contains ticker, changes, and net_change
    
    Example:
        parse_stock_data("AAPL:+2.5,-1.2,+0.8") 
        # Returns: {'ticker': 'AAPL', 'changes': [2.5, -1.2, 0.8], 'net_change': 2.1}
    
    Raises:
        ValueError: For invalid input format
    """
    # TODO: Implement your solution here
    pass


# Test your solution
def test_problem1():
    # Basic test case
    result = parse_stock_data("AAPL:+2.5,-1.2,+0.8,-0.3,+1.1")
    print(f"Result: {result}")
    # Expected: {'ticker': 'AAPL', 'changes': [2.5, -1.2, 0.8, -0.3, 1.1], 'net_change': 2.9}


# ==============================================================================
# PROBLEM 2: ALGORITHMS - MARKET DATA PROCESSOR (25 minutes)
# ==============================================================================

class MarketDataProcessor:
    def __init__(self):
        """Initialize your data structure for efficient time-based queries."""
        # TODO: Choose and initialize appropriate data structure
        pass
    
    def add_price(self, timestamp: int, price: float) -> None:
        """Add a new price point with timestamp (milliseconds since epoch)."""
        # TODO: Implement efficient insertion
        pass
    
    def get_current_price(self) -> float:
        """Get the most recent price."""
        # TODO: Return most recent price or None if no data
        pass
    
    def get_price_at_time(self, timestamp: int) -> float:
        """Get price at specific time (or most recent before that time)."""
        # TODO: Implement time-based lookup
        pass
    
    def get_average_price(self, start_time: int, end_time: int) -> float:
        """Get average price in time window [start_time, end_time]."""
        # TODO: Calculate average for time range
        pass
    
    def get_price_range(self, start_time: int, end_time: int) -> tuple:
        """Get (min_price, max_price) in time window [start_time, end_time]."""
        # TODO: Find min/max in time range
        pass


# Test your solution
def test_problem2():
    processor = MarketDataProcessor()
    
    # Add test data
    processor.add_price(1000, 100.0)
    processor.add_price(1001, 101.0)
    processor.add_price(1002, 99.0)
    processor.add_price(1003, 102.0)
    
    # Test queries
    print(f"Current price: {processor.get_current_price()}")
    print(f"Price at 1001: {processor.get_price_at_time(1001)}")
    print(f"Average (1000-1002): {processor.get_average_price(1000, 1002)}")
    print(f"Range (1000-1002): {processor.get_price_range(1000, 1002)}")


# ==============================================================================
# PROBLEM 3: FINANCIAL APPLICATION - PORTFOLIO RISK CALCULATOR (30 minutes)
# ==============================================================================

class PortfolioRiskCalculator:
    def __init__(self):
        """Initialize the portfolio risk calculator."""
        # TODO: Initialize data structures for positions, volatilities, and correlations
        pass
    
    def add_position(self, symbol: str, quantity: int, current_price: float) -> None:
        """Add or update a position in the portfolio."""
        # TODO: Store position (symbol, quantity, price)
        # If quantity is 0, remove the position
        pass
    
    def set_asset_volatility(self, symbol: str, volatility: float) -> None:
        """Set the daily volatility (standard deviation) for an asset."""
        # TODO: Validate volatility >= 0 and store
        pass
    
    def set_correlation(self, symbol1: str, symbol2: str, correlation: float) -> None:
        """Set correlation coefficient between two assets (-1 to +1)."""
        # TODO: Validate -1 <= correlation <= 1 and store both directions
        pass
    
    def calculate_portfolio_value(self) -> float:
        """Calculate total portfolio value."""
        # TODO: Sum all position values (quantity × price)
        pass
    
    def get_position_weights(self) -> dict:
        """Calculate weight of each position in portfolio."""
        # TODO: Calculate position_value / total_portfolio_value for each position
        pass
    
    def calculate_portfolio_volatility(self) -> float:
        """Calculate portfolio volatility using correlation matrix."""
        # TODO: Implement portfolio volatility formula
        # σ_p = sqrt(Σ Σ w_i * w_j * σ_i * σ_j * ρ_ij)
        pass
    
    def calculate_var(self, confidence_level: float = 0.95) -> float:
        """Calculate Value at Risk using parametric method."""
        # TODO: VaR = Portfolio_Value × Z_score × Portfolio_Volatility
        # Use scipy.stats.norm.ppf() for Z_score if available
        pass
    
    def stress_test(self, scenario: dict) -> float:
        """Apply stress scenario and return new portfolio value."""
        # TODO: Apply percentage changes to prices and recalculate value
        # scenario format: {"SYMBOL": price_change_percent}
        # e.g., {"AAPL": -0.20} means 20% price drop
        pass


# Test your solution
def test_problem3():
    calc = PortfolioRiskCalculator()
    
    # Build portfolio
    calc.add_position("AAPL", 100, 150.0)
    calc.add_position("GOOGL", 50, 2800.0)
    
    # Set risk parameters
    calc.set_asset_volatility("AAPL", 0.025)   # 2.5% daily volatility
    calc.set_asset_volatility("GOOGL", 0.030)  # 3.0% daily volatility
    calc.set_correlation("AAPL", "GOOGL", 0.7) # 70% correlation
    
    # Test calculations
    print(f"Portfolio Value: ${calc.calculate_portfolio_value():,.2f}")
    print(f"Portfolio Volatility: {calc.calculate_portfolio_volatility():.4f}")
    print(f"95% VaR: ${calc.calculate_var(0.95):,.2f}")
    
    # Stress test
    scenario = {"AAPL": -0.10, "GOOGL": -0.15}  # 10% and 15% drops
    print(f"Stressed Value: ${calc.stress_test(scenario):,.2f}")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    print("Bloomberg Python Interview - Starter Code")
    print("=" * 50)
    
    print("\n1. Testing Problem 1 - Stock Ticker Parser")
    print("-" * 40)
    try:
        test_problem1()
    except Exception as e:
        print(f"Error in Problem 1: {e}")
    
    print("\n2. Testing Problem 2 - Market Data Processor")  
    print("-" * 40)
    try:
        test_problem2()
    except Exception as e:
        print(f"Error in Problem 2: {e}")
    
    print("\n3. Testing Problem 3 - Portfolio Risk Calculator")
    print("-" * 40)
    try:
        test_problem3()
    except Exception as e:
        print(f"Error in Problem 3: {e}")
    
    print("\n" + "=" * 50)
    print("Instructions:")
    print("1. Implement the functions marked with 'TODO'")
    print("2. Run tests with: python -m pytest tests/ -v")
    print("3. Use 'python problems/starter_code.py' to test your progress")
    print("4. Good luck with your Bloomberg interview! 🚀")