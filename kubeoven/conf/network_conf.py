from pydantic import BaseModel, Field


class NetworkConf(BaseModel):
    plugin: str = Field(default="flannel")


