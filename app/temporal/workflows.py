


from datetime import timedelta
from temporalio import workflow
from typing import Any, Dict
import re

from app.schemas.workflow_schema import WorkflowPayload, StepNode
from app.temporal.activity_strategy import ActivityStrategy
from app.temporal.wokflow_strategy import WorkflowStrategy
from app.temporal.condition_strategy import ConditionStrategy
from app.temporal.loop_strategy import LoopStrategy
from app.temporal.switch_strategy import SwitchStrategy
from app.validators.payload_validators import WorkflowValidator


@workflow.defn
class GenericWorkflow:

    def __init__(self):
        self.strategies = {
            "activity": ActivityStrategy(),
            "workflow": WorkflowStrategy(),
            "condition": ConditionStrategy(),
            "loop": LoopStrategy(),
            "switch": SwitchStrategy()
        }

    @workflow.run
    async def run(self, payload: WorkflowPayload):
        
        
        context: Dict[str, Any] = {}
        results: Dict[str, Any] = {}
        
        step_map = {step.id: step for step in payload.steps}

        #  Find start node
        current_step = next((s for s in payload.steps if s.isStartNode), None)
        if not current_step:
            raise ValueError("No start node defined")

        while current_step:

            strategy = self.strategies.get(current_step.type)
            if not strategy:
                raise ValueError(f"No strategy for step type {current_step.type}")

            # Global background rule
            run_in_background = (
                payload.allBackgroundRun and
                current_step.type in ["activity", "workflow"]
            )

            if run_in_background:
                

                workflow.start_activity(
                    current_step.name,   
                    self._resolve_inputs(current_step.inputs, context),
                    start_to_close_timeout=timedelta(seconds=30)
                )


                output = current_step.id
                
            else:
                output = await strategy.execute(
                    workflow_ctx=self,
                    step=current_step,
                    context=context,
                    step_map=step_map
                )

                current_step.outputs = output
                context[current_step.id] = output
                results[current_step.id] = output

            # Resolve next step
            current_step = self._get_next_step(
                step=current_step,
                step_map=step_map,
                output=output
            )

        return results
    # ================= NEXT STEP RESOLVER =================
    def _get_next_step(self, step: StepNode, step_map: Dict[str, StepNode], output):

        # CONDITION → output already contains next node id
        if step.type == "condition":
            return step_map.get(output)

        # SWITCH → output already contains next node id
        if step.type == "switch":
            return step_map.get(output)

        # LOOP → continue after loop
        if step.type == "loop":
            return step_map.get(step.nextNodeId)
        
        if step.type == "workflow":
            return step_map.get(step.nextNodeId)

        # ACTIVITY / WORKFLOW
        if step.nextNodeId:
            return step_map.get(step.nextNodeId)

        return None

    # ================= INPUT RESOLVER =================
    def _resolve_inputs(self, inputs: Any, context: dict):
        if not isinstance(inputs, dict):
            return inputs

        resolved = {}
        for key, value in inputs.items():
            if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                expr = value.strip("{}")
                parts = expr.split(".")

                if len(parts) == 2:
                    step_name, field = parts
                    step_output = context.get(step_name)
                    if isinstance(step_output, dict):
                        resolved[key] = step_output.get(field)
                    else:
                        resolved[key] = None
                else:
                    resolved[key] = context.get(parts[0])
            else:
                resolved[key] = value

        return resolved

    # ================= CONDITION RESOLVER =================
    def _resolve_condition(self, condition: str, context: dict) -> str:
        def replacer(match):
            expr = match.group(1).strip()
            parts = expr.split(".")

            if len(parts) == 2:
                step_name, field = parts
                step_output = context.get(step_name)
                if isinstance(step_output, dict):
                    return repr(step_output.get(field))
            return repr(context.get(expr))

        return re.sub(r"\{\{([^}]+)\}\}", replacer, condition)




    
    
