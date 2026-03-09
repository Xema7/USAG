import jwt
from datetime import datetime, timedelta

SECRET = "1OJX7pTd5nfXC6kJ1LI1wxIaoZJRsU7LgMgmzTXjKEM"

payload = {
    "sub": "user001",
    "role": "user",
    "exp": datetime.utcnow() + timedelta(hours=2)
}

token = jwt.encode(payload, SECRET, algorithm="HS256")
print("\nGenerated JWT:\n")
print(token)