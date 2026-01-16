import re
from typing import Set, Any, Dict
from pydantic import BaseModel

from app.schemas.workflow_schema import ConditionConfig, LoopConfig, SwitchCase, SwitchConfig, WorkflowPayload

# Assuming these are already defined
# from your code
# StepNode, WorkflowPayload, ConditionConfig, LoopConfig, SwitchConfig, SwitchCase

class WorkflowValidator:
    @staticmethod
    def pre_validate(payload: WorkflowPayload):
        errors = []

        # --- 1. Validate workflow-level fields ---
        if not isinstance(payload.allBackgroundRun, bool):
            errors.append(f"Payload field 'allBackgroundRun' must be bool")
        if not isinstance(payload.steps, list) or len(payload.steps) == 0:
            errors.append(f"Payload field 'steps' must be a non-empty list")
            return False  # cannot continue without steps

        # Collect all step IDs
        step_ids: Set[str] = set()
        for step in payload.steps:
            # --- 2. Validate StepNode base fields ---
            if not isinstance(step.id, str) or not step.id:
                errors.append(f"Step has invalid 'id': {step.id}")
            if not isinstance(step.name, str) or not step.name:
                errors.append(f"Step '{step.id}' has invalid 'name'")
            if not isinstance(step.type, str) or step.type not in ["activity", "workflow", "condition", "loop", "switch"]:
                errors.append(f"Step '{step.id}' has invalid type '{step.type}'")
            if not isinstance(step.nextNodeId, str):
                errors.append(f"Step '{step.id}' nextNodeId must be string")
            if not isinstance(step.isStartNode, bool):
                errors.append(f"Step '{step.id}' isStartNode must be bool")
            if not isinstance(step.inputs, dict):
                errors.append(f"Step '{step.id}' inputs must be dict")
            if not isinstance(step.outputs, dict):
                errors.append(f"Step '{step.id}' outputs must be dict")
            if not isinstance(step.background, bool):
                errors.append(f"Step '{step.id}' background must be bool")

            # --- 3. Unique step IDs ---
            if step.id in step_ids:
                errors.append(f"Duplicate step ID found: {step.id}")
            step_ids.add(step.id)

            # --- 4. Start Node Rule: inputs must be constants ---
            if step.isStartNode:
                for key, value in step.inputs.items():
                    if isinstance(value, str) and re.search(r"\{\{.*\}\}", value):
                        errors.append(
                            f"Step '{step.id}' is a start node, input '{key}' must be constant (cannot reference other node outputs)"
                        )

            # --- 5. Node-type specific validations ---
            if step.type == "condition":
                if not step.condition or not isinstance(step.condition, ConditionConfig):
                    errors.append(f"Step '{step.id}' must have a valid ConditionConfig")
                else:
                    if not isinstance(step.condition.expression, str) or not step.condition.expression:
                        errors.append(f"Step '{step.id}' condition.expression must be a non-empty string")
                    if not isinstance(step.condition.on_true, str):
                        errors.append(f"Step '{step.id}' condition.on_true must be string")
                    if not isinstance(step.condition.on_false, str):
                        errors.append(f"Step '{step.id}' condition.on_false must be string")

            if step.type == "loop":
                if not step.loop or not isinstance(step.loop, LoopConfig):
                    errors.append(f"Step '{step.id}' must have a valid LoopConfig")
                else:
                    if not isinstance(step.loop.iterator, str):
                        errors.append(f"Step '{step.id}' loop.iterator must be string")
                    for x in [step.loop.start, step.loop.end, step.loop.step]:
                        if not isinstance(x, int):
                            errors.append(f"Step '{step.id}' loop start/end/step must be integer")
                    if step.loop.start > step.loop.end:
                        errors.append(f"Step '{step.id}' loop start > end")
                    if step.loop.step <= 0:
                        errors.append(f"Step '{step.id}' loop step must be > 0")
                    if not isinstance(step.loop.activity_node_id, str):
                        errors.append(f"Step '{step.id}' loop activity_node_id must be string")

            if step.type == "switch":
                if not step.switch or not isinstance(step.switch, SwitchConfig):
                    errors.append(f"Step '{step.id}' must have a valid SwitchConfig")
                else:
                    if not isinstance(step.switch.item, str):
                        errors.append(f"Step '{step.id}' switch.item must be string")
                    if not isinstance(step.switch.cases, list) or len(step.switch.cases) == 0:
                        errors.append(f"Step '{step.id}' switch.cases must be a non-empty list")
                    has_default = False
                    for case in step.switch.cases:
                        if not isinstance(case, SwitchCase):
                            errors.append(f"Step '{step.id}' switch case must be SwitchCase object")
                        else:
                            if case.is_default:
                                has_default = True
                            if case.condition is not None and not isinstance(case.condition, str):
                                errors.append(f"Step '{step.id}' switch case condition must be string or None")
                            if not isinstance(case.next_node_id, str):
                                errors.append(f"Step '{step.id}' switch case next_node_id must be string")
                    if not has_default:
                        errors.append(f"Step '{step.id}' switch node has no default case")

        # --- 6. Validate references for all nextNodeId / loop / switch / condition ---
        all_step_ids = {s.id for s in payload.steps}
        for step in payload.steps:
            # Validate nextNodeId
            if step.nextNodeId and step.nextNodeId not in all_step_ids:
                errors.append(f"Step '{step.id}' nextNodeId '{step.nextNodeId}' does not exist in workflow")

            # Validate loop activity_node_id
            if step.loop and step.loop.activity_node_id not in all_step_ids:
                errors.append(f"Step '{step.id}' loop activity_node_id '{step.loop.activity_node_id}' does not exist")

            # Validate condition nodes
            if step.type == "condition" and step.condition:
                if step.condition.on_true not in all_step_ids:
                    errors.append(f"Step '{step.id}' condition on_true '{step.condition.on_true}' does not exist")
                if step.condition.on_false not in all_step_ids:
                    errors.append(f"Step '{step.id}' condition on_false '{step.condition.on_false}' does not exist")

            # Validate switch cases
            if step.type == "switch" and step.switch:
                for case in step.switch.cases:
                    if case.next_node_id not in all_step_ids:
                        errors.append(f"Step '{step.id}' switch case next_node_id '{case.next_node_id}' does not exist")

        # --- 7. Raise errors if any ---
        if errors:
            raise ValueError("Workflow Validation Errors:\n" + "\n".join(errors))

        return True
