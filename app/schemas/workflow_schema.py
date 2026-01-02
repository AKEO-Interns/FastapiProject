from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Literal

class StepNode(BaseModel):
    name: str
    type: Literal["activity", "workflow"] = "activity"
    inputs: Dict[str, Any] | Any
    background: Optional[bool] = False

class WorkflowPayload(BaseModel):
    steps: List[StepNode]

