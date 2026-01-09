from abc import ABC, abstractmethod

class StepStrategy(ABC):

    @abstractmethod
    async def execute(self, workflow_ctx, step, context):
        pass
