from pathlib import Path
import os
import json

from fastapi import FastAPI, Request, Response, HTTPException

from conversion import decode_json, encode_json, InvalidXmlFormat, InvalidXmlItem


APP_DIR = Path(os.path.dirname(__file__))
INDEX_FILE_PATH = APP_DIR / "static" / "index.html"


app = FastAPI()    


@app.get("/")
async def index_page():
    page = INDEX_FILE_PATH.read_text()
    return Response(content=page, media_type="text/html")


@app.post("/json2xml")
async def json2xml(request: Request):
    try:
        json_body = await request.json()
    except json.decoder.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Data in body is not valid JSON")
    print(json_body)
    data = encode_json(json_body)
    resp = Response(content=data, media_type="application/xml")
    return resp


@app.post("/xml2json")
async def xml2json(request: Request):
    raw_body = await request.body()
    print(raw_body)
    try:
        resp = decode_json(raw_body)
    except InvalidXmlFormat:
        raise HTTPException(status_code=400, detail="Data in body is not valid XML file")
    except InvalidXmlItem as e:
        raise HTTPException(status_code=400, detail=str(e))
    return resp
