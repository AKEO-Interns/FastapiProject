from temporalio import workflow
from datetime import timedelta


@workflow.defn
class PaymentWorkflow:

    @workflow.run
    async def run(self, data: dict):
        # Simulate payment
        return {
            "payment_status": "SUCCESS",
            "order_id": data["order_id"]
        }
