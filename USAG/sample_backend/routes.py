from fastapi import APIRouter

router = APIRouter()

# -----------------------------------------
# Public endpoint (no validation rule)
# -----------------------------------------

@router.get("/public")
async def public_endpoint():
    return {
        "message": "This is a public backend endpoint."
    }

# -----------------------------------------
# Users Endpoint
# -----------------------------------------

@router.post("/users")
async def create_user(payload: dict):
    return {
        "message": "User created successfully",
        "data": payload
    }

@router.get("/users")
async def list_users():
    return [
        {"id": 1, "username": "alice"},
        {"id": 2, "username": "bob"}
    ]

# -----------------------------------------
# Payments Endpoint
# -----------------------------------------

@router.post("/payments")
async def create_payment(payload: dict):
    return {
        "message": "Payment processed",
        "amount": payload.get("amount"),
        "currency": payload.get("currency")
    }


@router.get("/payments")
async def list_payments():
    return [
        {"id": 101, "amount": 100, "currency": "USD"},
        {"id": 102, "amount": 250, "currency": "EUR"},
    ]