import pytest
import sys
import numpy as np
from pathlib import Path
import math

# Add the solutions directory to Python path
solutions_dir = Path(__file__).parent.parent / "solutions"
sys.path.insert(0, str(solutions_dir))

from solutions.financial_app import PortfolioRiskCalculator, AdvancedPortfolioAnalytics, RiskReporter


class TestPortfolioRiskCalculator:
    """Test suite for Portfolio Risk Calculator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.calc = PortfolioRiskCalculator()
    
    def test_empty_portfolio(self):
        """Test behavior with empty portfolio."""
        assert self.calc.calculate_portfolio_value() == 0
        assert self.calc.get_position_weights() == {}
        assert self.calc.calculate_portfolio_volatility() == 0
        assert self.calc.calculate_var(0.95) == 0
    
    def test_single_position(self):
        """Test portfolio with single position."""
        self.calc.add_position("AAPL", 100, 150.0)
        
        assert self.calc.calculate_portfolio_value() == 15000.0
        
        weights = self.calc.get_position_weights()
        assert weights["AAPL"] == 1.0
        
        # Need volatility for further calculations
        self.calc.set_asset_volatility("AAPL", 0.02)
        
        assert abs(self.calc.calculate_portfolio_volatility() - 0.02) < 0.001
    
    def test_multiple_positions(self):
        """Test portfolio with multiple positions."""
        self.calc.add_position("AAPL", 100, 150.0)  # $15,000
        self.calc.add_position("GOOGL", 50, 2800.0)  # $140,000
        # Total: $155,000
        
        assert self.calc.calculate_portfolio_value() == 155000.0
        
        weights = self.calc.get_position_weights()
        assert abs(weights["AAPL"] - 15000/155000) < 0.001
        assert abs(weights["GOOGL"] - 140000/155000) < 0.001
        assert abs(sum(weights.values()) - 1.0) < 0.001
    
    def test_position_updates(self):
        """Test updating and removing positions."""
        # Add position
        self.calc.add_position("AAPL", 100, 150.0)
        assert self.calc.calculate_portfolio_value() == 15000.0
        
        # Update position
        self.calc.add_position("AAPL", 200, 160.0)
        assert self.calc.calculate_portfolio_value() == 32000.0
        
        # Remove position (quantity = 0)
        self.calc.add_position("AAPL", 0, 160.0)
        assert self.calc.calculate_portfolio_value() == 0
    
    def test_volatility_management(self):
        """Test volatility setting and validation."""
        # Valid volatility
        self.calc.set_asset_volatility("AAPL", 0.025)
        assert self.calc.volatilities["AAPL"] == 0.025
        
        # Invalid volatility
        with pytest.raises(ValueError, match="Volatility cannot be negative"):
            self.calc.set_asset_volatility("AAPL", -0.01)
    
    def test_correlation_management(self):
        """Test correlation setting and validation."""
        # Valid correlation
        self.calc.set_correlation("AAPL", "GOOGL", 0.7)
        assert self.calc.correlations[("AAPL", "GOOGL")] == 0.7
        assert self.calc.correlations[("GOOGL", "AAPL")] == 0.7
        assert self.calc.correlations[("AAPL", "AAPL")] == 1.0
        
        # Invalid correlations
        with pytest.raises(ValueError, match="Correlation must be between -1 and 1"):
            self.calc.set_correlation("AAPL", "GOOGL", 1.5)
        
        with pytest.raises(ValueError, match="Correlation must be between -1 and 1"):
            self.calc.set_correlation("AAPL", "GOOGL", -1.5)
    
    def test_portfolio_volatility_calculation(self):
        """Test portfolio volatility with correlations."""
        # Set up portfolio
        self.calc.add_position("AAPL", 100, 100.0)  # $10,000
        self.calc.add_position("GOOGL", 50, 200.0)   # $10,000
        # Equal weights: 0.5 each
        
        # Set volatilities
        self.calc.set_asset_volatility("AAPL", 0.02)  # 2%
        self.calc.set_asset_volatility("GOOGL", 0.03) # 3%
        
        # Test with perfect correlation
        self.calc.set_correlation("AAPL", "GOOGL", 1.0)
        vol_perfect = self.calc.calculate_portfolio_volatility()
        expected_perfect = 0.5 * 0.02 + 0.5 * 0.03  # Weighted average
        assert abs(vol_perfect - expected_perfect) < 0.001
        
        # Test with zero correlation
        self.calc.set_correlation("AAPL", "GOOGL", 0.0)
        vol_zero = self.calc.calculate_portfolio_volatility()
        expected_zero = math.sqrt(0.5**2 * 0.02**2 + 0.5**2 * 0.03**2)
        assert abs(vol_zero - expected_zero) < 0.001
        
        # Zero correlation should be less than perfect correlation
        assert vol_zero < vol_perfect
        
        # Test with negative correlation
        self.calc.set_correlation("AAPL", "GOOGL", -0.5)
        vol_negative = self.calc.calculate_portfolio_volatility()
        
        # Negative correlation should reduce risk further
        assert vol_negative < vol_zero
    
    def test_var_calculation(self):
        """Test Value at Risk calculation."""
        # Set up simple portfolio
        self.calc.add_position("AAPL", 100, 100.0)  # $10,000
        self.calc.set_asset_volatility("AAPL", 0.02)  # 2% daily vol
        
        # Calculate 95% VaR
        var_95 = self.calc.calculate_var(0.95)
        
        # Expected VaR = Portfolio_Value * Z_score * Volatility
        # For 95%, Z_score ≈ 1.645
        from scipy import stats
        z_score = stats.norm.ppf(0.95)
        expected_var = 10000.0 * z_score * 0.02
        
        assert abs(var_95 - expected_var) < 0.01
        
        # VaR should be positive
        assert var_95 > 0
        
        # 99% VaR should be higher than 95% VaR
        var_99 = self.calc.calculate_var(0.99)
        assert var_99 > var_95
    
    def test_stress_testing(self):
        """Test stress testing functionality."""
        # Set up portfolio
        self.calc.add_position("AAPL", 100, 100.0)   # $10,000
        self.calc.add_position("GOOGL", 50, 200.0)   # $10,000
        original_value = self.calc.calculate_portfolio_value()  # $20,000
        
        # Stress scenario: AAPL -20%, GOOGL -15%
        stress_scenario = {
            "AAPL": -0.20,
            "GOOGL": -0.15
        }
        
        stressed_value = self.calc.stress_test(stress_scenario)
        
        # Expected: 100 * 80 + 50 * 170 = 8000 + 8500 = 16500
        expected_value = 100 * (100 * 0.8) + 50 * (200 * 0.85)
        assert abs(stressed_value - expected_value) < 0.01
        
        # Stressed value should be less than original
        assert stressed_value < original_value
        
        # Test partial scenario (only some assets affected)
        partial_scenario = {"AAPL": -0.10}
        partial_stressed = self.calc.stress_test(partial_scenario)
        expected_partial = 100 * (100 * 0.9) + 50 * 200  # GOOGL unchanged
        assert abs(partial_stressed - expected_partial) < 0.01
    
    def test_missing_data_handling(self):
        """Test handling of missing volatility data."""
        self.calc.add_position("AAPL", 100, 100.0)
        self.calc.add_position("GOOGL", 50, 200.0)
        
        # Try to calculate volatility without setting volatilities
        with pytest.raises(ValueError, match="Missing volatility data"):
            self.calc.calculate_portfolio_volatility()
    
    def test_invalid_inputs(self):
        """Test validation of invalid inputs."""
        # Negative price
        with pytest.raises(ValueError, match="Price cannot be negative"):
            self.calc.add_position("AAPL", 100, -50.0)
        
        # Invalid confidence level
        self.calc.add_position("AAPL", 100, 100.0)
        self.calc.set_asset_volatility("AAPL", 0.02)
        
        with pytest.raises(ValueError, match="Confidence level must be between 0 and 1"):
            self.calc.calculate_var(1.5)
        
        with pytest.raises(ValueError, match="Confidence level must be between 0 and 1"):
            self.calc.calculate_var(-0.1)


class TestAdvancedPortfolioAnalytics:
    """Test advanced portfolio analytics features."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.calc = AdvancedPortfolioAnalytics()
        
        # Set up a standard portfolio for testing
        self.calc.add_position("AAPL", 100, 100.0)
        self.calc.add_position("GOOGL", 50, 200.0)
        self.calc.set_asset_volatility("AAPL", 0.02)
        self.calc.set_asset_volatility("GOOGL", 0.03)
        self.calc.set_correlation("AAPL", "GOOGL", 0.5)
    
    def test_sharpe_ratio(self):
        """Test Sharpe ratio calculation."""
        portfolio_return = 0.10  # 10% annual return
        sharpe = self.calc.calculate_sharpe_ratio(portfolio_return, risk_free_rate=0.02)
        
        # Should be positive for positive excess return
        assert sharpe > 0
    
    def test_beta_calculation(self):
        """Test portfolio beta calculation."""
        beta = self.calc.calculate_beta(market_volatility=0.15, market_correlation=0.8)
        
        # Beta should be reasonable (typically 0.5 to 2.0 for diversified portfolio)
        assert 0.1 < beta < 5.0
    
    def test_monte_carlo_var(self):
        """Test Monte Carlo VaR calculation."""
        mc_var = self.calc.monte_carlo_var(confidence_level=0.95, num_simulations=1000)
        parametric_var = self.calc.calculate_var(0.95)
        
        # Monte Carlo should be reasonably close to parametric (within 30%)
        relative_diff = abs(mc_var - parametric_var) / parametric_var
        assert relative_diff < 0.3
        
        # Both should be positive
        assert mc_var > 0
        assert parametric_var > 0
    
    def test_expected_shortfall(self):
        """Test Expected Shortfall calculation."""
        es = self.calc.expected_shortfall(confidence_level=0.95, num_simulations=1000)
        var = self.calc.monte_carlo_var(confidence_level=0.95, num_simulations=1000)
        
        # Expected Shortfall should be higher than VaR
        assert es >= var
        assert es > 0
    
    def test_component_var(self):
        """Test component VaR calculation."""
        component_vars = self.calc.component_var(confidence_level=0.95)
        
        # Should have component VaR for each position
        assert "AAPL" in component_vars
        assert "GOOGL" in component_vars
        
        # All component VaRs should be positive
        assert all(cv >= 0 for cv in component_vars.values())
        
        # Sum of component VaRs should approximately equal total VaR
        total_component_var = sum(component_vars.values())
        total_var = self.calc.calculate_var(0.95)
        
        # Allow some tolerance due to calculation differences
        relative_diff = abs(total_component_var - total_var) / total_var
        assert relative_diff < 0.1  # Within 10%


