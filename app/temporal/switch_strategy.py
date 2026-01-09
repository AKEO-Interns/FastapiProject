

from app.temporal.step_strategy import StepStrategy

class SwitchStrategy:
    async def execute(self, workflow_ctx, step, context, **_):
        switch = step.switch
        value = eval(
            workflow_ctx._resolve_condition(switch.item, context),
            {}, {}
        )

        default = None
        for case in switch.cases:
            if getattr(case, "is_default", False):
                default = case.next_node_id
                continue

            expr = case.condition.replace("value", repr(value))
            if eval(expr, {}, {}):
                return case.next_node_id

        return default







