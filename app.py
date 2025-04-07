from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib
from typing import Union, List

pepper = 'innofi-jay-anderson'

app = FastAPI()

class HashRequest(BaseModel):
    message: Union[str, List[str]]

@app.post("/sha256")
def hash_message(data: HashRequest):

    try:
        input_type = type(data.message)
        input_list = data.message if isinstance(data.message, list) else [data.message]
        response_dict = {'__input_type__': input_type}
        for x in input_list:
            salted_message = str(x) + pepper
            response_dict[x] = hashlib.sha256(salted_message.encode()).hexdigest()

        return response_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"message": "Welcome to the SHA256 API ✨ Use POST /sha256"}

# salted_message = data.message + pepper
# return {"sha256": hashlib.sha256(salted_message.encode()).hexdigest()}