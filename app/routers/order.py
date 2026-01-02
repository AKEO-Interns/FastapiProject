
from fastapi import APIRouter, Depends
from temporalio.client import Client
from app.temporal.workflows import GenericWorkflow
from app.auth.auth_handler import get_current_user

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/temporal_order/")
async def temporal_order(user_id: int, token: str, book_id: int, user=Depends(get_current_user)):
    client = await Client.connect("localhost:7233")
    workflow_handle = await client.workflow.start(
        GenericWorkflow.run,
        user_id,
        token,
        book_id,
        id=f"order-{user_id}-{book_id}",
        task_queue="bookstore-task-queue"
    )
    return {"message": "Order workflow started", "workflow_id": workflow_handle.id}
