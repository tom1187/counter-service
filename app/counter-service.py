import os
import logging
import aioredis
import uvicorn
from fastapi import FastAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

app = FastAPI()

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))

redis_client = None


@app.on_event("startup")
async def startup_event():
    global redis_client
    logging.info(f"Connecting to Redis server at {redis_host}:{redis_port}")
    redis_client = await aioredis.from_url(f"redis://{redis_host}:{redis_port}", encoding="utf-8", decode_responses=True)
    logging.info("Connected to Redis server")


@app.on_event("shutdown")
async def shutdown_event():
    global redis_client
    logging.info("Disconnecting from Redis server")
    redis_client.close()
    await redis_client.wait_closed()
    logging.info("Disconnected from Redis server")


@app.post("/")
async def increment_counter():
    await redis_client.incr("counter")
    logging.info("Counter incremented")
    return {"message": "Counter incremented"}


@app.get("/")
async def get_counter():
    counter = await redis_client.get("counter")
    if counter is None:
        logging.warning("Counter not found")
        return {"message": "Counter not found"}
    else:
        counter_value = int(counter)
        logging.info(f"Counter value is {counter_value}")
        return {"counter": counter_value}

# if __name__ == "__main__":
#     uvicorn.run("counter-service:app", host="0.0.0.0", port=8000, reload=True)