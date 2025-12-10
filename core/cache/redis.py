import redis

print('redis is connecting... ')
redis_client = redis.Redis(host='192.168.1.6', port=6379, decode_responses=True)
print('connection redis', redis_client.ping())