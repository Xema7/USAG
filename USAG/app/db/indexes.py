from app.db.mongodb import get_database


async def create_indexes():
    db = get_database()

    collection = db["audit_logs"]

    await collection.create_index("timestamp")
    await collection.create_index("user_id")
    await collection.create_index("endpoint")
    await collection.create_index("compliance_tag")
    await collection.create_index("request_id")

    await collection.create_index(
        [("user_id", 1), ("timestamp", -1)]
    )
