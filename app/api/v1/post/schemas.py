from datetime import datetime
from pydantic import BaseModel, Field


class PostM(BaseModel):
    id: int = Field(..., description="Post ID")
    user_id: int = Field(..., description="Author ID")
    text: str = Field(..., min_length=1, description="Content of the post")
    created_at: datetime = Field(..., description="Post creation time")
    updated_at: datetime = Field(..., description="Post update time")

    class Config:
        from_attributes = True
        orm_mode = True


# This model is used to update a post also.
# Best practice is to use it in combination with PostCreateM
class PostCreateM(BaseModel):
    text: str = Field(min_length=1)
