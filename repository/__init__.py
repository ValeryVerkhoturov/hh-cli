from tinydb import Query

from db import db
from model.client import Client


class ClientRepository:
    @staticmethod
    def upsert(client: Client):
        query = Query()
        db.table("client").upsert(document=client.model_dump(), cond=query["id"] == 1)