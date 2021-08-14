from typing import Optional
from pydantic.main import BaseModel

class NodeStatus(BaseModel):
    address: str
    name: str
    status: bool
    online_ratio: Optional[float]
    ip: str
    version: str
    block_height: int
