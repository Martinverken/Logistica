from typing import List, Optional
from uuid import UUID
from supabase import Client
from app.models.comment import Comment, CommentCreate
import logging

logger = logging.getLogger(__name__)

class CommentService:
    def __init__(self, db: Client):
        self.db = db
    
    def create_comment(self, comment_data: CommentCreate) -> Optional[Comment]:
        """Crea un comentario"""
        try:
            data = comment_data.model_dump()
            data['order_id'] = str(data['order_id'])
            
            result = self.db.table('comments').insert(data).execute()
            
            if result.data:
                logger.info(f"Comment created for order {comment_data.order_id}")
                return Comment(**result.data[0])
            return None
        except Exception as e:
            logger.error(f"Error creating comment: {e}")
            return None
    
    def get_comments_by_order(self, order_id: UUID) -> List[Comment]:
        """Comentarios de una orden"""
        try:
            result = self.db.table('comments').select('*').eq(
                'order_id', str(order_id)
            ).order('created_at', desc=True).execute()
            
            return [Comment(**c) for c in result.data] if result.data else []
        except Exception as e:
            logger.error(f"Error: {e}")
            return []

