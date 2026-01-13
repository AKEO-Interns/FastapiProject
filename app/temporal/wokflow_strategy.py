

from temporalio import workflow
from app.temporal.child_workflow import PaymentWorkflow
from app.temporal.step_strategy import StepStrategy


class WorkflowStrategy(StepStrategy):

    async def execute(self, workflow_ctx, step, context, **_):
        # use workflow_ctx to resolve inputs
        resolved_inputs = workflow_ctx._resolve_inputs(step.inputs, context)

        if step.background:
            workflow.start_child_workflow(
                step.name,
                resolved_inputs,
                workflow_class=PaymentWorkflow
            )
            return None

        result = await workflow.execute_child_workflow(
            PaymentWorkflow,
            resolved_inputs
        )

    
        return result

