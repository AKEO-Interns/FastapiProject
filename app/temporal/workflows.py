# app/temporal/workflows.py
from temporalio import workflow
from datetime import timedelta
from app.schemas.workflow_schema import WorkflowPayload
from inspect import signature
from typing import Any

@workflow.defn
class GenericWorkflow:

    @workflow.run
    async def run(self, payload: WorkflowPayload):
        results = {}

        for step in payload.steps:
            # Ensure single argument if inputs is dict
            activity_args = (step.inputs,)  # pass dict as one positional argument

            if step.background:
                workflow.start_activity(
                    step.name,
                    *activity_args,
                    start_to_close_timeout=timedelta(seconds=30),
                )
            else:
                result = await workflow.execute_activity(
                    step.name,
                    *activity_args,
                    start_to_close_timeout=timedelta(seconds=30),
                )
                results[step.name] = result

        return results
    def _build_activity_args(self, activity_name: str, inputs: Any):
        """
        STRICTLY match activity function signature
        """

        activity_fn = workflow.get_activity(activity_name)
        params = list(signature(activity_fn).parameters.values())

        # Activity expects ONE primitive (int, float, str)
        if (
            len(params) == 1
            and params[0].annotation in (int, float, str)
            and isinstance(inputs, dict)
        ):
            # Extract value from dict
            return (next(iter(inputs.values())),)

        # Otherwise pass inputs as single argument
        return (inputs,)


