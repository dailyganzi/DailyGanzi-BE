import uuid
from pydantic import BaseModel, Field, SecretStr
from pydantic.networks import EmailStr


class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4)
    name: str
    email: EmailStr = Field(unique=True, index=True)
    password: SecretStr

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Nana",
                "email": "nana@gmail.com",
                "password": "nana1234"
            }
        }