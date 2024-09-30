from datetime import datetime
from pydantic import BaseModel, field_validator, ConfigDict


class PostM(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    text: str
    created_at: datetime
    updated_at: datetime


class PostCreateM(BaseModel):
    text: str

    @field_validator('text')
    def text_must_be_at_least_1_char(cls, v):
        if len(v) < 1:
            raise ValueError('Text must be at least 1 character')
        return v