from typing import Any, Optional
from pydantic import BaseModel


class APIResponse(BaseModel):
    code: int = 0
    data: Any = None
    message: str = "ok"


class PaginatedData(BaseModel):
    items: list[Any]
    total: int
    page: int
    page_size: int
