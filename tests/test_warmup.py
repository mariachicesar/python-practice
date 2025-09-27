import pytest
import sys
from pathlib import Path

# Add the solutions directory to Python path
solutions_dir = Path(__file__).parent.parent / "solutions"
sys.path.insert(0, str(solutions_dir))

from solutions.warmup import parse_stock_data, parse_stock_data_enhanced, parse_multiple_stock_data


class TestParseStockData:
    """Test suite for the stock data parser."""
    
    def test_basic_functionality(self):
        """Test basic parsing functionality."""
        result = parse_stock_data("AAPL:+2.5,-1.2,+0.8,-0.3,+1.1")
        
        assert result['ticker'] == 'AAPL'
        assert result['changes'] == [2.5, -1.2, 0.8, -0.3, 1.1]
        assert abs(result['net_change'] - 2.9) < 0.01
    
    def test_no_changes(self):
        """Test parsing with no price changes."""
        result = parse_stock_data("MSFT:")
        
        assert result['ticker'] == 'MSFT'
        assert result['changes'] == []
        assert result['net_change'] == 0
    
    def test_case_sensitivity(self):
        """Test ticker case conversion."""
        result = parse_stock_data("googl:+5.0,-2.1")
        
        assert result['ticker'] == 'GOOGL'
        assert result['changes'] == [5.0, -2.1]
        assert abs(result['net_change'] - 2.9) < 0.01
    
    def test_whitespace_handling(self):
        """Test handling of extra whitespace."""
        result = parse_stock_data(" TSLA : +1.0 , -0.5 , +2.0 ")
        
        assert result['ticker'] == 'TSLA'
        assert result['changes'] == [1.0, -0.5, 2.0]
        assert abs(result['net_change'] - 2.5) < 0.01
    
    def test_single_change(self):
        """Test parsing with a single price change."""
        result = parse_stock_data("META:+3.75")
        
        assert result['ticker'] == 'META'
        assert result['changes'] == [3.75]
        assert result['net_change'] == 3.75
    
    def test_mixed_number_formats(self):
        """Test various number formats."""
        result = parse_stock_data("NVDA:1.5,-2.0,0.5")
        
        assert result['changes'] == [1.5, -2.0, 0.5]
        assert result['net_change'] == 0.0
    
    def test_precision_handling(self):
        """Test floating point precision."""
        result = parse_stock_data("AAPL:+0.01,-0.01")
        
        assert result['net_change'] == 0.0
    
    def test_large_numbers(self):
        """Test handling of large price changes."""
        result = parse_stock_data("BRK:+1000.50,-999.75")
        
        assert abs(result['net_change'] - 0.75) < 0.01


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_missing_colon(self):
        """Test invalid format without colon."""
        with pytest.raises(ValueError, match="Invalid input format"):
            parse_stock_data("AAPL+1.0,-2.0")
    
    def test_empty_input(self):
        """Test empty input string."""
        with pytest.raises(ValueError, match="Invalid input format"):
            parse_stock_data("")
    
    def test_none_input(self):
        """Test None input."""
        with pytest.raises((ValueError, AttributeError)):
            parse_stock_data(None)
    
    def test_empty_ticker(self):
        """Test empty ticker symbol."""
        with pytest.raises(ValueError, match="empty"):
            parse_stock_data(":+1.0,-2.0")
    
    def test_invalid_price_change(self):
        """Test invalid price change values."""
        with pytest.raises(ValueError, match="Invalid price change"):
            parse_stock_data("AAPL:+1.0,invalid,-2.0")
    
    def test_whitespace_only_ticker(self):
        """Test ticker with only whitespace."""
        with pytest.raises(ValueError, match="empty"):
            parse_stock_data("   :+1.0,-2.0")


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_zero_changes(self):
        """Test zero price changes."""
        result = parse_stock_data("AAPL:0.0,0.0,0.0")
        
        assert result['changes'] == [0.0, 0.0, 0.0]
        assert result['net_change'] == 0.0
    
    def test_very_small_numbers(self):
        """Test very small price changes."""
        result = parse_stock_data("AAPL:+0.001,-0.001")
        
        assert result['net_change'] == 0.0
    
    def test_many_decimal_places(self):
        """Test numbers with many decimal places."""
        result = parse_stock_data("AAPL:+1.123456,-0.123456")
        
        assert abs(result['net_change'] - 1.0) < 0.01
    
    def test_scientific_notation(self):
        """Test scientific notation (if supported)."""
        try:
            result = parse_stock_data("AAPL:1e-2,-2e-2")
            assert abs(result['net_change'] - (-0.01)) < 0.001
        except ValueError:
            # Scientific notation might not be supported
            pytest.skip("Scientific notation not supported")
    
    def test_multiple_colons(self):
        """Test string with multiple colons."""
        result = parse_stock_data("AAPL:INFO:+1.0,-2.0")
        
        assert result['ticker'] == 'AAPL'
        # Should handle everything after first colon as changes


