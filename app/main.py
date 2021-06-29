"""Implementation of JsonXmlSerailizer server"""

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
    """
    Returns utility web app that uses the `/json2xml` and `/xml2json` endpoints to convert
    between JSON and XML.
    """
    page = INDEX_FILE_PATH.read_text()
    return Response(content=page, media_type="text/html")


@app.post("/json2xml")
async def json2xml(request: Request):
    """Converts a POSTed JSON file to an XML file and returns it."""
    try:
        json_body = await request.json()
    except json.decoder.JSONDecodeError as err:
        raise HTTPException(status_code=400, detail="Data in body is not valid JSON") from err
    print(json_body)
    data = encode_json(json_body)
    resp = Response(content=data, media_type="application/xml")
    return resp


@app.post("/xml2json")
async def xml2json(request: Request):
    """Converts a POSTed XML file to a JSON and returns it."""
    raw_body = await request.body()
    print(raw_body)
    try:
        resp = decode_json(raw_body)
    except InvalidXmlFormat as err:
        raise HTTPException(status_code=400, detail="Data in body is not valid XML file") from err
    except InvalidXmlItem as err:
        raise HTTPException(status_code=400, detail=str(err)) from err
    return resp
