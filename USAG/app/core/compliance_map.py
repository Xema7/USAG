from typing import Dict, List


# ---------------------------------------------------------
# Compliance Levels
# ---------------------------------------------------------

COMPLIANCE_PUBLIC = "Public"
COMPLIANCE_INTERNAL = "Internal"
COMPLIANCE_SENSITIVE = "Sensitive"
COMPLIANCE_RESTRICTED = "Restricted"


# ---------------------------------------------------------
# Endpoint Compliance Configuration
# Key: endpoint path
# Value: metadata
# ---------------------------------------------------------

COMPLIANCE_RULES: Dict[str, Dict] = {
    "/health": {
        "level": COMPLIANCE_PUBLIC,
        "allowed_roles": [],
        "description": "Health check endpoint"
    },
    "/users": {
        "level": COMPLIANCE_INTERNAL,
        "allowed_roles": ["admin", "user"],
        "description": "User information access"
    },
    "/payments": {
        "level": COMPLIANCE_SENSITIVE,
        "allowed_roles": ["admin"],
        "description": "Financial transaction endpoint"
    },
    "/audit/logs": {
        "level": COMPLIANCE_RESTRICTED,
        "allowed_roles": ["admin", "auditor"],
        "description": "Audit trail access"
    },
    "/ai/security-report": {
    "level": COMPLIANCE_RESTRICTED,
    "allowed_roles": ["admin", "auditor"],
    "description": "AI-based security intelligence endpoint"
    },
}


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------

def get_compliance_metadata(path: str) -> Dict:
    """
    Returns compliance metadata for a given path.
    Defaults to INTERNAL if not configured.
    """

    for rule_path in COMPLIANCE_RULES:
        if path.startswith(rule_path):
            return COMPLIANCE_RULES[rule_path]

    return {"level": COMPLIANCE_INTERNAL, "allowed_roles": []}


def is_role_allowed(path: str, role: str) -> bool:
    """
    Check if user role is allowed to access endpoint.
    If allowed_roles is empty, endpoint is public/internal.
    """
    metadata = get_compliance_metadata(path)
    allowed_roles: List[str] = metadata.get("allowed_roles", [])

    return True if not allowed_roles else role in allowed_roles
