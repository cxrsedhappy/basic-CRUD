from pydantic import BaseModel, field_validator


class PostModel(BaseModel):
    text: str

    @field_validator('text')
    def text_must_be_at_least_1_char(cls, v):
        if len(v) < 1:
            raise ValueError('Text must be at least 1 character')
        return v