from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib

pepper = 'innofi-jay-anderson'

app = FastAPI()

class HashRequest(BaseModel):
    message: str

    @app.post("/sha256")
    def hash_message(data: HashRequest):
        try:
            salted_message = data.message + pepper
            return {"sha256": hashlib.sha256(salted_message.encode()).hexdigest()}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"message": "Welcome to the SHA256 API ✨ Use POST /sha256"}