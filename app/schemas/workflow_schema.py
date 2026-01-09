# from pydantic import BaseModel
# from typing import Any, Dict, List, Optional, Literal

# class StepNode(BaseModel):
#     name: str
#     type: Literal["activity", "workflow", "condition", "loop", "switch"] = "activity"
#     inputs: Dict[str, Any] | Any = {}
#     outputs:Dict [str, Any] | Any = {}
#     background: Optional[bool] = False
#     condition: Optional[str] = None            # for condition nodes
#     loop_over: Optional[List[Any]] = None      # for loop nodes
#     steps: Optional[List["StepNode"]] = None   # child steps
#     switch_on: Optional[str] = None            # for switch nodes
#     cases: Optional[Dict[str, List["StepNode"]]] = None  # switch cases

# class WorkflowPayload(BaseModel):
#     steps: List[StepNode]

from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Literal


# -----------------------------
# CONDITION NODE CONFIG
# -----------------------------
class ConditionConfig(BaseModel):
    expression: str          # e.g. "{{checkInventory.available}} == True"
    on_true: str             # next node id
    on_false: str            # next node id


# -----------------------------
# LOOP NODE CONFIG
# -----------------------------
class LoopConfig(BaseModel):
    iterator: str            # e.g. "i"
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
    item: str                       # e.g. "{{checkInventory.book_id}}"
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
    steps: List[StepNode]




