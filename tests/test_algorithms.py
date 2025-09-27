import pytest
import sys
import numpy as np
from pathlib import Path

# Add the solutions directory to Python path
solutions_dir = Path(__file__).parent.parent / "solutions"
sys.path.insert(0, str(solutions_dir))

from solutions.algorithms import MarketDataProcessor, AdvancedMarketDataProcessor


class TestMarketDataProcessor:
    """Test suite for Market Data Processor."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = MarketDataProcessor()
        
    def test_empty_processor(self):
        """Test behavior with no data."""
        assert self.processor.get_current_price() is None
        assert self.processor.get_price_at_time(1000) is None
        assert self.processor.get_average_price(1000, 2000) is None
        assert self.processor.get_price_range(1000, 2000) is None
    
    def test_single_price_point(self):
        """Test with single price point."""
        self.processor.add_price(1000, 100.0)
        
        assert self.processor.get_current_price() == 100.0
        assert self.processor.get_price_at_time(999) is None
        assert self.processor.get_price_at_time(1000) == 100.0
        assert self.processor.get_price_at_time(1001) == 100.0
        assert self.processor.get_average_price(1000, 1000) == 100.0
        assert self.processor.get_price_range(1000, 1000) == (100.0, 100.0)
    
    def test_multiple_price_points(self):
        """Test with multiple price points in order."""
        prices = [(1000, 100.0), (1001, 101.0), (1002, 99.0), (1003, 102.0)]
        
        for timestamp, price in prices:
            self.processor.add_price(timestamp, price)
        
        assert self.processor.get_current_price() == 102.0
        assert self.processor.get_price_at_time(1001) == 101.0
        
        # Test range queries
        avg = self.processor.get_average_price(1000, 1002)
        expected_avg = (100.0 + 101.0 + 99.0) / 3
        assert abs(avg - expected_avg) < 0.001
        
        price_range = self.processor.get_price_range(1000, 1002)
        assert price_range == (99.0, 101.0)
    
    def test_out_of_order_insertion(self):
        """Test inserting timestamps out of chronological order."""
        # Add in random order
        self.processor.add_price(1002, 99.0)
        self.processor.add_price(1000, 100.0)
        self.processor.add_price(1003, 102.0)
        self.processor.add_price(1001, 101.0)
        
        # Should still work correctly
        assert self.processor.get_current_price() == 102.0
        assert self.processor.get_price_at_time(1000) == 100.0
        assert self.processor.get_price_at_time(1001) == 101.0
        assert self.processor.get_price_at_time(1002) == 99.0
    
    def test_duplicate_timestamps(self):
        """Test updating existing timestamps."""
        self.processor.add_price(1000, 100.0)
        self.processor.add_price(1001, 101.0)
        
        # Update existing timestamp
        self.processor.add_price(1000, 105.0)
        
        assert self.processor.get_price_at_time(1000) == 105.0
        assert self.processor.get_price_at_time(1001) == 101.0
    
    def test_price_at_time_interpolation(self):
        """Test getting price at time between data points."""
        self.processor.add_price(1000, 100.0)
        self.processor.add_price(1002, 102.0)
        
        # Should return most recent price before timestamp
        assert self.processor.get_price_at_time(1001) == 100.0
        assert self.processor.get_price_at_time(1003) == 102.0
        assert self.processor.get_price_at_time(999) is None
    
    def test_range_queries_edge_cases(self):
        """Test edge cases for range queries."""
        prices = [(1000, 100.0), (1001, 101.0), (1002, 99.0), (1003, 102.0)]
        
        for timestamp, price in prices:
            self.processor.add_price(timestamp, price)
        
        # Empty range
        assert self.processor.get_average_price(1004, 1005) is None
        assert self.processor.get_price_range(1004, 1005) is None
        
        # Single point range
        assert self.processor.get_average_price(1001, 1001) == 101.0
        assert self.processor.get_price_range(1001, 1001) == (101.0, 101.0)
        
        # Partial overlap
        avg = self.processor.get_average_price(999, 1000)
        assert avg == 100.0
    
    def test_large_dataset_performance(self):
        """Test performance with large dataset."""
        import time
        
        # Add 10,000 price points
        start_time = time.time()
        for i in range(10000):
            self.processor.add_price(1000 + i, 100.0 + i * 0.01)
        insert_time = time.time() - start_time
        
        # Should complete reasonably quickly (adjust threshold as needed)
        assert insert_time < 5.0  # 5 seconds for 10k insertions
        
        # Test query performance
        start_time = time.time()
        for _ in range(100):
            self.processor.get_average_price(1000, 2000)
        query_time = time.time() - start_time
        
        assert query_time < 1.0  # 1 second for 100 queries
    
    def test_precision_handling(self):
        """Test floating point precision handling."""
        self.processor.add_price(1000, 100.12345)
        self.processor.add_price(1001, 100.67890)
        
        avg = self.processor.get_average_price(1000, 1001)
        expected = (100.12345 + 100.67890) / 2
        
        assert abs(avg - expected) < 1e-10


class TestAdvancedMarketDataProcessor:
    """Test suite for Advanced Market Data Processor."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = AdvancedMarketDataProcessor(max_size=1000, window_size=3600)
    
    def test_memory_management(self):
        """Test automatic cleanup of old data."""
        # Add data that exceeds max_size
        for i in range(1500):
            timestamp = 1000 + i * 1000  # 1 second intervals
            self.processor.add_price(timestamp, 100.0 + i)
        
        # Should have cleaned up old data
        stats = self.processor.get_statistics()
        assert stats['data_points'] <= self.processor.max_size
    
    def test_statistics_tracking(self):
        """Test statistics collection."""
        # Add some data and make queries
        for i in range(100):
            self.processor.add_price(1000 + i, 100.0 + i)
        
        # Make various queries
        self.processor.get_current_price()
        self.processor.get_price_at_time(1050)
        self.processor.get_average_price(1000, 1010)
        self.processor.get_price_range(1000, 1010)
        
        stats = self.processor.get_statistics()
        
        assert stats['data_points'] == 100
        assert stats['operations']['total_updates'] == 100
        assert stats['operations']['queries']['current'] >= 1
        assert stats['operations']['queries']['at_time'] >= 1
        assert stats['operations']['queries']['average'] >= 1
        assert stats['operations']['queries']['range'] >= 1
    
    def test_bulk_operations(self):
        """Test bulk price insertion."""
        # Create bulk data
        bulk_data = [(1000 + i, 100.0 + i * 0.1) for i in range(1000)]
        
        # Test bulk insertion
        import time
        start_time = time.time()
        self.processor.bulk_add_prices(bulk_data)
        bulk_time = time.time() - start_time
        
        # Should be faster than individual insertions
        assert self.processor.get_statistics()['data_points'] == 1000
    
    def test_volatility_calculation(self):
        """Test volatility calculation."""
        # Add price data with known volatility pattern
        prices = [100.0, 101.0, 99.0, 102.0, 98.0, 103.0, 97.0]
        
        for i, price in enumerate(prices):
            self.processor.add_price(1000 + i, price)
        
        vol = self.processor.get_volatility(1000, 1006)
        
        # Should calculate reasonable volatility
        assert vol is not None
        assert vol > 0


class TestPerformanceComparison:
    """Compare performance of different implementations."""
    
    @pytest.mark.slow
    def test_implementation_comparison(self):
        """Compare basic vs advanced implementations."""
        basic = MarketDataProcessor()
        advanced = AdvancedMarketDataProcessor()
        
        # Create test data
        test_data = [(1000 + i, 100.0 + i * 0.01) for i in range(1000)]
        
        # Test insertion performance
        import time
        
        # Basic implementation
        start_time = time.time()
        for timestamp, price in test_data:
            basic.add_price(timestamp, price)
        basic_insert_time = time.time() - start_time
        
        # Advanced implementation
        start_time = time.time()
        for timestamp, price in test_data:
            advanced.add_price(timestamp, price)
        advanced_insert_time = time.time() - start_time
        
        # Both should complete reasonably quickly
        assert basic_insert_time < 5.0
        assert advanced_insert_time < 5.0
        
        print(f"Basic insertion time: {basic_insert_time:.3f}s")
        print(f"Advanced insertion time: {advanced_insert_time:.3f}s")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])