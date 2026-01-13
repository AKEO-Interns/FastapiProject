

from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Literal


# -----------------------------
# CONDITION NODE CONFIG
# -----------------------------
class ConditionConfig(BaseModel):
    expression: str          
    on_true: str             
    on_false: str           


# -----------------------------
# LOOP NODE CONFIG
# -----------------------------
class LoopConfig(BaseModel):
    iterator: str            
    start: int
    end: int
    step: int = 1
    activity_node_id: str    # Node ID to execute inside the loop


# -----------------------------
# SWITCH NODE CONFIG
# -----------------------------
class SwitchCase(BaseModel):
    condition: Optional[str] = None
    is_default: bool = False
    next_node_id: str


class SwitchConfig(BaseModel):
    item: str                       
    cases: List[SwitchCase]


# -----------------------------
# STEP NODE (MAIN UNIT)
# -----------------------------
class StepNode(BaseModel):
    id: str
    nextNodeId: str
    isStartNode: bool = False
    name: str
    type: Literal["activity", "workflow", "condition", "loop", "switch"] = "activity"
    inputs: Dict[str, Any] = {}
    outputs: Dict[str, Any] = {}
    background: bool = False

    # Node-specific configs
    condition: Optional[ConditionConfig] = None
    loop: Optional[LoopConfig] = None
    switch: Optional[SwitchConfig] = None


# -----------------------------
# WORKFLOW PAYLOAD
# -----------------------------
class WorkflowPayload(BaseModel):
    allBackgroundRun: bool = False
    steps: List[StepNode]

    # background




