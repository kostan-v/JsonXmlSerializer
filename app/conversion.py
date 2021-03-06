"""Implementation of encoding / decoding JSON to XML"""

from xml.etree import ElementTree as ET
from xml.dom import minidom
import io


JSON_DATA_TYPES = {"string", "integer", "float", "object", "list", "boolean", "null"}

TYPE_MAPPING = {
    ("string", str),
    ("integer", int),
    ("float", float),
    ("boolean", bool),
    ("null", type(None)),
    ("object", dict),
    ("list", list),
}

KEYWORD_TO_PYTHON_TYPE = dict(TYPE_MAPPING)
PYTHON_TYPE_TO_KEYWORD = {t: type_kw for type_kw, t in TYPE_MAPPING}


class InvalidXmlFormat(Exception):
    """Raised when parsed XML data in not valid XML file"""


class InvalidXmlItem(Exception):
    """Raised when parsing of <ITEM> element fails"""


def decode_json_item(item: ET.Element):
    """Convert XML-encoded JSON element to Python object"""
    if item.tag != "ITEM":
        raise InvalidXmlItem(f"Unexpected element '{item.tag}'")

    item_type = item.get("type", None)

    if item_type is None:
        raise InvalidXmlItem(f"Missing 'type' attribute in element '{item.text}'")

    if item_type == "list":
        return [decode_json_item(child) for child in item]

    if item_type == "object":
        for child in item:
            if "key" not in child:
                InvalidXmlItem(f"Missing 'key' attribute in element '{child.text}'")
        return {child.attrib["key"]: decode_json_item(child) for child in item}

    if item_type == "null":
        return None

    if item_type in KEYWORD_TO_PYTHON_TYPE:
        value = item.get("value")
        if value is None:
            raise InvalidXmlItem(f"Missing 'value' attribute in element '{item.text}'")
        return KEYWORD_TO_PYTHON_TYPE[item_type](value)

    raise InvalidXmlItem(f"Unexpected 'type' attribute '{item_type}'")


def decode_json(xml_data: bytes):
    """Convert XML-encoded JSON to python object that can be converted to JSON using json.dumps"""
    stream = io.BytesIO(xml_data)
    try:
        tree = ET.parse(stream)
    except ET.ParseError as err:
        raise InvalidXmlFormat from err
    root = tree.getroot()
    return decode_json_item(root)


def encode_json_item(obj, parent=None) -> ET.Element:
    """Convert Python object to XML-encoded JSON element"""
    type_kw = PYTHON_TYPE_TO_KEYWORD.get(type(obj))
    if type_kw is None:
        raise Exception(f"Unsupported python object of type {type(obj)} for conversion to JSON!")

    if parent is None:
        node = ET.Element("ITEM")
    else:
        node = ET.SubElement(parent, "ITEM")
    node.attrib["type"] = type_kw

    if obj is None:
        pass
    elif isinstance(obj, list):
        for val in obj:
            encode_json_item(val, node)
    elif isinstance(obj, dict):
        for key, val in obj.items():
            child = encode_json_item(val, node)
            child.attrib["key"] = str(key)
    elif isinstance(obj, bool):
        node.attrib["value"] = "true" if obj else "false"
    else:
        node.attrib["value"] = str(obj)

    return node


def prettyprint_xml(node : ET.Element):
    """Get string containing prettyprinted XML element (with children)."""
    # Apparently if you want to prettyprint xml in native Python you have to either format and parse
    # and reformat XML using minidom but it cannot ommit header.

    pretty_xml = minidom.parseString(ET.tostring(node)).toprettyxml(indent="    ")
    return pretty_xml.split('\n', maxsplit=1)[1].rstrip('\n')


def encode_json(obj) -> bytes:
    """Convert python object convertable to JSON to XML"""
    root = encode_json_item(obj)
    return prettyprint_xml(root)
