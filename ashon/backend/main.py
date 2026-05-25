import os
from dotenv import load_dotenv

# Load env variables early
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import connect_to_mongo, close_mongo_connection
from routes.products import router as products_router
from routes.reviews import router as reviews_router
from routes.image_search import router as image_search_router

app = FastAPI(title="Product Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev, allow all. In prod, restrict.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo(app)

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection(app)

app.include_router(products_router, prefix="/api/products", tags=["products"])
app.include_router(reviews_router, prefix="/api", tags=["reviews"])
app.include_router(image_search_router, prefix="/api/images", tags=["images"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Product Portal API"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
