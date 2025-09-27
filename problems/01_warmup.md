# Problem 1: String Manipulation - Stock Ticker Parser
**Difficulty**: Easy  
**Time**: 10 minutes  
**Focus**: String processing, error handling, basic data structures

## Problem Statement
You need to parse stock ticker data that comes in as a formatted string representing price changes throughout a trading day.

### Input Format
```
"TICKER:change1,change2,change3,..."
```
Where:
- `TICKER` is the stock symbol (e.g., "AAPL", "GOOGL")
- Each `change` is a price movement (e.g., "+2.5", "-1.2", "+0.8")

### Requirements
Implement a function `parse_stock_data(data_string)` that:

1. **Extracts** the ticker symbol (before the colon)
2. **Parses** all price changes into a list of floats
3. **Calculates** the net change for the day
4. **Returns** a dictionary with the structure:
   ```python
   {
       'ticker': 'AAPL',
       'changes': [2.5, -1.2, 0.8, -0.3, 1.1],
       'net_change': 2.9
   }
   ```

### Test Cases
```python
# Basic case
parse_stock_data("AAPL:+2.5,-1.2,+0.8,-0.3,+1.1")
# Expected: {'ticker': 'AAPL', 'changes': [2.5, -1.2, 0.8, -0.3, 1.1], 'net_change': 2.9}

# No changes
parse_stock_data("MSFT:")
# Expected: {'ticker': 'MSFT', 'changes': [], 'net_change': 0}

# Case sensitivity
parse_stock_data("googl:+5.0,-2.1")
# Expected: {'ticker': 'GOOGL', 'changes': [5.0, -2.1], 'net_change': 2.9}
```

### Error Handling
Your solution should handle:
- Invalid input format (missing colon, empty ticker)
- Invalid price changes (non-numeric values)
- Edge cases (empty string, None input)

### Your Implementation
```python
def parse_stock_data(data_string):
    """
    Parse stock ticker and price changes.
    
    Args:
        data_string (str): Format "TICKER:change1,change2,..."
    
    Returns:
        dict: Contains ticker, changes, and net_change
    
    Raises:
        ValueError: For invalid input format
    """
    # TODO: Implement your solution here
    pass

# Test your solution
if __name__ == "__main__":
    # Add your test cases here
    pass
```

### Discussion Questions
After implementing your solution, be prepared to discuss:

1. **Time/Space Complexity**: What are the complexities of your solution?
2. **Error Handling**: How would you handle malformed input in production?
3. **Scale**: How would you optimize for processing thousands of these strings?
4. **Extensions**: How would you extend this to handle timestamps or additional metadata?

### Hints
- Consider using string methods like `split()` and `strip()`
- Remember to handle the `+` sign in positive numbers
- Think about floating-point precision for financial calculations
- Use meaningful variable names and add comments