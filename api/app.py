from fastapi import FastAPI, WebSocket
from mangum import Mangum

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# adaptar la rest API a Lambda
handler = Mangum(app)