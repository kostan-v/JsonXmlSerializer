from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


TEST_JSON = {
    "apple": 7,
    "orange": 4.1,
    "other": {
        "banana": "fruit"
    },
    "many": [
        True,
        "thing",
        {
            "pineapple": None
        }
    ]
}


TEST_JSON_XML_ENCODED = """<ITEM type="object">
    <ITEM key="apple" type="integer" value="7"/>
    <ITEM key="orange" type="float" value="4.1"/>
    <ITEM key="other" type="object">
        <ITEM key="banana" type="string" value="fruit"/>
    </ITEM>
    <ITEM key="many" type="list">
        <ITEM type="boolean" value="true"/>
        <ITEM type="string" value="thing"/>
        <ITEM type="object">
            <ITEM key="pineapple" type="null"/>
        </ITEM>
    </ITEM>
</ITEM>"""


def test_xml2json_example():
    response = client.post("/xml2json", data=TEST_JSON_XML_ENCODED)
    assert response.status_code == 200
    assert response.json() == TEST_JSON


def test_json2xml_example():
    response = client.post("/json2xml", json=TEST_JSON)
    print(response.text)
    print(type(response.text))
    print(type(TEST_JSON_XML_ENCODED))
    assert response.status_code == 200
    assert response.text == TEST_JSON_XML_ENCODED


def test_xml2json_exceptions():
    response = client.post("/xml2json", data="<ITEM type="object">")
    assert response.status_code == 400
    assert response.json() == {"detail": "Data in body is not valid XML file"}


def test_json2xml_exceptions():
    response = client.post("/json2xml", data="{\"test\": None}")
    assert response.status_code == 400
    assert response.json() == {"detail": "Data in body is not valid JSON"}
