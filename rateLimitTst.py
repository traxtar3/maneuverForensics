from ratelimiter import RateLimiter

rate_limiter = RateLimiter(max_calls=1, period=5)

for i in range(100):
    with rate_limiter:
        print(i)
