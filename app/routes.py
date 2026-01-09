from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from app import models
from app import recommender
from app import chatbot

router = APIRouter()


class UserCreate(BaseModel):
	name: str
	height_cm: Optional[int] = None
	body_type: Optional[str] = None
	style: Optional[str] = None
	favorite_colors: Optional[List[str]] = []


class WardrobeItemCreate(BaseModel):
	category: str
	color: str
	occasion: str
	comfort: int = Field(..., ge=1, le=10)
	tags: Optional[str] = ""


class RecommendRequest(BaseModel):
	user_id: str
	occasion: str


class ChatRequest(BaseModel):
	user_id: str
	outfit: Any


@router.post("/register")
def register(user: UserCreate):
	user_doc = user.dict()
	user_id = models.create_user(user_doc)
	return {"user_id": user_id}


@router.post("/add-wardrobe")
def add_wardrobe_item(user_id: str, item: WardrobeItemCreate):
	# basic validation of user
	u = models.get_user(user_id)
	if not u:
		raise HTTPException(status_code=404, detail="User not found")
	item_id = models.add_wardrobe_item(user_id, item.dict())
	return {"item_id": item_id}


@router.post("/recommend-outfit")
def recommend_outfit(req: RecommendRequest):
	user = models.get_user(req.user_id)
	if not user:
		raise HTTPException(status_code=404, detail="User not found")

	wardrobe = models.get_wardrobe_for_user(req.user_id)
	recs = recommender.get_recommendations(user, wardrobe, req.occasion)
	return {"recommendations": recs}


@router.post("/chat-styleup")
def chat_styleup(req: ChatRequest):
	user = models.get_user(req.user_id)
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	explanation = chatbot.explain_outfit(req.outfit, user)
	return {"explanation": explanation}
