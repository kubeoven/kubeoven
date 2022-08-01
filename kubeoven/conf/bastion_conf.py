import os
from typing import Optional
from pydantic import BaseModel, Field

class BastionConf(BaseModel):
    address: str
    ssh_key_path: Optional[str] = Field()
    port: int = Field(default=22)
    user: str = Field(default=os.getenv('USER') or '')
