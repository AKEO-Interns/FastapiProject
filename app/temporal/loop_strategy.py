from app.temporal.step_strategy import StepStrategy
from app.schemas.workflow_schema import WorkflowPayload

class LoopStrategy(StepStrategy):

    async def execute(self, workflow_ctx, step, context, step_map=None, **kwargs):
        loop = step.loop
        if not loop or not step_map:
            return None

        results = []

        activity_step = step_map.get(loop.activity_node_id)
        if not activity_step:
            raise ValueError(
                f"Loop activity node '{loop.activity_node_id}' not found"
            )

        activity_strategy = workflow_ctx.strategies.get(activity_step.type)
        if not activity_strategy:
            raise ValueError(
                f"No strategy for activity type {activity_step.type}"
            )

        for val in range(loop.start, loop.end, loop.step):
            print("🔁 LOOP ITERATION:", val)

            # set iterator in SAME context
            context[loop.iterator] = val

            # execute activity directly
            output = await activity_strategy.execute(
                workflow_ctx=workflow_ctx,
                step=activity_step,
                context=context,
                step_map=step_map
            )

            results.append(output)

        return results

  


















