from temporalio import workflow
from datetime import timedelta
from app.schemas.workflow_schema import WorkflowPayload
from typing import Any
import re
from app.temporal.child_workflow import PaymentWorkflow

@workflow.defn
class GenericWorkflow:

    @workflow.run
    async def run(self, payload: WorkflowPayload):
        context = {}
        results = {}

        for step in payload.steps:
            resolved_inputs = self._resolve_inputs(step.inputs, context)  # <-- uses the method

            if step.type == "activity":
                if step.background:
                    workflow.start_activity(
                        step.name,
                        resolved_inputs,
                        start_to_close_timeout=timedelta(seconds=30),
                    )
                else:
                    result = await workflow.execute_activity(
                        step.name,
                        resolved_inputs,
                        start_to_close_timeout=timedelta(seconds=30),
                    )
                    context[step.name] = result
                    results[step.name] = result

            elif step.type == "workflow":
                if step.background:
                    workflow.start_child_workflow(
                        step.name,
                        resolved_inputs,
                        workflow_class=PaymentWorkflow,
                        
                    )
                else:
                    result = await workflow.execute_child_workflow(
                        PaymentWorkflow,
                        resolved_inputs,
                      
                    )
                    context[step.name] = result
                    results[step.name] = result

        return results

    def _resolve_inputs(self, inputs: Any, context: dict):
        """
        Resolve references like {{step_name.field}} using previous step outputs
        """
        if isinstance(inputs, dict):
            resolved = {}
            for key, value in inputs.items():
                if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                    # Parse {{step_name.field}}
                    step_field = value.strip("{}").split(".")
                    if len(step_field) == 2:
                        step_name, field = step_field
                        if step_name in context and field in context[step_name]:
                            resolved[key] = context[step_name][field]
                        else:
                            raise ValueError(f"Cannot resolve reference: {value}")
                    else:
                        raise ValueError(f"Invalid reference format: {value}")
                else:
                    resolved[key] = value
            return resolved
        return inputs
