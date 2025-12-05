import redis

redis_client = redis.Redis(host='10.91.10.19', port=6379, decode_responses=True)
print('connection redis', redis_client.ping())