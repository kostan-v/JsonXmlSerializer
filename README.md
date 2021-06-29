# JsonXmlSerializer name

<!--- These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and licence info here --->
![GitHub license](https://img.shields.io/github/license/kostan-v/JsonXmlSerializer)

JsonXmlSerializer is a simple REST service that converts between JSON and XML

You can use `[POST] /json2xml` to convert from JSON to XML and `[POST] /xml2json` for backwards conversion.

## Prerequisites

Before you begin, ensure you have met the following requirements:
* You have installed Docker
* (Optional) You have installed Docker-Compose

## Running JsonXmlSerializer server

To run the server open you terminal or command line, navigate to project root directory and execute these commands.

### Using Docker-Compose

Run server
```
docker-compose -d up
```

Close server
```
docker-compose down
```

### Using Docker

Run server

* Create docker image (only once)
```
docker build -t json-xml-serializer .
```
* Run the image
```
docker run -d -p 80:80 json-xml-serializer
```

Close server
```
docker ps
docker kill <id_of_json-xml-serializer>
```

### Web app

When you have server running you can go to http://localhost:80/ to view web app.

## Endpoints

`[GET] /`

Returns utility web app that uses the `/json2xml` and `/xml2json` endpoints to convert between JSON and XML.

`[POST] /json2xml`

Converts a POSTed JSON file to an XML file and returns it.

`[POST] /xml2json`

Converts a POSTed XML file to a JSON and returns it.
