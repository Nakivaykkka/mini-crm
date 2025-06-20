from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, HTTPBearer


from app.client.routes import router as client_router
from app.user.routes import router as user_router
from app.deal.routes import router as deal_router


app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")
bearer_scheme = HTTPBearer()

app.include_router(client_router)
app.include_router(user_router)
app.include_router(deal_router)

@app.get("/")
def root():
    return {"message": "Hello from Docker!"}