# # activity_strategy.py
from app.temporal.step_strategy import StepStrategy
from temporalio import workflow
from datetime import timedelta
class ActivityStrategy(StepStrategy):

    async def execute(self, workflow_ctx, step, context, **kwargs):
        resolved_inputs = workflow_ctx._resolve_inputs(step.inputs, context)

        # Example: Replace with Temporal activity execution


        if step.background:
            workflow.start_activity(
                step.name,
                resolved_inputs,
                start_to_close_timeout=timedelta(seconds=30),
            )
            return None
        else:
            result = await workflow.execute_activity(
                step.name,
                resolved_inputs,
                start_to_close_timeout=timedelta(seconds=30),
            )
            return result


