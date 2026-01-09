# # # condition_strategy.py
# from app.temporal.step_strategy import StepStrategy

# class ConditionStrategy(StepStrategy):

#     async def execute(self, workflow_ctx, step, context, **kwargs):
#         if not step.condition:
#             return None

#         condition = workflow_ctx._resolve_condition(
#             step.condition.expression,
#             context
#         )

#         condition = (
#             condition
#             .replace("true", "True")
#             .replace("false", "False")
#         )

#         try:
#             result = eval(condition)
#         except Exception as e:
#             raise ValueError(f"Condition eval failed: {condition}") from e

#         return (
#             step.condition.on_true
#             if result
#             else step.condition.on_false
#         )

# condition_strategy.py

from app.temporal.step_strategy import StepStrategy

class ConditionStrategy(StepStrategy):

    async def execute(self, workflow_ctx, step, context, **kwargs):
        if not step.condition:
            return None

        # Resolve the expression from the workflow context
        condition = workflow_ctx._resolve_condition(step.condition.expression, context)
        condition = condition.replace("true", "True").replace("false", "False")

        try:
            result = eval(condition, {}, {})
        except Exception as e:
            raise ValueError(f"Condition eval failed: {condition}") from e

        # Return the next step ID based on result
        return step.condition.on_true if result else step.condition.on_false

    









