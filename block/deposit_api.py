from fastapi import APIRouter, Depends, Request, HTTPException
from util.logger import logger
import json
import hashlib
import util.response_util as response_util
import requests
from setting import game_server_api

router = APIRouter()


@router.get("/deposit_mock")
def deposit_mock(account: str, typeId: int, itemId: int, tokenId: int, amount: int):
    logger.info(f"deposit_mock {account} {typeId} {itemId} {tokenId} {amount}")

    url = f"{game_server_api}/deposit"
    # response = requests.get(url, headers=headers)
    response = requests.get(url)
    result = response.json()
    logger.info(result)

    return response_util.success()
