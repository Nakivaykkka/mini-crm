from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

import time
from sqlalchemy.exc import OperationalError

from app.database import engine, Base
from app.models import user, client
from app.routers import client , auth 


MAX_RETRIES = 10

app = FastAPI(
    title="Mini_CRM",
    description="Production-ready FastAPI backend",
    version="1.0.0",
)

# Middleware: CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Swagger Authorize + Token
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Роуты
app.include_router(auth.router)
app.include_router(client.router)


for i in range(MAX_RETRIES):
    try:
        print(f"🔌 Attempting DB connection ({i+1}/{MAX_RETRIES})...")
        Base.metadata.create_all(bind=engine)
        print("Database initialized.")
        break
    except OperationalError:
        print(f"DB not ready yet, retrying in 2s...")
        time.sleep(2)

@app.get("/")
def root():
    return {"msg": "API is alive"}

# Run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    
    
    
    
    
    
    
    
    
    
    
    
