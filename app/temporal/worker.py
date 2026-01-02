import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from app.temporal.workflows import GenericWorkflow
from app.temporal.child_workflow import PaymentWorkflow
from app.temporal.activities import (
    verify_user_activity,
    check_inventory_activity,
    create_order_activity,
)

async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="bookstore-task-queue",
        workflows=[
            GenericWorkflow,
            PaymentWorkflow,
        ],
        activities=[
            verify_user_activity,
            check_inventory_activity,
            create_order_activity,
        ],
    )

    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())



