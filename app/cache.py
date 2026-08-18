import redis
import os
import hashlib
import json
r=redis.Redis(host=os.getenv("REDIS_HOST","localhost"), port=6379, decode_responses=True)

# Create Unique identifier of user's question
def get_cache_key(question):
    text=question.strip().lower()
    hashval=hashlib.md5(text.encode()).hexdigest()
    return hashval



# Check if value is in the Redis using get_cache_key()
def get_cached_response(question):
    key=get_cache_key(question) #took unique identifier
    cached=r.get(key)
    if cached is not None:
       j=json.loads(cached)
       return j
    return None


def set_cached_response(question,answer):
    key=get_cache_key(question)
    j=json.dumps(answer)# Creates string from dictionary
    r.setex(key,3600,j)
    
    




