# Problem 3: Financial Application - Portfolio Risk Calculator
**Difficulty**: Medium-Hard  
**Time**: 30 minutes  
**Focus**: Financial mathematics, complex algorithms, domain knowledge

## Problem Statement
You're building a portfolio risk management system for Bloomberg Terminal. The system needs to calculate various risk metrics for investment portfolios, helping traders and portfolio managers make informed decisions.

### Financial Background
- **Portfolio**: A collection of financial positions (stocks, quantities)
- **Value at Risk (VaR)**: Maximum expected loss over a time period at a confidence level
- **Volatility**: Measure of price fluctuation (standard deviation of returns)
- **Correlation**: How different assets move relative to each other (-1 to +1)
- **Diversification**: Reducing risk by combining uncorrelated assets

### Bloomberg Context
Portfolio managers at Bloomberg clients need real-time risk calculations to:
- Monitor portfolio exposure
- Comply with risk limits
- Optimize asset allocation
- Perform stress testing
- Make trading decisions

### Requirements
Implement a `PortfolioRiskCalculator` class with this interface:

```python
class PortfolioRiskCalculator:
    def add_position(self, symbol: str, quantity: int, current_price: float) -> None:
        """Add or update a position in the portfolio"""
        pass
    
    def set_asset_volatility(self, symbol: str, volatility: float) -> None:
        """Set the daily volatility (standard deviation) for an asset"""
        pass
    
    def set_correlation(self, symbol1: str, symbol2: str, correlation: float) -> None:
        """Set correlation coefficient between two assets (-1 to +1)"""
        pass
    
    def calculate_portfolio_value(self) -> float:
        """Calculate total portfolio value"""
        pass
    
    def calculate_portfolio_volatility(self) -> float:
        """Calculate portfolio volatility using correlation matrix"""
        pass
    
    def calculate_var(self, confidence_level: float = 0.95) -> float:
        """Calculate Value at Risk at given confidence level"""
        pass
    
    def stress_test(self, scenario: dict) -> float:
        """Apply stress scenario and return new portfolio value"""
        pass
```

### Mathematical Formulas

#### Portfolio Value
```
Portfolio Value = Σ (quantity_i × price_i) for all positions i
```

#### Portfolio Volatility
```
σ_portfolio = √(Σ Σ w_i × w_j × σ_i × σ_j × ρ_ij)

where:
- w_i = weight of asset i in portfolio
- σ_i = volatility of asset i  
- ρ_ij = correlation between assets i and j
```

#### Value at Risk (Parametric Method)
```
VaR = Portfolio_Value × Z_score × Portfolio_Volatility

where Z_score is inverse normal CDF at confidence level
(e.g., 95% confidence = 1.645, 99% confidence = 2.326)
```

### Example Usage
```python
calc = PortfolioRiskCalculator()

# Build portfolio
calc.add_position("AAPL", 100, 150.0)   # 100 shares at $150
calc.add_position("GOOGL", 50, 2800.0)  # 50 shares at $2800
calc.add_position("MSFT", 75, 300.0)    # 75 shares at $300

# Set risk parameters
calc.set_asset_volatility("AAPL", 0.025)   # 2.5% daily volatility
calc.set_asset_volatility("GOOGL", 0.030)  # 3.0% daily volatility
calc.set_asset_volatility("MSFT", 0.022)   # 2.2% daily volatility

# Set correlations
calc.set_correlation("AAPL", "GOOGL", 0.7)   # 70% correlation
calc.set_correlation("AAPL", "MSFT", 0.8)    # 80% correlation  
calc.set_correlation("GOOGL", "MSFT", 0.6)   # 60% correlation

# Calculate risk metrics
portfolio_value = calc.calculate_portfolio_value()  # $185,500
portfolio_vol = calc.calculate_portfolio_volatility()  # ~0.024 (2.4%)
var_95 = calc.calculate_var(0.95)  # 95% VaR

# Stress test: market crash scenario
crash_scenario = {"AAPL": -0.20, "GOOGL": -0.25, "MSFT": -0.18}
stressed_value = calc.stress_test(crash_scenario)
```

