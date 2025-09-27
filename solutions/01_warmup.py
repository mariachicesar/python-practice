# Solution: Stock Ticker Parser
# Bloomberg Python Technical Interview - Problem 1

def parse_stock_data(data_string):
    """
    Parse stock ticker and price changes.
    
    Args:
        data_string (str): Format "TICKER:change1,change2,..."
    
    Returns:
        dict: Contains ticker, changes, and net_change
    
    Time Complexity: O(n) where n is the length of the string
    Space Complexity: O(k) where k is the number of changes
    
    Raises:
        ValueError: For invalid input format
    """
    # Input validation
    if not data_string or ':' not in data_string:
        raise ValueError("Invalid input format: expected 'TICKER:changes'")
    
    # Split ticker and changes
    ticker, changes_str = data_string.split(':', 1)
    
    if not ticker.strip():
        raise ValueError("Ticker symbol cannot be empty")
    
    # Parse changes
    changes = []
    if changes_str.strip():  # Only process if there are changes
        for change_str in changes_str.split(','):
            change_str = change_str.strip()
            if not change_str:
                continue  # Skip empty strings
            try:
                # Handle explicit + sign
                change = float(change_str)
                changes.append(change)
            except ValueError:
                raise ValueError(f"Invalid price change: '{change_str}'")
    
    # Calculate net change
    net_change = sum(changes)
    
    return {
        'ticker': ticker.upper().strip(),
        'changes': changes,
        'net_change': round(net_change, 2)  # Round to 2 decimal places for financial precision
    }


# Enhanced version with additional features
def parse_stock_data_enhanced(data_string, validate_ticker=True):
    """
    Enhanced version with additional validation and features.
    
    Args:
        data_string (str): Format "TICKER:change1,change2,..."
        validate_ticker (bool): Whether to validate ticker format
    
    Returns:
        dict: Contains ticker, changes, net_change, and additional metrics
    """
    import re
    
    # Basic parsing
    result = parse_stock_data(data_string)
    
    # Additional ticker validation
    if validate_ticker:
        ticker_pattern = r'^[A-Z]{1,5}$'  # 1-5 uppercase letters
        if not re.match(ticker_pattern, result['ticker']):
            raise ValueError(f"Invalid ticker format: {result['ticker']}")
    
    # Additional metrics
    changes = result['changes']
    if changes:
        result['max_change'] = max(changes)
        result['min_change'] = min(changes)
        result['volatility'] = sum(abs(change) for change in changes) / len(changes)
        result['num_changes'] = len(changes)
    else:
        result['max_change'] = 0
        result['min_change'] = 0
        result['volatility'] = 0
        result['num_changes'] = 0
    
    return result


# Performance-optimized version for batch processing
def parse_multiple_stock_data(data_strings):
    """
    Parse multiple stock data strings efficiently.
    
    Args:
        data_strings (list): List of stock data strings
    
    Returns:
        list: List of parsed stock data dictionaries
    """
    results = []
    errors = []
    
    for i, data_string in enumerate(data_strings):
        try:
            result = parse_stock_data(data_string)
            results.append(result)
        except ValueError as e:
            errors.append({'index': i, 'data': data_string, 'error': str(e)})
    
    return {
        'results': results,
        'errors': errors,
        'success_rate': len(results) / len(data_strings) if data_strings else 0
    }


# Test suite
def test_parse_stock_data():
    """Comprehensive test suite for the stock data parser."""
    
    # Test basic functionality
    result1 = parse_stock_data("AAPL:+2.5,-1.2,+0.8,-0.3,+1.1")
    assert result1['ticker'] == 'AAPL'
    assert result1['changes'] == [2.5, -1.2, 0.8, -0.3, 1.1]
    assert abs(result1['net_change'] - 2.9) < 0.01
    
    # Test no changes
    result2 = parse_stock_data("MSFT:")
    assert result2['ticker'] == 'MSFT'
    assert result2['changes'] == []
    assert result2['net_change'] == 0
    
    # Test case sensitivity
    result3 = parse_stock_data("googl:+5.0,-2.1")
    assert result3['ticker'] == 'GOOGL'
    assert abs(result3['net_change'] - 2.9) < 0.01
    
    # Test whitespace handling
    result4 = parse_stock_data(" TSLA : +1.0 , -0.5 , +2.0 ")
    assert result4['ticker'] == 'TSLA'
    assert result4['changes'] == [1.0, -0.5, 2.0]
    
    # Test single change
    result5 = parse_stock_data("META:+3.75")
    assert result5['ticker'] == 'META'
    assert result5['changes'] == [3.75]
    assert result5['net_change'] == 3.75
    
    # Test negative numbers without explicit sign
    result6 = parse_stock_data("NVDA:1.5,-2.0,0.5")
    assert result6['changes'] == [1.5, -2.0, 0.5]
    assert result6['net_change'] == 0.0
    
    print("✅ All basic tests passed!")


