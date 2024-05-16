from util.logger import logger
import uvicorn
from fastapi import FastAPI, APIRouter, Depends, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import block.deposit_api as deposit_api
import block.withdraw_api as withdraw_api
from setting import block_server_port

app = None

app = FastAPI()


origins = ["http://localhost", "http://127.0.0.1", "0.0.0.0", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    raise HTTPException(status_code=500, detail="server error")


@app.get("/")
async def home():
    return "home"


router = APIRouter()
router.include_router(deposit_api.router, prefix="/sdk", tags=["deposit"])
router.include_router(withdraw_api.router, prefix="/sdk", tags=["withdraw"])

app.include_router(router)

logger.info("block server start...")

uvicorn.run(app, host="0.0.0.0", port=block_server_port)