### Your Implementation
```python
import math
from typing import Dict, Optional
from scipy import stats  # You may use this for normal distribution functions

class PortfolioRiskCalculator:
    def __init__(self):
        """Initialize the portfolio risk calculator"""
        # TODO: Initialize data structures
        pass
    
    def add_position(self, symbol: str, quantity: int, current_price: float) -> None:
        """Add or update a position in the portfolio"""
        # TODO: Store position (symbol, quantity, price)
        # If quantity is 0, remove the position
        pass
    
    def set_asset_volatility(self, symbol: str, volatility: float) -> None:
        """Set the daily volatility for an asset"""
        # TODO: Validate volatility >= 0 and store
        pass
    
    def set_correlation(self, symbol1: str, symbol2: str, correlation: float) -> None:
        """Set correlation coefficient between two assets"""
        # TODO: Validate -1 <= correlation <= 1 and store both directions
        pass
    
    def calculate_portfolio_value(self) -> float:
        """Calculate total portfolio value"""
        # TODO: Sum all position values (quantity × price)
        pass
    
    def get_position_weights(self) -> Dict[str, float]:
        """Calculate weight of each position in portfolio"""
        # TODO: Calculate position_value / total_portfolio_value for each position
        pass
    
    def calculate_portfolio_volatility(self) -> float:
        """Calculate portfolio volatility using correlation matrix"""
        # TODO: Implement portfolio volatility formula
        # σ_p = sqrt(Σ Σ w_i * w_j * σ_i * σ_j * ρ_ij)
        pass
    
    def calculate_var(self, confidence_level: float = 0.95) -> float:
        """Calculate Value at Risk using parametric method"""
        # TODO: VaR = Portfolio_Value × Z_score × Portfolio_Volatility
        # Use scipy.stats.norm.ppf() for Z_score
        pass
    
    def stress_test(self, scenario: Dict[str, float]) -> float:
        """Apply stress scenario and return new portfolio value"""
        # TODO: Apply percentage changes to prices and recalculate value
        # scenario format: {"SYMBOL": price_change_percent}
        # e.g., {"AAPL": -0.20} means 20% price drop
        pass

# Test your implementation
if __name__ == "__main__":
    calc = PortfolioRiskCalculator()
    
    # Add positions
    calc.add_position("AAPL", 100, 150.0)
    calc.add_position("GOOGL", 50, 2800.0)
    
    # Set volatilities
    calc.set_asset_volatility("AAPL", 0.025)
    calc.set_asset_volatility("GOOGL", 0.030)
    
    # Set correlation
    calc.set_correlation("AAPL", "GOOGL", 0.7)
    
    # Test calculations
    print(f"Portfolio Value: ${calc.calculate_portfolio_value():,.2f}")
    print(f"Portfolio Volatility: {calc.calculate_portfolio_volatility():.4f}")
    print(f"95% VaR: ${calc.calculate_var(0.95):,.2f}")
    
    # Stress test
    scenario = {"AAPL": -0.10, "GOOGL": -0.15}
    print(f"Stressed Value: ${calc.stress_test(scenario):,.2f}")
```

### Test Cases
Your implementation should handle these scenarios:

```python
# Empty portfolio
calc = PortfolioRiskCalculator()
assert calc.calculate_portfolio_value() == 0
assert calc.calculate_portfolio_volatility() == 0

# Single position
calc.add_position("AAPL", 100, 150.0)
calc.set_asset_volatility("AAPL", 0.02)
assert calc.calculate_portfolio_value() == 15000.0
assert abs(calc.calculate_portfolio_volatility() - 0.02) < 0.001

# Remove position (quantity = 0)
calc.add_position("AAPL", 0, 150.0)
assert calc.calculate_portfolio_value() == 0

# Multiple positions with correlation
calc.add_position("AAPL", 100, 100.0)  # $10,000
calc.add_position("MSFT", 100, 200.0)  # $20,000 (total: $30,000)
calc.set_asset_volatility("AAPL", 0.02)
calc.set_asset_volatility("MSFT", 0.03)
calc.set_correlation("AAPL", "MSFT", 0.5)

# Portfolio weights: AAPL=1/3, MSFT=2/3
# Portfolio volatility should be less than weighted average due to diversification

# Error handling
try:
    calc.set_asset_volatility("AAPL", -0.01)  # Should raise ValueError
    assert False, "Should have raised ValueError"
except ValueError:
    pass

try:
    calc.set_correlation("AAPL", "MSFT", 1.5)  # Should raise ValueError
    assert False, "Should have raised ValueError"  
except ValueError:
    pass
```

### Discussion Questions
Be prepared to discuss:

1. **Financial Concepts**: Explain diversification and why correlation matters
2. **Mathematical Implementation**: How did you handle the portfolio volatility calculation?
3. **Edge Cases**: What happens with zero positions, missing volatility data, or extreme correlations?
4. **Performance**: How would you optimize for portfolios with hundreds of assets?
5. **Alternative VaR Methods**: What are the limitations of parametric VaR? What other methods exist?
6. **Real-world Considerations**: How would you handle data quality issues, missing prices, or market closures?

### Extension Challenges
If you finish early, consider implementing:

1. **Monte Carlo VaR**: Simulate portfolio returns using random sampling
2. **Expected Shortfall**: Calculate expected loss beyond VaR threshold
3. **Risk Attribution**: Break down portfolio risk by asset contribution
4. **Optimization**: Find optimal weights to minimize risk for target return
5. **Historical VaR**: Calculate VaR based on historical price movements

### Hints
- Use `scipy.stats.norm.ppf()` for inverse normal distribution
- Handle correlation matrix symmetry (if A-B correlation is set, B-A should be the same)
- Consider floating-point precision for financial calculations
- Default correlations: use 1.0 for same asset, 0.0 for different assets if not specified
- Portfolio volatility will be less than the weighted average volatility when correlations < 1