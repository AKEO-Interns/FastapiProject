
from fastapi import APIRouter



router = APIRouter(
    prefix = "/payment",
    tags = ["Payment"]
)

#create list 
TransactionHistory = []

@router.post("/makePayment")
def createPayment():
    fee = 100
    TransactionHistory.append(fee)

    return TransactionHistory

@router.get("/seeYourTransaction")
def transactionHistory():
    return TransactionHistory
