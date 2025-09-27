# Problem 2: Core Algorithms - Market Data Stream Processor
**Difficulty**: Medium  
**Time**: 25 minutes  
**Focus**: Data structures, algorithms, time complexity, real-time processing

## Problem Statement
You're building a system to process real-time market data for Bloomberg Terminal. Design and implement a data structure that efficiently handles high-frequency price updates and supports various time-based queries.

### Bloomberg Context
In financial markets, price data arrives continuously throughout trading hours. Systems need to:
- Handle thousands of updates per second
- Provide instant access to current prices
- Support historical price lookups
- Calculate statistics over time windows
- Maintain memory efficiency for long-running processes

### Requirements
Implement a `MarketDataProcessor` class with the following interface:

```python
class MarketDataProcessor:
    def add_price(self, timestamp: int, price: float) -> None:
        """Add a new price point with timestamp (milliseconds since epoch)"""
        pass
    
    def get_current_price(self) -> float:
        """Get the most recent price"""
        pass
    
    def get_price_at_time(self, timestamp: int) -> float:
        """Get price at specific time (or most recent before that time)"""
        pass
    
    def get_average_price(self, start_time: int, end_time: int) -> float:
        """Get average price in time window [start_time, end_time]"""
        pass
    
    def get_price_range(self, start_time: int, end_time: int) -> tuple:
        """Get (min_price, max_price) in time window [start_time, end_time]"""
        pass
```

### Example Usage
```python
processor = MarketDataProcessor()

# Add price points (timestamp, price)
processor.add_price(1000, 150.00)  # AAPL at $150.00
processor.add_price(1001, 150.25)  # AAPL at $150.25
processor.add_price(1003, 149.80)  # AAPL at $149.80
processor.add_price(1005, 151.00)  # AAPL at $151.00

# Query operations
current = processor.get_current_price()  # 151.00
price_at = processor.get_price_at_time(1002)  # 150.25 (most recent before 1002)
avg = processor.get_average_price(1000, 1003)  # Average of prices at 1000, 1001, 1003
min_max = processor.get_price_range(1000, 1003)  # (149.80, 150.25)
```

### Performance Requirements
- `add_price`: Should be efficient for frequent calls
- `get_current_price`: Should be O(1) or near O(1)
- `get_price_at_time`: Should be efficient for time-based lookups
- Range queries: Should be efficient for typical time windows

### Your Implementation
```python
class MarketDataProcessor:
    def __init__(self):
        """Initialize your data structure"""
        # TODO: Choose and initialize your data structure
        pass
    
    def add_price(self, timestamp: int, price: float) -> None:
        """Add a new price point"""
        # TODO: Implement efficient insertion
        pass
    
    def get_current_price(self) -> float:
        """Get the most recent price"""
        # TODO: Return most recent price or None if no data
        pass
    
    def get_price_at_time(self, timestamp: int) -> float:
        """Get price at specific time (or most recent before)"""
        # TODO: Implement time-based lookup
        pass
    
    def get_average_price(self, start_time: int, end_time: int) -> float:
        """Get average price in time window"""
        # TODO: Calculate average for time range
        pass
    
    def get_price_range(self, start_time: int, end_time: int) -> tuple:
        """Get (min_price, max_price) in time window"""
        # TODO: Find min/max in time range
        pass

# Test your implementation
if __name__ == "__main__":
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
```

### Test Cases
Your implementation should handle:

```python
# Empty processor
processor = MarketDataProcessor()
assert processor.get_current_price() is None

# Single price point
processor.add_price(1000, 100.0)
assert processor.get_current_price() == 100.0
assert processor.get_price_at_time(999) is None
assert processor.get_price_at_time(1000) == 100.0
assert processor.get_price_at_time(1001) == 100.0

# Multiple price points
processor.add_price(1001, 101.0)
processor.add_price(1002, 99.0)
assert processor.get_current_price() == 99.0
assert processor.get_average_price(1000, 1002) == 100.0  # (100+101+99)/3

# Out-of-order timestamps
processor.add_price(999, 98.0)  # Earlier timestamp
assert processor.get_price_at_time(999) == 98.0
assert processor.get_current_price() == 99.0  # Still most recent

# Duplicate timestamps
processor.add_price(1002, 103.0)  # Update existing timestamp
assert processor.get_price_at_time(1002) == 103.0
```

### Discussion Questions
Be prepared to discuss:

1. **Data Structure Choice**: What data structure did you choose and why?
2. **Trade-offs**: What are the time/space complexity trade-offs of your approach?
3. **Alternatives**: What other data structures could work? When would you choose them?
4. **Scale**: How would your solution handle millions of price points?
5. **Memory Management**: How would you handle memory constraints in a long-running system?
6. **Concurrency**: How would you make this thread-safe for concurrent reads/writes?

### Extension Challenges
If you finish early, consider these extensions:

1. **Memory Optimization**: Implement a sliding window to limit memory usage
2. **Bulk Operations**: Add methods to insert multiple price points efficiently
3. **Persistence**: How would you save/load data to/from disk?
4. **Monitoring**: Add metrics tracking (number of queries, average response time)

### Hints
- Consider sorted data structures for time-based queries
- Binary search can be useful for time lookups
- Think about the most common operations and optimize for them
- Consider using Python's `bisect` module for sorted lists
- Libraries like `sortedcontainers` provide efficient sorted data structures