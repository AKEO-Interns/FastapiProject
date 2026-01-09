

# generic_workflow.py
# from temporalio import workflow
# from typing import Any, Dict
# import re

# from app.schemas.workflow_schema import WorkflowPayload
# from app.temporal.activity_strategy import ActivityStrategy
# from app.temporal.wokflow_strategy import WorkflowStrategy
# from app.temporal.condition_strategy import ConditionStrategy
# from app.temporal.loop_strategy import LoopStrategy
# from app.temporal.switch_strategy import SwitchStrategy

# @workflow.defn
# class GenericWorkflow:

#     def __init__(self):
#         self.strategies = {
#             "activity": ActivityStrategy(),
#             "workflow": WorkflowStrategy(),
#             "condition": ConditionStrategy(),
#             "loop": LoopStrategy(),
#             "switch": SwitchStrategy()
#         }

#     @workflow.run
#     async def run(self, payload: WorkflowPayload):

#         context: Dict[str, Any] = {}
#         results: Dict[str, Any] = {}

#         step_map = {step.id: step for step in payload.steps}
#         current_step = payload.steps[0]
       

#         stop_after_current_activity = False

#         while current_step:
#             strategy = self.strategies.get(current_step.type)
#             print("which strategy :", strategy)
#             if not strategy:
#                 raise ValueError(f"No strategy for step type {current_step.type}")

#             workflow.logger.info(f"Executing step: {current_step.id}")

#             output = await strategy.execute(
#                 workflow_ctx=self,
#                 step=current_step,
#                 context=context,
#                 step_map=step_map
#             )
#             current_step.outputs = output
#             print("output field:", current_step.outputs)

#             # ================= ACTIVITY =================
#             if current_step.type == "activity":
#                 context[current_step.id] = output
#                 results[current_step.id] = output
                
#                 # if stop_after_current_activity:
#                 #     break   #  HARD STOP
            
               
#                 # normal sequential move
#                 idx = payload.steps.index(current_step)
#                 current_step = (
#                     payload.steps[idx + 1]
#                     if idx + 1 < len(payload.steps)
#                     else None
#                 )



#             # ================= CONDITION =================
#             elif current_step.type == "condition":


    
#                 current_step = step_map.get(output)

 

#             # ================= SWITCH =================
#             elif current_step.type == "switch":
#                 stop_after_current_activity=True
#                 current_step = step_map.get(output)
#                 print("switch step:", current_step)
                
            
#             #++++++++++++++++++++loop+++++++++++++++++++++
#             elif current_step.type == "loop":
#                 stop_after_current_activity=True
#                 idx = payload.steps.index(current_step)
#                 current_step = (
#                     payload.steps[idx + 1]
#                     if idx +1 < len(payload.steps)
#                     else None
#                 )

#             else:
#                 raise ValueError(f"Unsupported step type: {current_step.type}")
            


#         return results
           

#     # ================= INPUT RESOLVER =================
#     def _resolve_inputs(self, inputs: Any, context: dict):
#         if not isinstance(inputs, dict):
#             return inputs

#         resolved = {}
#         for key, value in inputs.items():
#             if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
#                 expr = value.strip("{}")
#                 parts = expr.split(".")

#                 if len(parts) == 2:
#                     step_name, field = parts
#                     step_output = context.get(step_name)

#                     if isinstance(step_output, dict):
#                         resolved[key] = step_output.get(field)
#                     elif field == "result":
#                         resolved[key] = step_output
#                     else:
#                         resolved[key] = None
#                 else:
#                     resolved[key] = context.get(parts[0])
#             else:
#                 resolved[key] = value

#         return resolved

#     # ================= CONDITION RESOLVER =================
#     def _resolve_condition(self, condition: str, context: dict) -> str:
#         def replacer(match):
#             expr = match.group(1).strip()
#             parts = expr.split(".")

#             if len(parts) == 2:
#                 step_name, field = parts
#                 step_output = context.get(step_name)

#                 if isinstance(step_output, dict):
#                     return repr(step_output.get(field))
#                 elif field == "result":
#                     return repr(step_output)

#             return repr(context.get(expr))

#         return re.sub(r"\{\{([^}]+)\}\}", replacer, condition)
    

#     #+++++++++++++++++++++++++++++ get_next_node++++++++++++++
#     def get_next_step(step, step_map, fallback=None):
#         if step.nextNodeId:
#             return step_map.get(step.nextNodeId)
#         return fallback


from temporalio import workflow
from typing import Any, Dict
import re

from app.schemas.workflow_schema import WorkflowPayload, StepNode
from app.temporal.activity_strategy import ActivityStrategy
from app.temporal.wokflow_strategy import WorkflowStrategy
from app.temporal.condition_strategy import ConditionStrategy
from app.temporal.loop_strategy import LoopStrategy
from app.temporal.switch_strategy import SwitchStrategy


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

    # ================= WORKFLOW RUN =================
    @workflow.run
    async def run(self, payload: WorkflowPayload):

        context: Dict[str, Any] = {}
        results: Dict[str,Any] = {}
        

        step_map = {step.id: step for step in payload.steps}
        print("stepNode :", step_map)

        # 🔹 find start node
        current_step = next(
            (s for s in payload.steps if s.isStartNode), None
        )
        if not current_step:
            raise ValueError("No start node defined")

        while current_step:
            workflow.logger.info(f"➡ Executing step: {current_step.id}")

            strategy = self.strategies.get(current_step.type)
            print("which strategy execute :", strategy)
            if not strategy:
                raise ValueError(f"No strategy for step type {current_step.type}")

            # 🔹 execute step
            output = await strategy.execute(
                workflow_ctx=self,
                step=current_step,
                context=context,
                step_map=step_map
            )
         

            # 🔹 store output
            current_step.outputs = output
            context[current_step.id] = output
            results[current_step.id] = output
        

            # 🔹 resolve next step
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




    
    