class TestEnhancedFeatures:
    """Test enhanced version with additional features."""
    
    def test_additional_metrics(self):
        """Test additional metrics in enhanced version."""
        result = parse_stock_data_enhanced("AAPL:+2.0,-1.0,+3.0")
        
        assert result['max_change'] == 3.0
        assert result['min_change'] == -1.0
        assert result['volatility'] == 2.0  # (2 + 1 + 3) / 3
        assert result['num_changes'] == 3
    
    def test_ticker_validation(self):
        """Test ticker format validation."""
        # Valid ticker
        result = parse_stock_data_enhanced("AAPL:+1.0", validate_ticker=True)
        assert result['ticker'] == 'AAPL'
        
        # Invalid ticker (too long)
        with pytest.raises(ValueError, match="Invalid ticker format"):
            parse_stock_data_enhanced("TOOLONG:+1.0", validate_ticker=True)
    
    def test_no_validation(self):
        """Test with ticker validation disabled."""
        result = parse_stock_data_enhanced("TOOLONG:+1.0", validate_ticker=False)
        assert result['ticker'] == 'TOOLONG'


class TestBatchProcessing:
    """Test batch processing functionality."""
    
    def test_successful_batch(self):
        """Test processing multiple valid strings."""
        data_strings = [
            "AAPL:+1.0,-0.5",
            "GOOGL:+2.0,-1.0",
            "MSFT:+0.5,-0.25"
        ]
        
        result = parse_multiple_stock_data(data_strings)
        
        assert len(result['results']) == 3
        assert len(result['errors']) == 0
        assert result['success_rate'] == 1.0
    
    def test_mixed_batch(self):
        """Test processing batch with some errors."""
        data_strings = [
            "AAPL:+1.0,-0.5",  # Valid
            "INVALID_FORMAT",   # Invalid
            "GOOGL:+2.0,-1.0",  # Valid
            "MSFT:invalid_change"  # Invalid
        ]
        
        result = parse_multiple_stock_data(data_strings)
        
        assert len(result['results']) == 2
        assert len(result['errors']) == 2
        assert result['success_rate'] == 0.5
    
    def test_empty_batch(self):
        """Test processing empty list."""
        result = parse_multiple_stock_data([])
        
        assert len(result['results']) == 0
        assert len(result['errors']) == 0
        assert result['success_rate'] == 0


class TestPerformance:
    """Test performance characteristics."""
    
    def test_large_input(self):
        """Test parsing string with many changes."""
        changes = ",".join([f"+{i}.0" for i in range(1000)])
        data_string = f"AAPL:{changes}"
        
        result = parse_stock_data(data_string)
        
        assert result['ticker'] == 'AAPL'
        assert len(result['changes']) == 1000
        assert result['net_change'] == sum(range(1, 1001))
    
    @pytest.mark.slow
    def test_batch_performance(self):
        """Test performance with large batch."""
        # Generate 1000 test strings
        data_strings = [f"STOCK{i}:+{i}.0,-{i/2}.0" for i in range(1, 1001)]
        
        result = parse_multiple_stock_data(data_strings)
        
        assert len(result['results']) == 1000
        assert result['success_rate'] == 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])