import jwt
from datetime import datetime, timedelta, timezone

# Must match your Gateway JWT_SECRET
SECRET = "dev-secret"

payload = {
    "user_id": "12345",
    "exp": datetime.now(timezone.utc) + timedelta(days=30),
    "iat": datetime.now(timezone.utc),
}

token = jwt.encode(payload, SECRET, algorithm="HS256")

print(f'export TOKEN="{token}"')