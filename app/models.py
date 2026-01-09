import os
from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get("COSMOS_MONGO_URI") or os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("COSMOS_DB_NAME") or "styleup"

_client: Optional[MongoClient] = None
_db = None
_use_memory = False
_memory_store = {"users": [], "wardrobe": []}


def connect_db():
	global _client, _db
	global _use_memory
	if not MONGO_URI:
		# Use an in-memory fallback for local/demo runs when no Mongo URI provided
		_use_memory = True
		return

	if _client is None:
		_client = MongoClient(MONGO_URI)
		_db = _client[DB_NAME]


def close_db():
	global _client
	if _client is not None:
		_client.close()


def create_user(user_doc: Dict[str, Any]) -> str:
	if _use_memory:
		# assign a simple numeric id
		new_id = str(len(_memory_store["users"]) + 1)
		doc = user_doc.copy()
		doc["_id"] = new_id
		_memory_store["users"].append(doc)
		return new_id

	users = _db["users"]
	res = users.insert_one(user_doc)
	return str(res.inserted_id)


def get_user(user_id: str) -> Optional[Dict[str, Any]]:
	if _use_memory:
		for d in _memory_store["users"]:
			if str(d.get("_id")) == str(user_id):
				return d
		return None

	users = _db["users"]
	doc = users.find_one({"_id": ObjectId(user_id)})
	if doc:
		doc["_id"] = str(doc["_id"])
	return doc


def add_wardrobe_item(user_id: str, item: Dict[str, Any]) -> str:
	if _use_memory:
		new_id = "w" + str(len(_memory_store["wardrobe"]) + 1)
		item_copy = item.copy()
		item_copy["_id"] = new_id
		item_copy["user_id"] = str(user_id)
		_memory_store["wardrobe"].append(item_copy)
		return new_id

	items = _db["wardrobe"]
	item_copy = item.copy()
	item_copy["user_id"] = ObjectId(user_id)
	res = items.insert_one(item_copy)
	return str(res.inserted_id)


def get_wardrobe_for_user(user_id: str) -> List[Dict[str, Any]]:
	if _use_memory:
		docs = [d.copy() for d in _memory_store["wardrobe"] if str(d.get("user_id")) == str(user_id)]
		return docs

	items = _db["wardrobe"]
	docs = list(items.find({"user_id": ObjectId(user_id)}))
	for d in docs:
		d["_id"] = str(d["_id"])
		d["user_id"] = str(d["user_id"])
	return docs
