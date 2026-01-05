from pydantic import BaseModel


class Inquiry(BaseModel):
    """Inquiries schema."""

    __modelname__ = "inquiries"

    _item: str = "inquiries"
    id: int | None = None
    info: str
    initiator: str
    origins: str | None = ""


print(Inquiry(_item="inquiries", info="test", initiator="test"))
