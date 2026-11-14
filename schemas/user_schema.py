USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "email", "tenant"],
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "email": {"type": "string"},
        "tenant": {"type": "string"},
    },
    "additionalProperties": False,
}
