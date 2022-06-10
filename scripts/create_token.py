
# pip install pyjwt

import os
import jwt
from datetime import datetime, timedelta

key = os.environ.get("TOKEN_KEY", "my-secret-key")

iat_time = datetime.now()
exp_time = iat_time + timedelta(days=365)

claims = {
    "iss": "twave",
    "sub": "twave",
    "iat": int(iat_time.timestamp()),
    "exp": int(exp_time.timestamp()),
}
encoded = jwt.encode(claims, key, algorithm="HS256")
print(claims)
print(encoded)