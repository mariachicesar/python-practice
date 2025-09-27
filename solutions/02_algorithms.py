# Solution: Market Data Stream Processor
# Bloomberg Python Technical Interview - Problem 2

from bisect import bisect_left, bisect_right
from typing import List, Tuple, Optional
import time
from collections import defaultdict

# Basic implementation using sorted lists
class MarketDataProcessor:
    def __init__(self):
        """
        Market data processor using sorted lists for efficient time-based queries.
        
        Time Complexity:
        - add_price: O(n) due to insertion in sorted list
        - get_current_price: O(1)
        - get_price_at_time: O(log n)
        - get_average_price: O(k + log n) where k is number of points in range
        - get_price_range: O(k + log n) where k is number of points in range
        
        Space Complexity: O(n) where n is number of price points
        """
        self.timestamps = []  # Sorted list of timestamps
        self.prices = []      # Corresponding prices
    
    def add_price(self, timestamp: int, price: float) -> None:
        """Add a new price point, maintaining sorted order by timestamp."""
        if not self.timestamps or timestamp >= self.timestamps[-1]:
            # Common case: new timestamp is latest (append operation)
            self.timestamps.append(timestamp)
            self.prices.append(price)
        else:
            # Find insertion position using binary search
            idx = bisect_left(self.timestamps, timestamp)
            if idx < len(self.timestamps) and self.timestamps[idx] == timestamp:
                # Update existing timestamp
                self.prices[idx] = price
            else:
                # Insert new timestamp and price
                self.timestamps.insert(idx, timestamp)
                self.prices.insert(idx, price)
    
    def get_current_price(self) -> Optional[float]:
        """Get the most recent price."""
        return self.prices[-1] if self.prices else None
    
    def get_price_at_time(self, timestamp: int) -> Optional[float]:
        """Get price at specific time (or most recent before that time)."""
        if not self.timestamps:
            return None
        
        # Find the rightmost position <= timestamp
        idx = bisect_right(self.timestamps, timestamp) - 1
        
        if idx >= 0:
            return self.prices[idx]
        return None
    
    def get_average_price(self, start_time: int, end_time: int) -> Optional[float]:
        """Get average price in time window [start_time, end_time]."""
        if not self.timestamps:
            return None
        
        # Find range of indices
        start_idx = bisect_left(self.timestamps, start_time)
        end_idx = bisect_right(self.timestamps, end_time)
        
        if start_idx >= end_idx:
            return None
        
        # Calculate average
        price_sum = sum(self.prices[start_idx:end_idx])
        count = end_idx - start_idx
        
        return price_sum / count
    
    def get_price_range(self, start_time: int, end_time: int) -> Optional[Tuple[float, float]]:
        """Get (min_price, max_price) in time window [start_time, end_time]."""
        if not self.timestamps:
            return None
        
        # Find range of indices
        start_idx = bisect_left(self.timestamps, start_time)
        end_idx = bisect_right(self.timestamps, end_time)
        
        if start_idx >= end_idx:
            return None
        
        # Find min and max in range
        prices_in_range = self.prices[start_idx:end_idx]
        return (min(prices_in_range), max(prices_in_range))


# Optimized implementation using SortedDict
try:
    from sortedcontainers import SortedDict
    
    class OptimizedMarketDataProcessor:
        def __init__(self):
            """
            Optimized market data processor using SortedDict.
            
            Time Complexity:
            - add_price: O(log n)
            - get_current_price: O(1)
            - get_price_at_time: O(log n)
            - get_average_price: O(k + log n)
            - get_price_range: O(k + log n)
            """
            self.data = SortedDict()  # timestamp -> price
        
        def add_price(self, timestamp: int, price: float) -> None:
            """Add a new price point."""
            self.data[timestamp] = price
        
        def get_current_price(self) -> Optional[float]:
            """Get the most recent price."""
            return self.data.peekitem(-1)[1] if self.data else None
        
        def get_price_at_time(self, timestamp: int) -> Optional[float]:
            """Get price at specific time (or most recent before that time)."""
            if not self.data:
                return None
            
            try:
                return self.data[timestamp]
            except KeyError:
                # Find the largest key <= timestamp
                idx = self.data.bisect_right(timestamp) - 1
                if idx >= 0:
                    return self.data.peekitem(idx)[1]
                return None
        
        def get_average_price(self, start_time: int, end_time: int) -> Optional[float]:
            """Get average price in time window."""
            if not self.data:
                return None
            
            # Get items in range
            items = list(self.data.irange(start_time, end_time, inclusive=(True, True)))
            
            if not items:
                return None
            
            prices = [self.data[timestamp] for timestamp in items]
            return sum(prices) / len(prices)
        
        def get_price_range(self, start_time: int, end_time: int) -> Optional[Tuple[float, float]]:
            """Get (min_price, max_price) in time window."""
            if not self.data:
                return None
            
            items = list(self.data.irange(start_time, end_time, inclusive=(True, True)))
            
            if not items:
                return None
            
            prices = [self.data[timestamp] for timestamp in items]
            return (min(prices), max(prices))

