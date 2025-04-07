from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib
import traceback
import os
from typing import Union, List

PEPPER = os.environ.get("PEPPER")

if not PEPPER:
    raise RuntimeError("Missing required environment variable: PEPPER")

app = FastAPI()

class HashRequest(BaseModel):
    message: Union[str, List[str]]
    use_pepper: bool = True

@app.post("/sha256")
def hash_message(data: HashRequest):

    try:
        input_type = type(data.message)
        input_list = data.message if isinstance(data.message, list) else [data.message]
        response_dict = {'__input_type__':str(input_type)}
        for x in input_list:
            pepper_for_hashing = PEPPER if data.use_pepper else ''
            salted_message = str(x) + pepper_for_hashing
            response_dict[x] = hashlib.sha256(salted_message.encode()).hexdigest()

        return response_dict

    except Exception as e:
        traceback.print_exc()  # Prints full stack trace to console/logs
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "type": type(e).__name__
            }
        )

# todo add a boolean flag that tells us whether to use the pepper
# default true

@app.get("/")
def root():
    return {"message": "v1.1.05 ;  Welcome to the SHA256 API ✨ Use POST /sha256"}

