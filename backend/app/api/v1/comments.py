from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.services.comment_service import CommentService
from app.models.comment import Comment, CommentCreate

router = APIRouter()

def get_comment_service(db=Depends(get_db)):
    return CommentService(db)

@router.post("/", response_model=Comment, status_code=201)
async def create_comment(
    comment: CommentCreate,
    service: CommentService = Depends(get_comment_service)
):
    """Crea un comentario en una orden"""
    created_comment = service.create_comment(comment)
    if not created_comment:
        raise HTTPException(status_code=400, detail="Could not create comment")
    return created_comment

@router.get("/order/{order_id}", response_model=List[Comment])
async def get_comments_by_order(
    order_id: UUID,
    service: CommentService = Depends(get_comment_service)
):
    """Obtiene todos los comentarios de una orden"""
    return service.get_comments_by_order(order_id)