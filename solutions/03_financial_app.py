# Solution: Portfolio Risk Calculator  
# Bloomberg Python Technical Interview - Problem 3

import math
import numpy as np
from scipy import stats
from scipy.optimize import minimize
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


class PortfolioRiskCalculator:
    def __init__(self):
        """
        Initialize portfolio risk calculator.
        
        Data structures:
        - positions: {symbol: {'quantity': int, 'price': float}}
        - volatilities: {symbol: float}  # Daily volatility (std dev)
        - correlations: {(symbol1, symbol2): float}
        """
        self.positions = {}
        self.volatilities = {}
        self.correlations = defaultdict(lambda: 0.0)  # Default correlation = 0.0
        
    def add_position(self, symbol: str, quantity: int, current_price: float) -> None:
        """Add or update a position in the portfolio."""
        if current_price < 0:
            raise ValueError("Price cannot be negative")
            
        if quantity == 0:
            # Remove position if quantity is 0
            self.positions.pop(symbol, None)
        else:
            self.positions[symbol] = {
                'quantity': quantity,
                'price': current_price
            }
    
    def set_asset_volatility(self, symbol: str, volatility: float) -> None:
        """Set the volatility for an asset (daily standard deviation)."""
        if volatility < 0:
            raise ValueError("Volatility cannot be negative")
        self.volatilities[symbol] = volatility
    
    def set_correlation(self, symbol1: str, symbol2: str, correlation: float) -> None:
        """Set correlation coefficient between two assets."""
        if not (-1 <= correlation <= 1):
            raise ValueError("Correlation must be between -1 and 1")
        
        # Store both directions
        self.correlations[(symbol1, symbol2)] = correlation
        self.correlations[(symbol2, symbol1)] = correlation
        
        # Self-correlation is always 1
        self.correlations[(symbol1, symbol1)] = 1.0
        self.correlations[(symbol2, symbol2)] = 1.0
    
    def calculate_portfolio_value(self) -> float:
        """Calculate total portfolio value."""
        total_value = 0
        for symbol, position in self.positions.items():
            value = position['quantity'] * position['price']
            total_value += value
        return total_value
    
    def get_position_weights(self) -> Dict[str, float]:
        """Calculate weight of each position in portfolio."""
        total_value = self.calculate_portfolio_value()
        if total_value == 0:
            return {}
        
        weights = {}
        for symbol, position in self.positions.items():
            position_value = position['quantity'] * position['price']
            weights[symbol] = position_value / total_value
            
        return weights
    
    def calculate_portfolio_volatility(self) -> float:
        """
        Calculate portfolio volatility using correlation matrix.
        
        Formula: σ_p = sqrt(Σ Σ w_i * w_j * σ_i * σ_j * ρ_ij)
        where w_i = weight of asset i, σ_i = volatility of asset i, ρ_ij = correlation
        """
        weights = self.get_position_weights()
        symbols = list(weights.keys())
        
        if len(symbols) == 0:
            return 0.0
        
        # Check if all assets have volatility data
        missing_volatilities = [s for s in symbols if s not in self.volatilities]
        if missing_volatilities:
            raise ValueError(f"Missing volatility data for: {missing_volatilities}")
        
        # Calculate portfolio variance
        portfolio_variance = 0.0
        
        for i, symbol_i in enumerate(symbols):
            for j, symbol_j in enumerate(symbols):
                weight_i = weights[symbol_i]
                weight_j = weights[symbol_j]
                vol_i = self.volatilities[symbol_i]
                vol_j = self.volatilities[symbol_j]
                
                # Get correlation
                if symbol_i == symbol_j:
                    correlation = 1.0
                else:
                    correlation = self.correlations.get((symbol_i, symbol_j), 0.0)
                
                portfolio_variance += weight_i * weight_j * vol_i * vol_j * correlation
        
        return math.sqrt(portfolio_variance)
    
    def calculate_var(self, confidence_level: float = 0.95, time_horizon: int = 1) -> float:
        """
        Calculate Value at Risk using parametric method.
        
        VaR = Portfolio_Value * Z_score * Volatility * sqrt(time_horizon)
        where Z_score is the inverse normal CDF at confidence level
        """
        if not (0 < confidence_level < 1):
            raise ValueError("Confidence level must be between 0 and 1")
        
        portfolio_value = self.calculate_portfolio_value()
        if portfolio_value <= 0:
            return 0.0
        
        portfolio_volatility = self.calculate_portfolio_volatility()
        
        # Get Z-score for confidence level (e.g., 95% = 1.645)
        z_score = stats.norm.ppf(confidence_level)
        
        # Scale by time horizon (assuming daily volatility)
        time_adjusted_vol = portfolio_volatility * math.sqrt(time_horizon)
        
        # VaR is the expected loss (positive number)
        var = portfolio_value * z_score * time_adjusted_vol
        
        return var
    
    def stress_test(self, scenario: Dict[str, float]) -> float:
        """
        Apply stress scenario and return new portfolio value.
        
        Args:
            scenario: {symbol: price_change_percent}
        
        Returns:
            New portfolio value after applying stress scenario
        """
        new_value = 0
        
        for symbol, position in self.positions.items():
            current_price = position['price']
            quantity = position['quantity']
            
            # Apply stress scenario
            if symbol in scenario:
                price_change = scenario[symbol]  # e.g., -0.20 for -20%
                new_price = current_price * (1 + price_change)
                new_price = max(0.01, new_price)  # Ensure positive price
            else:
                new_price = current_price
            
            new_value += quantity * new_price
        
        return new_value
    
    def optimize_weights(self, target_return: float) -> Optional[Dict[str, float]]:
        """
        Find optimal weights to minimize risk for target return.
        This is a simplified version of mean-variance optimization.
        """
        symbols = list(self.positions.keys())
        if len(symbols) <= 1:
            return {symbol: 1.0 for symbol in symbols}
        
        n_assets = len(symbols)
        
        # Build covariance matrix
        cov_matrix = np.zeros((n_assets, n_assets))
        for i, symbol_i in enumerate(symbols):
            for j, symbol_j in enumerate(symbols):
                vol_i = self.volatilities.get(symbol_i, 0.1)  # Default 10% volatility
                vol_j = self.volatilities.get(symbol_j, 0.1)
                
                if symbol_i == symbol_j:
                    correlation = 1.0
                else:
                    correlation = self.correlations.get((symbol_i, symbol_j), 0.0)
                
                cov_matrix[i][j] = vol_i * vol_j * correlation
        
        # Objective function: minimize portfolio variance
        def objective(weights):
            return np.dot(weights, np.dot(cov_matrix, weights))
        
        # Constraints: weights sum to 1
        constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0}
        
        # Bounds: weights between 0 and 1 (long-only portfolio)
        bounds = tuple((0, 1) for _ in range(n_assets))
        
        # Initial guess: equal weights
        initial_weights = np.array([1.0 / n_assets] * n_assets)
        
        # Optimization
        try:
            result = minimize(objective, initial_weights, method='SLSQP',
                            bounds=bounds, constraints=constraints)
            
            if result.success:
                optimal_weights = {symbols[i]: float(result.x[i]) 
                                 for i in range(n_assets)}
                return optimal_weights
            else:
                return None
        except:
            return None