def test_error_handling():
    """Test error handling cases."""
    
    # Test invalid format - no colon
    try:
        parse_stock_data("AAPL+1.0,-2.0")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Invalid input format" in str(e)
    
    # Test empty input
    try:
        parse_stock_data("")
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    # Test None input
    try:
        parse_stock_data(None)
        assert False, "Should raise ValueError"
    except (ValueError, AttributeError):
        pass
    
    # Test empty ticker
    try:
        parse_stock_data(":+1.0,-2.0")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "empty" in str(e).lower()
    
    # Test invalid price change
    try:
        parse_stock_data("AAPL:+1.0,invalid,-2.0")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Invalid price change" in str(e)
    
    # Test multiple colons
    result = parse_stock_data("AAPL:TIME:+1.0,-2.0")  # Should take everything after first colon
    assert result['ticker'] == 'AAPL'
    # This might fail depending on implementation - could be extended to handle this case
    
    print("✅ All error handling tests passed!")


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    
    # Test very small numbers
    result1 = parse_stock_data("AAPL:+0.01,-0.01")
    assert result1['net_change'] == 0.0
    
    # Test large numbers
    result2 = parse_stock_data("BRK.A:+1000.50,-999.75")  # Note: dots in ticker might not be valid
    assert abs(result2['net_change'] - 0.75) < 0.01
    
    # Test many decimal places
    result3 = parse_stock_data("AAPL:+1.123456,-0.123456")
    assert abs(result3['net_change'] - 1.0) < 0.01
    
    # Test zero changes
    result4 = parse_stock_data("AAPL:0.0,0.0,0.0")
    assert result4['net_change'] == 0.0
    
    # Test scientific notation (if supported)
    try:
        result5 = parse_stock_data("AAPL:1e-2,-2e-2")
        assert abs(result5['net_change'] - (-0.01)) < 0.001
    except ValueError:
        # Scientific notation might not be supported, that's okay
        pass
    
    print("✅ All edge case tests passed!")


def benchmark_performance():
    """Benchmark the performance of the parser."""
    import time
    
    # Generate test data
    test_data = [f"STOCK{i}:+{i}.0,-{i/2}.0,+{i/4}.0" for i in range(1, 1001)]
    
    # Benchmark single parsing
    start_time = time.time()
    for data in test_data:
        parse_stock_data(data)
    single_time = time.time() - start_time
    
    # Benchmark batch parsing
    start_time = time.time()
    parse_multiple_stock_data(test_data)
    batch_time = time.time() - start_time
    
    print(f"📊 Performance Benchmark:")
    print(f"   Single parsing (1000 items): {single_time:.4f}s")
    print(f"   Batch parsing (1000 items): {batch_time:.4f}s")
    print(f"   Average per item: {single_time/1000*1000:.4f}ms")


if __name__ == "__main__":
    print("🧪 Testing Stock Data Parser")
    print("=" * 40)
    
    test_parse_stock_data()
    test_error_handling()
    test_edge_cases()
    benchmark_performance()
    
    print("\n✅ All tests completed successfully!")
    
    # Demo usage
    print("\n📈 Demo Usage:")
    examples = [
        "AAPL:+2.5,-1.2,+0.8,-0.3,+1.1",
        "GOOGL:+15.0,-8.5,+3.2",
        "MSFT:",
        "tsla:+5.0,-2.1,+1.8,-0.5"
    ]
    
    for example in examples:
        try:
            result = parse_stock_data(example)
            print(f"Input:  {example}")
            print(f"Output: {result}")
            print()
        except ValueError as e:
            print(f"Input:  {example}")
            print(f"Error:  {e}")
            print()