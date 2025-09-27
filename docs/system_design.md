# System Design Discussion - Bloomberg Financial Systems
**Duration**: 15 minutes  
**Focus**: Architecture, scalability, real-world considerations

## Overview
This section focuses on system design principles relevant to Bloomberg's financial technology infrastructure. We'll discuss how to scale the solutions from the previous problems and design production-ready financial systems.

## Discussion Topics

### 1. Market Data Processing System (25 minutes)
Based on Problem 2 (Market Data Processor), discuss designing a system that can handle real-time market data for all global exchanges.

#### Requirements
- **Scale**: Process 1M+ price updates per second
- **Latency**: Sub-millisecond response times for queries  
- **Reliability**: 99.99% uptime during trading hours
- **Global**: Support multiple exchanges across time zones
- **Historical**: Store years of historical data

#### Discussion Points
1. **Architecture Design**
   - How would you distribute the system across multiple servers?
   - What role would caching play in your design?
   - How would you handle data partitioning?

2. **Data Storage**
   - What database technologies would you choose and why?
   - How would you optimize for both real-time queries and historical analysis?
   - What about data compression and archival strategies?

3. **Performance Optimization**
   - How would you achieve sub-millisecond latencies?
   - What caching strategies would you implement?
   - How would you handle memory constraints?

4. **Fault Tolerance**
   - How would you ensure high availability?
   - What happens if a data center goes down?
   - How would you handle partial system failures?

#### Sample Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Feeds    │    │   Data Feeds    │    │   Data Feeds    │
│   (NYSE, LSE)   │    │   (NASDAQ)      │    │   (TSE, ASX)    │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Message Bus (Kafka)                         │
└─────────┬───────────────────────────────┬─────────────────────┘
          │                               │
          ▼                               ▼
┌─────────────────┐              ┌─────────────────┐
│  Stream         │              │  Stream         │
│  Processor      │              │  Processor      │
│  (Real-time)    │              │  (Analytics)    │
└─────────┬───────┘              └─────────┬───────┘
          │                               │
          ▼                               ▼
┌─────────────────┐              ┌─────────────────┐
│   Hot Storage   │              │  Cold Storage   │
│   (Redis)       │              │  (ClickHouse)   │
└─────────────────┘              └─────────────────┘
```

### 2. Portfolio Risk Management System (20 minutes)
Based on Problem 3 (Portfolio Risk Calculator), discuss scaling to handle thousands of portfolios.

#### Requirements
- **Scale**: Support 10,000+ portfolios with 1,000+ positions each
- **Real-time**: Risk calculations updated every second
- **Compliance**: Audit trails and regulatory reporting
- **Integration**: Connect with trading systems and data feeds

#### Discussion Points
1. **Microservices Architecture**
   - How would you decompose the system into services?
   - What are the boundaries between portfolio management, risk calculation, and reporting?

2. **Data Consistency**
   - How do you ensure portfolio data stays consistent across services?
   - What happens when a trade executes while risk is being calculated?

3. **Performance at Scale**
   - How would you optimize matrix calculations for large portfolios?
   - What caching strategies would help with correlation matrices?
   - When would you use approximation algorithms vs exact calculations?

4. **Regulatory Compliance**
   - How would you implement audit trails?
   - What data retention policies would you need?
   - How would you handle different regulatory requirements across regions?

#### Sample Service Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Trading       │    │   Market Data   │    │   Reference     │
│   System        │    │   Service       │    │   Data Service  │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Event Bus                                    │
└─────────┬───────────────────────────────────────────┬─────────┘
          │                                           │
          ▼                                           ▼
┌─────────────────┐                         ┌─────────────────┐
│   Portfolio     │                         │   Risk Engine   │
│   Management    │◄────────────────────────┤   Service       │
└─────────┬───────┘                         └─────────┬───────┘
          │                                           │
          ▼                                           ▼
┌─────────────────┐                         ┌─────────────────┐
│   Compliance    │                         │   Reporting     │
│   Service       │                         │   Service       │
└─────────────────┘                         └─────────────────┘
```

