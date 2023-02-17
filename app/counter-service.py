import os
import aioredis
import uvicorn
from fastapi import FastAPI

app = FastAPI()

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))

redis_client = None


@app.on_event("startup")
async def startup_event():
    global redis_client
    redis_client = await aioredis.from_url(f"redis://{redis_host}:{redis_port}", encoding="utf-8", decode_responses=True)


@app.on_event("shutdown")
async def shutdown_event():
    global redis_client
    redis_client.close()
    await redis_client.wait_closed()


@app.post("/")
async def increment_counter():
    await redis_client.incr("counter")
    return {"message": "Counter incremented"}


@app.get("/")
async def get_counter():
    counter = await redis_client.get("counter")
    if counter is None:
        return {"message": "Counter not found"}
    else:
        return {"counter": int(counter)}


# if __name__ == "__main__":
#     uvicorn.run("counter-service:app", host="0.0.0.0", port=8000, reload=True)
