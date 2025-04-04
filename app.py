from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib

app = FastAPI()

class HashRequest(BaseModel):
    message: str

@app.post("/sha256")
def hash_message(data: HashRequest):
    try:
        hash_object = hashlib.sha256(data.message.encode())
        return {"sha256": hash_object.hexdigest()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# test trigger