### 3. Technology Stack Decisions

#### Database Technologies
- **Time-series databases**: InfluxDB, TimescaleDB for market data
- **In-memory databases**: Redis, Hazelcast for low-latency access
- **Analytical databases**: ClickHouse, Snowflake for historical analysis
- **Traditional databases**: PostgreSQL for transactional data

#### Message Brokers
- **Apache Kafka**: High-throughput, fault-tolerant streaming
- **Redis Streams**: Low-latency pub/sub
- **RabbitMQ**: Reliable message delivery with complex routing

#### Programming Languages
- **Python**: Rapid development, extensive libraries for finance
- **C++**: Ultra-low latency, high-performance computing
- **Java**: Enterprise integration, mature ecosystem
- **Go**: Concurrent processing, microservices

### 4. Common Design Patterns

#### Circuit Breaker Pattern
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
            raise e
```

#### Cache-Aside Pattern
```python
def get_portfolio_risk(portfolio_id):
    # Try cache first
    cache_key = f"risk:{portfolio_id}"
    cached_risk = redis_client.get(cache_key)
    
    if cached_risk:
        return json.loads(cached_risk)
    
    # Calculate risk if not in cache
    risk_data = calculate_portfolio_risk(portfolio_id)
    
    # Store in cache with TTL
    redis_client.setex(cache_key, 300, json.dumps(risk_data))  # 5 min TTL
    
    return risk_data
```

### 5. Monitoring and Observability

#### Key Metrics
- **Latency percentiles**: P50, P95, P99 response times
- **Throughput**: Messages/queries per second
- **Error rates**: Failed requests, timeouts
- **Resource utilization**: CPU, memory, disk I/O

#### Alerting Strategy
```yaml
# Example alerting rules
alerts:
  - name: HighLatency
    condition: avg_response_time > 10ms
    severity: warning
    
  - name: HighErrorRate  
    condition: error_rate > 1%
    severity: critical
    
  - name: DataFeedDown
    condition: messages_received == 0 for 30s
    severity: critical
```

## Questions for Candidate

### Architecture Questions
1. **Design Trade-offs**: How would you choose between consistency and availability in a financial system?
2. **Data Modeling**: How would you model complex financial instruments in your database?
3. **API Design**: How would you design APIs for both real-time and batch processing?

### Scalability Questions  
1. **Horizontal Scaling**: How would you partition portfolio data across multiple servers?
2. **Load Balancing**: What load balancing strategies work best for stateful financial services?
3. **Caching**: When would you use different caching strategies (write-through, write-back, etc.)?

### Reliability Questions
1. **Disaster Recovery**: How would you design for cross-region failover?
2. **Data Integrity**: How do you ensure data consistency during system failures?
3. **Testing**: How would you test a system that processes live market data?

### Performance Questions
1. **Low Latency**: What techniques would you use to achieve microsecond latencies?
2. **Memory Management**: How would you optimize memory usage for large datasets?
3. **I/O Optimization**: How would you minimize disk I/O for frequently accessed data?

## Evaluation Criteria

### Technical Depth
- [ ] Understanding of distributed systems concepts
- [ ] Knowledge of database technologies and trade-offs
- [ ] Awareness of performance optimization techniques
- [ ] Understanding of fault tolerance patterns

### Practical Experience
- [ ] Can discuss real-world trade-offs and decisions
- [ ] Understands operational concerns (monitoring, deployment)
- [ ] Considers security and compliance requirements
- [ ] Thinks about maintainability and evolution

### Communication
- [ ] Can explain complex concepts clearly
- [ ] Asks clarifying questions about requirements
- [ ] Discusses multiple solution approaches
- [ ] Acknowledges limitations and trade-offs

### Bloomberg-Specific Knowledge
- [ ] Understanding of financial markets and trading
- [ ] Awareness of regulatory requirements
- [ ] Knowledge of real-time systems constraints
- [ ] Appreciation for data quality and accuracy