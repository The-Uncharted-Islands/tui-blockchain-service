from fastapi import APIRouter, Depends, Request, HTTPException
from util.logger import logger
import json
import hashlib
import util.response_util as response_util
import requests
from setting import block_server_apikey

router = APIRouter()

eventIds = []


@router.get("/withdraw")
def withdraw(
    eventId: int,
    account: str,
    typeId: int,
    itemId: int,
    tokenId: int,
    amount: int,
    apikey: str,
):
    logger.info(f"withdraw {eventId} {account} {typeId} {itemId} {tokenId} {amount}")

    if apikey != block_server_apikey:
        return response_util.fail()

    if eventId in eventIds:
        return response_util.success()


    return response_util.success()


@router.get("/getWithdrawResult")
def getWithdrawResult(eventId: int, apikey: str):
    logger.info(f"getWithdrawResult {eventId}{apikey}")

    if apikey != block_server_apikey:
        return response_util.fail()

    return response_util.success()