# Advanced Portfolio Analytics
class AdvancedPortfolioAnalytics(PortfolioRiskCalculator):
    """Extended version with additional risk metrics."""
    
    def calculate_sharpe_ratio(self, portfolio_return: float, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio (return per unit of risk)."""
        portfolio_vol = self.calculate_portfolio_volatility() * math.sqrt(252)  # Annualized
        
        if portfolio_vol == 0:
            return 0
        
        return (portfolio_return - risk_free_rate) / portfolio_vol
    
    def calculate_beta(self, market_volatility: float = 0.15, 
                      market_correlation: float = 0.8) -> float:
        """Calculate portfolio beta relative to market."""
        portfolio_vol = self.calculate_portfolio_volatility() * math.sqrt(252)  # Annualized
        
        # Simplified beta calculation
        beta = (portfolio_vol * market_correlation) / market_volatility
        return beta
    
    def monte_carlo_var(self, confidence_level: float = 0.95, 
                       num_simulations: int = 10000, time_horizon: int = 1) -> float:
        """Calculate VaR using Monte Carlo simulation."""
        portfolio_value = self.calculate_portfolio_value()
        portfolio_vol = self.calculate_portfolio_volatility()
        
        if portfolio_value <= 0:
            return 0.0
        
        # Generate random returns
        np.random.seed(42)  # For reproducibility
        random_returns = np.random.normal(0, portfolio_vol, num_simulations)
        
        # Scale for time horizon
        random_returns = random_returns * math.sqrt(time_horizon)
        
        # Calculate portfolio values
        portfolio_values = portfolio_value * (1 + random_returns)
        
        # Calculate losses (negative returns)
        losses = portfolio_value - portfolio_values
        
        # Find VaR at confidence level
        var = np.percentile(losses, confidence_level * 100)
        
        return max(0, var)
    
    def expected_shortfall(self, confidence_level: float = 0.95, 
                          num_simulations: int = 10000) -> float:
        """Calculate Expected Shortfall (Conditional VaR)."""
        portfolio_value = self.calculate_portfolio_value()
        portfolio_vol = self.calculate_portfolio_volatility()
        
        if portfolio_value <= 0:
            return 0.0
        
        # Generate random returns
        np.random.seed(42)
        random_returns = np.random.normal(0, portfolio_vol, num_simulations)
        
        # Calculate portfolio values
        portfolio_values = portfolio_value * (1 + random_returns)
        losses = portfolio_value - portfolio_values
        
        # Find VaR threshold
        var_threshold = np.percentile(losses, confidence_level * 100)
        
        # Calculate average loss beyond VaR
        extreme_losses = losses[losses >= var_threshold]
        
        if len(extreme_losses) > 0:
            return np.mean(extreme_losses)
        else:
            return var_threshold
    
    def component_var(self, confidence_level: float = 0.95) -> Dict[str, float]:
        """Calculate component VaR for each position."""
        portfolio_var = self.calculate_var(confidence_level)
        portfolio_vol = self.calculate_portfolio_volatility()
        
        if portfolio_vol == 0:
            return {symbol: 0.0 for symbol in self.positions.keys()}
        
        weights = self.get_position_weights()
        component_vars = {}
        
        for symbol in self.positions.keys():
            # Calculate marginal contribution to risk
            marginal_vol = self._calculate_marginal_volatility(symbol)
            
            # Component VaR = weight * marginal contribution * total VaR / total vol
            weight = weights[symbol]
            component_var = weight * marginal_vol * portfolio_var / portfolio_vol
            component_vars[symbol] = component_var
        
        return component_vars
    
    def _calculate_marginal_volatility(self, target_symbol: str) -> float:
        """Calculate marginal contribution of an asset to portfolio volatility."""
        weights = self.get_position_weights()
        
        marginal_vol = 0.0
        target_vol = self.volatilities.get(target_symbol, 0.0)
        
        for symbol, weight in weights.items():
            asset_vol = self.volatilities.get(symbol, 0.0)
            
            if target_symbol == symbol:
                correlation = 1.0
            else:
                correlation = self.correlations.get((target_symbol, symbol), 0.0)
            
            marginal_vol += weight * asset_vol * correlation
        
        return target_vol * marginal_vol


# Risk reporting and utilities
class RiskReporter:
    """Generate risk reports and analytics."""
    
    def __init__(self, calculator: PortfolioRiskCalculator):
        self.calculator = calculator
    
    def generate_risk_report(self) -> Dict:
        """Generate comprehensive risk report."""
        report = {
            'portfolio_summary': {
                'total_value': self.calculator.calculate_portfolio_value(),
                'num_positions': len(self.calculator.positions),
                'positions': dict(self.calculator.positions),
                'weights': self.calculator.get_position_weights()
            },
            'risk_metrics': {
                'portfolio_volatility': self.calculator.calculate_portfolio_volatility(),
                'var_95': self.calculator.calculate_var(0.95),
                'var_99': self.calculator.calculate_var(0.99),
            },
            'stress_scenarios': {},
            'diversification_metrics': self._calculate_diversification_metrics()
        }
        
        # Add stress test scenarios
        stress_scenarios = {
            'market_crash': {symbol: -0.20 for symbol in self.calculator.positions.keys()},
            'sector_rotation': {symbol: -0.10 if 'TECH' in symbol.upper() else 0.05 
                              for symbol in self.calculator.positions.keys()},
            'volatility_spike': {symbol: -0.15 for symbol in self.calculator.positions.keys()}
        }
        
        for scenario_name, scenario in stress_scenarios.items():
            stressed_value = self.calculator.stress_test(scenario)
            current_value = report['portfolio_summary']['total_value']
            loss = current_value - stressed_value if current_value > 0 else 0
            loss_pct = loss / current_value if current_value > 0 else 0
            
            report['stress_scenarios'][scenario_name] = {
                'stressed_value': stressed_value,
                'absolute_loss': loss,
                'percentage_loss': loss_pct
            }
        
        return report
    
    def _calculate_diversification_metrics(self) -> Dict:
        """Calculate portfolio diversification metrics."""
        weights = self.calculator.get_position_weights()
        
        if not weights:
            return {'concentration': 0, 'effective_positions': 0}
        
        # Calculate concentration (Herfindahl index)
        concentration = sum(w**2 for w in weights.values())
        
        # Calculate effective number of positions
        effective_positions = 1 / concentration if concentration > 0 else 0
        
        return {
            'concentration': concentration,
            'effective_positions': effective_positions,
            'max_weight': max(weights.values()) if weights else 0,
            'min_weight': min(weights.values()) if weights else 0
        }


# Test and validation functions
def create_sample_portfolio():
    """Create a sample portfolio for testing."""
    calc = PortfolioRiskCalculator()
    
    # Add positions
    calc.add_position("AAPL", 100, 150.0)
    calc.add_position("GOOGL", 50, 2800.0)
    calc.add_position("MSFT", 75, 300.0)
    calc.add_position("TSLA", 25, 800.0)
    
    # Set volatilities (daily)
    calc.set_asset_volatility("AAPL", 0.025)   # 2.5% daily vol
    calc.set_asset_volatility("GOOGL", 0.030)  # 3.0% daily vol
    calc.set_asset_volatility("MSFT", 0.022)   # 2.2% daily vol
    calc.set_asset_volatility("TSLA", 0.045)   # 4.5% daily vol
    
    # Set correlations
    correlations = [
        ("AAPL", "GOOGL", 0.7),
        ("AAPL", "MSFT", 0.8),
        ("AAPL", "TSLA", 0.6),
        ("GOOGL", "MSFT", 0.6),
        ("GOOGL", "TSLA", 0.5),
        ("MSFT", "TSLA", 0.4)
    ]
    
    for symbol1, symbol2, corr in correlations:
        calc.set_correlation(symbol1, symbol2, corr)
    
    return calc


def test_portfolio_risk_calculator():
    """Comprehensive test suite for the portfolio risk calculator."""
    print("🧪 Testing Portfolio Risk Calculator")
    print("=" * 50)
    
    # Test 1: Basic functionality
    print("Test 1: Basic portfolio operations")
    calc = PortfolioRiskCalculator()
    
    calc.add_position("AAPL", 100, 150.0)
    calc.add_position("GOOGL", 50, 2800.0)
    
    assert calc.calculate_portfolio_value() == 155000.0  # 100*150 + 50*2800
    
    weights = calc.get_position_weights()
    assert abs(weights["AAPL"] - 0.0968) < 0.001  # 15000/155000
    assert abs(weights["GOOGL"] - 0.9032) < 0.001  # 140000/155000
    
    print("✅ Basic operations passed")
    
    # Test 2: Risk calculations
    print("Test 2: Risk calculations")
    calc.set_asset_volatility("AAPL", 0.02)
    calc.set_asset_volatility("GOOGL", 0.03)
    calc.set_correlation("AAPL", "GOOGL", 0.5)
    
    portfolio_vol = calc.calculate_portfolio_volatility()
    assert portfolio_vol > 0
    
    var_95 = calc.calculate_var(0.95)
    assert var_95 > 0
    
    print(f"✅ Portfolio volatility: {portfolio_vol:.4f}")
    print(f"✅ 95% VaR: ${var_95:,.2f}")
    
    # Test 3: Stress testing
    print("Test 3: Stress testing")
    stress_scenario = {"AAPL": -0.20, "GOOGL": -0.15}
    stressed_value = calc.stress_test(stress_scenario)
    original_value = calc.calculate_portfolio_value()
    
    assert stressed_value < original_value
    loss = original_value - stressed_value
    loss_pct = loss / original_value
    
    print(f"✅ Stress test loss: ${loss:,.2f} ({loss_pct:.1%})")
    
    # Test 4: Error handling
    print("Test 4: Error handling")
    
    try:
        calc.set_asset_volatility("AAPL", -0.01)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    try:
        calc.set_correlation("AAPL", "GOOGL", 1.5)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    print("✅ Error handling passed")
    
    # Test 5: Advanced analytics
    print("Test 5: Advanced analytics")
    advanced = AdvancedPortfolioAnalytics()
    advanced.add_position("AAPL", 100, 150.0)
    advanced.add_position("GOOGL", 50, 2800.0)
    advanced.set_asset_volatility("AAPL", 0.02)
    advanced.set_asset_volatility("GOOGL", 0.03)
    advanced.set_correlation("AAPL", "GOOGL", 0.5)
    
    mc_var = advanced.monte_carlo_var(0.95, 1000)
    parametric_var = advanced.calculate_var(0.95)
    
    # Monte Carlo VaR should be similar to parametric VaR
    assert abs(mc_var - parametric_var) / parametric_var < 0.2  # Within 20%
    
    print(f"✅ Monte Carlo VaR: ${mc_var:,.2f}")
    
    print("\n🎉 All tests passed!")


def demo_risk_analysis():
    """Demonstrate comprehensive risk analysis."""
    print("📈 Portfolio Risk Analysis Demo")
    print("=" * 40)
    
    # Create sample portfolio
    calc = create_sample_portfolio()
    
    # Generate risk report
    reporter = RiskReporter(calc)
    report = reporter.generate_risk_report()
    
    # Display results
    print(f"Portfolio Value: ${report['portfolio_summary']['total_value']:,.2f}")
    print(f"Number of Positions: {report['portfolio_summary']['num_positions']}")
    print(f"Portfolio Volatility: {report['risk_metrics']['portfolio_volatility']:.4f}")
    print(f"95% VaR: ${report['risk_metrics']['var_95']:,.2f}")
    print(f"99% VaR: ${report['risk_metrics']['var_99']:,.2f}")
    
    print("\nPosition Weights:")
    for symbol, weight in report['portfolio_summary']['weights'].items():
        print(f"  {symbol}: {weight:.1%}")
    
    print("\nStress Test Results:")
    for scenario, results in report['stress_scenarios'].items():
        loss_pct = results['percentage_loss']
        print(f"  {scenario.replace('_', ' ').title()}: {loss_pct:.1%} loss")
    
    print(f"\nDiversification Metrics:")
    div_metrics = report['diversification_metrics']
    print(f"  Effective Positions: {div_metrics['effective_positions']:.1f}")
    print(f"  Concentration Index: {div_metrics['concentration']:.3f}")


if __name__ == "__main__":
    # Run tests
    test_portfolio_risk_calculator()
    
    print("\n" + "="*60 + "\n")
    
    # Run demo
    demo_risk_analysis()