except ImportError:
    # Fallback if sortedcontainers is not available
    OptimizedMarketDataProcessor = MarketDataProcessor


# Advanced implementation with additional features
class AdvancedMarketDataProcessor(MarketDataProcessor):
    """Extended processor with memory management and analytics."""
    
    def __init__(self, max_size: int = 100000, window_size: int = 3600):
        """
        Initialize with memory management.
        
        Args:
            max_size: Maximum number of data points to keep
            window_size: Time window in seconds for sliding window
        """
        super().__init__()
        self.max_size = max_size
        self.window_size = window_size
        self.stats = {
            'total_updates': 0,
            'queries': defaultdict(int),
            'last_cleanup': time.time()
        }
    
    def add_price(self, timestamp: int, price: float) -> None:
        """Add price with memory management."""
        super().add_price(timestamp, price)
        self.stats['total_updates'] += 1
        
        # Trigger cleanup if needed
        if len(self.timestamps) > self.max_size:
            self._cleanup_old_data()
    
    def _cleanup_old_data(self) -> None:
        """Remove old data points to free memory."""
        if not self.timestamps:
            return
        
        current_time = self.timestamps[-1]
        cutoff_time = current_time - self.window_size * 1000  # Convert to milliseconds
        
        # Find first index to keep
        idx = bisect_left(self.timestamps, cutoff_time)
        
        if idx > 0:
            # Remove old data
            self.timestamps = self.timestamps[idx:]
            self.prices = self.prices[idx:]
            self.stats['last_cleanup'] = time.time()
    
    def get_current_price(self) -> Optional[float]:
        """Get current price with analytics."""
        self.stats['queries']['current'] += 1
        return super().get_current_price()
    
    def get_price_at_time(self, timestamp: int) -> Optional[float]:
        """Get price at time with analytics."""
        self.stats['queries']['at_time'] += 1
        return super().get_price_at_time(timestamp)
    
    def get_average_price(self, start_time: int, end_time: int) -> Optional[float]:
        """Get average price with analytics."""
        self.stats['queries']['average'] += 1
        return super().get_average_price(start_time, end_time)
    
    def get_price_range(self, start_time: int, end_time: int) -> Optional[Tuple[float, float]]:
        """Get price range with analytics."""
        self.stats['queries']['range'] += 1
        return super().get_price_range(start_time, end_time)
    
    def get_statistics(self) -> dict:
        """Get processor statistics."""
        return {
            'data_points': len(self.timestamps),
            'time_range': {
                'start': self.timestamps[0] if self.timestamps else None,
                'end': self.timestamps[-1] if self.timestamps else None,
                'span_seconds': (self.timestamps[-1] - self.timestamps[0]) / 1000 if len(self.timestamps) > 1 else 0
            },
            'memory_usage': {
                'max_size': self.max_size,
                'current_size': len(self.timestamps),
                'utilization': len(self.timestamps) / self.max_size
            },
            'operations': dict(self.stats)
        }
    
    def bulk_add_prices(self, price_data: List[Tuple[int, float]]) -> None:
        """Efficiently add multiple price points."""
        # Sort by timestamp for efficient insertion
        sorted_data = sorted(price_data, key=lambda x: x[0])
        
        for timestamp, price in sorted_data:
            self.add_price(timestamp, price)
    
    def get_volatility(self, start_time: int, end_time: int, window: int = 100) -> Optional[float]:
        """Calculate price volatility in time window."""
        if not self.timestamps:
            return None
        
        # Get prices in range
        start_idx = bisect_left(self.timestamps, start_time)
        end_idx = bisect_right(self.timestamps, end_time)
        
        if end_idx - start_idx < 2:
            return None
        
        prices = self.prices[start_idx:end_idx]
        
        # Calculate returns
        returns = []
        for i in range(1, len(prices)):
            if prices[i-1] != 0:  # Avoid division by zero
                ret = (prices[i] - prices[i-1]) / prices[i-1]
                returns.append(ret)
        
        if len(returns) < 2:
            return None
        
        # Calculate standard deviation
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / (len(returns) - 1)
        
        return variance ** 0.5


# Test and benchmark functions
def create_test_data(num_points: int = 1000, time_step: int = 1000) -> List[Tuple[int, float]]:
    """Create test data for benchmarking."""
    import random
    
    base_time = int(time.time() * 1000)  # Current time in milliseconds
    base_price = 100.0
    
    data = []
    current_price = base_price
    
    for i in range(num_points):
        timestamp = base_time + i * time_step
        # Random walk price movement
        price_change = random.uniform(-0.05, 0.05) * current_price
        current_price = max(0.01, current_price + price_change)  # Ensure positive price
        data.append((timestamp, current_price))
    
    return data


