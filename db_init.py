from common.database import SessionLocal
from nft.record_model import RecordModel
from nft.reward_model import RewardModel


import common.database as database

import json


def create_all():
    database.init_db()
    database.create_all()
    print("create all")


if __name__ == "__main__":
    create_all()
