from fastapi import APIRouter, HTTPException
from temporalio.client import Client
from app.schemas.workflow_schema import WorkflowPayload
from app.temporal.workflows import GenericWorkflow
from app.validators.payload_validators import WorkflowValidator


router = APIRouter(prefix="/workflow", tags=["Workflow"])

@router.post("/start_workflow")
async def start_workflow(payload: WorkflowPayload):
    try:
        WorkflowValidator.pre_validate(payload)
    except ValueError as e:
        # BLOCK EXECUTION
        raise HTTPException(status_code=400, detail=str(e))
    
    client = await Client.connect("localhost:7233")

    handle = await client.start_workflow(
        GenericWorkflow.run,     # workflow entry
        payload,                 # payload
        id="dynamic-workflow-1", # must be unique
        task_queue="bookstore-task-queue",
    )

    return {
        "workflow_id": handle.id,
        "run_id": handle.first_execution_run_id,
        "status": "started"
    }

@router.get("/result/{workflow_id}")
async def get_result(workflow_id: str):
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle(workflow_id)
    result = await handle.result()
    return result



