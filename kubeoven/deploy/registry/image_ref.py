from pydantic import BaseModel, Field

class ImageRef(BaseModel):
    name: str = Field(default="")

    registry: str = Field(default="")

    @classmethod
    def of(cls, ref: str):
        registry = "docker.io"
        pieces = ref.split('/', 1)
        if len(pieces) == 1:
            name = pieces[0]
        if len(pieces) > 1:
            if pieces[0].find('.') > 0 or pieces[0].find(':') > 0:
                registry = pieces[0]
                name = pieces[1]
            else:
                name = "/".join(pieces)
        return cls(name=name, registry=registry)
    def __str__(self) -> str:
        return self.registry + "/" + self.name
    