class TestRiskReporter:
    """Test risk reporting functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.calc = PortfolioRiskCalculator()
        
        # Create a comprehensive portfolio
        self.calc.add_position("AAPL", 100, 150.0)
        self.calc.add_position("GOOGL", 50, 2800.0)
        self.calc.add_position("MSFT", 75, 300.0)
        
        # Set volatilities and correlations
        self.calc.set_asset_volatility("AAPL", 0.025)
        self.calc.set_asset_volatility("GOOGL", 0.030)
        self.calc.set_asset_volatility("MSFT", 0.022)
        
        self.calc.set_correlation("AAPL", "GOOGL", 0.7)
        self.calc.set_correlation("AAPL", "MSFT", 0.8)
        self.calc.set_correlation("GOOGL", "MSFT", 0.6)
        
        self.reporter = RiskReporter(self.calc)
    
    def test_comprehensive_risk_report(self):
        """Test generation of comprehensive risk report."""
        report = self.reporter.generate_risk_report()
        
        # Check report structure
        assert 'portfolio_summary' in report
        assert 'risk_metrics' in report
        assert 'stress_scenarios' in report
        assert 'diversification_metrics' in report
        
        # Check portfolio summary
        portfolio_summary = report['portfolio_summary']
        assert portfolio_summary['total_value'] > 0
        assert portfolio_summary['num_positions'] == 3
        assert len(portfolio_summary['weights']) == 3
        
        # Check risk metrics
        risk_metrics = report['risk_metrics']
        assert risk_metrics['portfolio_volatility'] > 0
        assert risk_metrics['var_95'] > 0
        assert risk_metrics['var_99'] > risk_metrics['var_95']
        
        # Check stress scenarios
        stress_scenarios = report['stress_scenarios']
        assert len(stress_scenarios) > 0
        
        for scenario_name, scenario_results in stress_scenarios.items():
            assert 'stressed_value' in scenario_results
            assert 'absolute_loss' in scenario_results
            assert 'percentage_loss' in scenario_results
            
            # Losses should be reasonable
            assert scenario_results['absolute_loss'] >= 0
            assert 0 <= scenario_results['percentage_loss'] <= 1
        
        # Check diversification metrics
        div_metrics = report['diversification_metrics']
        assert 'concentration' in div_metrics
        assert 'effective_positions' in div_metrics
        assert div_metrics['concentration'] > 0
        assert div_metrics['effective_positions'] > 1  # Should be diversified


class TestRealWorldScenarios:
    """Test with realistic financial scenarios."""
    
    def test_typical_equity_portfolio(self):
        """Test with typical equity portfolio parameters."""
        calc = PortfolioRiskCalculator()
        
        # Typical large-cap equity portfolio
        positions = [
            ("AAPL", 100, 175.0),  # Tech
            ("MSFT", 80, 330.0),   # Tech
            ("JNJ", 150, 160.0),   # Healthcare
            ("JPM", 120, 140.0),   # Finance
            ("XOM", 200, 80.0)     # Energy
        ]
        
        for symbol, quantity, price in positions:
            calc.add_position(symbol, quantity, price)
        
        # Set realistic volatilities (annualized to daily)
        volatilities = {
            "AAPL": 0.30 / math.sqrt(252),  # 30% annual
            "MSFT": 0.25 / math.sqrt(252),  # 25% annual
            "JNJ": 0.15 / math.sqrt(252),   # 15% annual
            "JPM": 0.35 / math.sqrt(252),   # 35% annual
            "XOM": 0.40 / math.sqrt(252)    # 40% annual
        }
        
        for symbol, vol in volatilities.items():
            calc.set_asset_volatility(symbol, vol)
        
        # Set realistic sector correlations
        correlations = [
            ("AAPL", "MSFT", 0.8),   # Same sector
            ("AAPL", "JNJ", 0.3),    # Different sectors
            ("AAPL", "JPM", 0.5),    # Market correlation
            ("AAPL", "XOM", 0.2),    # Low correlation
            ("MSFT", "JNJ", 0.3),
            ("MSFT", "JPM", 0.5),
            ("MSFT", "XOM", 0.2),
            ("JNJ", "JPM", 0.4),
            ("JNJ", "XOM", 0.1),     # Defensive vs cyclical
            ("JPM", "XOM", 0.6)      # Both cyclical
        ]
        
        for symbol1, symbol2, corr in correlations:
            calc.set_correlation(symbol1, symbol2, corr)
        
        # Calculate metrics
        portfolio_value = calc.calculate_portfolio_value()
        portfolio_vol = calc.calculate_portfolio_volatility()
        var_95 = calc.calculate_var(0.95)
        
        # Sanity checks
        assert portfolio_value > 50000  # Reasonable portfolio size
        assert 0.01 < portfolio_vol < 0.05  # Daily vol between 1-5%
        assert var_95 > 0
        assert var_95 < portfolio_value * 0.1  # VaR should be < 10% of portfolio
    
    def test_market_crash_scenario(self):
        """Test portfolio behavior during market crash."""
        calc = PortfolioRiskCalculator()
        
        # Simple two-asset portfolio
        calc.add_position("SPY", 1000, 400.0)  # S&P 500 ETF
        calc.add_position("TLT", 500, 100.0)   # Treasury ETF
        
        calc.set_asset_volatility("SPY", 0.01)  # 1% daily
        calc.set_asset_volatility("TLT", 0.008) # 0.8% daily
        calc.set_correlation("SPY", "TLT", -0.3)  # Negative correlation
        
        original_value = calc.calculate_portfolio_value()
        
        # 2008-style crash scenario
        crash_scenario = {
            "SPY": -0.40,  # 40% drop in equities
            "TLT": 0.15    # 15% gain in bonds (flight to quality)
        }
        
        stressed_value = calc.stress_test(crash_scenario)
        
        # Portfolio should lose money but less than pure equity exposure
        loss_pct = (original_value - stressed_value) / original_value
        
        # Loss should be between 10-30% (less than 40% due to bond allocation)
        assert 0.1 < loss_pct < 0.3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])