def benchmark_processors():
    """Benchmark different processor implementations."""
    import time
    
    print("📊 Benchmarking Market Data Processors")
    print("=" * 50)
    
    # Create test data
    test_data = create_test_data(10000)
    
    processors = [
        ("Basic", MarketDataProcessor()),
        ("Advanced", AdvancedMarketDataProcessor()),
    ]
    
    try:
        processors.append(("Optimized", OptimizedMarketDataProcessor()))
    except:
        pass
    
    results = {}
    
    for name, processor in processors:
        print(f"\n🔧 Testing {name} Processor")
        
        # Test insertion performance
        start_time = time.time()
        for timestamp, price in test_data:
            processor.add_price(timestamp, price)
        insert_time = time.time() - start_time
        
        # Test query performance
        query_times = []
        for _ in range(1000):
            # Random queries
            idx = len(test_data) // 2
            start_ts = test_data[idx][0]
            end_ts = test_data[idx + 100][0] if idx + 100 < len(test_data) else test_data[-1][0]
            
            start_time = time.time()
            processor.get_average_price(start_ts, end_ts)
            query_times.append(time.time() - start_time)
        
        avg_query_time = sum(query_times) / len(query_times)
        
        results[name] = {
            'insert_time': insert_time,
            'avg_query_time': avg_query_time * 1000,  # Convert to milliseconds
            'data_points': len(test_data)
        }
        
        print(f"  Insert time: {insert_time:.3f}s")
        print(f"  Avg query time: {avg_query_time*1000:.3f}ms")
    
    return results


def test_comprehensive():
    """Comprehensive test suite."""
    print("🧪 Running Comprehensive Tests")
    print("=" * 40)
    
    processor = MarketDataProcessor()
    
    # Test 1: Basic functionality
    print("Test 1: Basic functionality")
    processor.add_price(1000, 100.0)
    processor.add_price(1001, 101.0)
    processor.add_price(1002, 99.0)
    processor.add_price(1003, 102.0)
    
    assert processor.get_current_price() == 102.0
    assert processor.get_price_at_time(1001) == 101.0
    assert processor.get_price_at_time(999) is None
    assert processor.get_price_at_time(1001.5) == 101.0
    print("✅ Basic functionality passed")
    
    # Test 2: Range queries
    print("Test 2: Range queries")
    avg = processor.get_average_price(1000, 1002)
    assert abs(avg - 100.0) < 0.001  # (100 + 101 + 99) / 3
    
    price_range = processor.get_price_range(1000, 1002)
    assert price_range == (99.0, 101.0)
    print("✅ Range queries passed")
    
    # Test 3: Edge cases
    print("Test 3: Edge cases")
    empty_processor = MarketDataProcessor()
    assert empty_processor.get_current_price() is None
    assert empty_processor.get_average_price(1000, 2000) is None
    print("✅ Edge cases passed")
    
    # Test 4: Out-of-order insertion
    print("Test 4: Out-of-order insertion")
    processor.add_price(999, 98.0)  # Earlier timestamp
    assert processor.get_price_at_time(999) == 98.0
    assert processor.get_current_price() == 102.0  # Should still be most recent
    print("✅ Out-of-order insertion passed")
    
    # Test 5: Duplicate timestamps
    print("Test 5: Duplicate timestamps")
    processor.add_price(1002, 103.0)  # Update existing timestamp
    assert processor.get_price_at_time(1002) == 103.0
    print("✅ Duplicate timestamps passed")
    
    print("\n🎉 All tests passed!")


if __name__ == "__main__":
    # Run tests
    test_comprehensive()
    
    # Run benchmarks
    print("\n")
    benchmark_results = benchmark_processors()
    
    # Display advanced processor stats if available
    print("\n📈 Advanced Processor Statistics")
    advanced = AdvancedMarketDataProcessor()
    test_data = create_test_data(1000)
    
    for timestamp, price in test_data:
        advanced.add_price(timestamp, price)
    
    # Generate some queries
    for i in range(50):
        advanced.get_current_price()
        if i % 10 == 0:
            start_ts = test_data[i][0]
            end_ts = test_data[min(i+10, len(test_data)-1)][0]
            advanced.get_average_price(start_ts, end_ts)
    
    stats = advanced.get_statistics()
    print(f"Data points: {stats['data_points']}")
    print(f"Time span: {stats['time_range']['span_seconds']:.1f}s")
    print(f"Total updates: {stats['operations']['total_updates']}")
    print(f"Query breakdown: {dict(stats['operations']['queries'])}")