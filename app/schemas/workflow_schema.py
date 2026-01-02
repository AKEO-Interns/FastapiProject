from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class ActivityNode(BaseModel):
    name: str
    inputs: Dict[str, Any] | Any
    background: Optional[bool] = False

class ActivityResult(BaseModel):
    name: str
    output: Dict[str, Any] | Any

class WorkflowPayload(BaseModel):
    steps: List[ActivityNode]

class WorkflowResult(BaseModel):
    results: Dict[str, Any]

