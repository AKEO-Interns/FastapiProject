import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from app.temporal.workflows import GenericWorkflow
from app.temporal.activities import (
    verify_user_activity,
    check_inventory_activity,
    create_order_activity
)

async def main():
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")

    # Create worker with heartbeating disabled
    worker = Worker(
        client,
        task_queue="bookstore-task-queue",
        workflows=[GenericWorkflow],
        activities=[
            verify_user_activity,
            check_inventory_activity,
            create_order_activity,
        ],
 
    )

    # Run worker loop
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())


