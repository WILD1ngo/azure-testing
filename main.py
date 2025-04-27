import time
import uvicorn
import redis
from fastapi import FastAPI

app = FastAPI()
cache = redis.Redis(host='redis', port=6379)


def get_hit_count() -> int:
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.get('/')
def hello() -> str:
    count = get_hit_count()
    return f'Hello World! I have been seen {count*10000000} times.\n'


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
