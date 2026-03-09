from fastapi import HTTPException
from typing import Dict, Any


VALIDATION_RULES = {
    "/users": {
        "POST": {
            "required_fields": ["username", "email", "password"],
            "field_types": {
                "username": str,
                "email": str,
                "password": str
            },
        }
    },
    "/payments": {
        "POST": {
            "required_fields": ["amount", "currency"],
            "field_types": {
                "amount": (int, float),
                "currency": str
            },
        }
    },
}


def validate_request(path: str, method: str, body: Dict[str, Any] | None):
    """
    Validates request body against configured rules.
    Uses prefix matching for dynamic routes.
    """

    if not body:
        return

    matched_rules = None

    # Prefix matching instead of exact match
    for rule_path in VALIDATION_RULES:
        if path.startswith(rule_path):
            matched_rules = VALIDATION_RULES[rule_path]
            break

    if not matched_rules:
        return

    method_rules = matched_rules.get(method.upper())
    if not method_rules:
        return

    required_fields = method_rules.get("required_fields", [])

    for field in required_fields:
        if field not in body:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required field: {field}"
            )

    field_types = method_rules.get("field_types", {})

    for field, expected_type in field_types.items():
        if field in body and not isinstance(body[field], expected_type):
            raise HTTPException(
                status_code=400,
                detail=f"Field '{field}' must be of type {expected_type}"
            )