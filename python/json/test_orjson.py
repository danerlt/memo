import json
import orjson

from common.const import DATA_PATH


def test_orjson_dumps_dict():
    # dumps（）将Python对象序列化为JSON。
    data = {"name": "你好", "age": 20, "sex": "man"}
    json_bytes = orjson.dumps(data)
    json_str = json_bytes.decode("utf-8")
    print(json_bytes)
    print(json_str)
    assert isinstance(json_bytes, bytes)
    assert json_bytes == b'{"name":"\xe4\xbd\xa0\xe5\xa5\xbd","age":20,"sex":"man"}'
    assert json_str == '{"name":"你好","age":20,"sex":"man"}'


def test_orjson_dumps_list():
    # dumps（）将Python对象序列化为JSON。
    data = [{"name": "你好", "age": 20, "sex": "man"}, {"name": "世界", "age": 20, "sex": "woman"}]
    json_bytes = orjson.dumps(data)
    json_str = json_bytes.decode("utf-8")
    assert isinstance(json_bytes, bytes)
    assert json_bytes == b'[{"name":"\xe4\xbd\xa0\xe5\xa5\xbd","age":20,"sex":"man"},{"name":"\xe4\xb8\x96\xe7\x95\x8c","age":20,"sex":"woman"}]'
    assert json_str == '[{"name":"你好","age":20,"sex":"man"},{"name":"世界","age":20,"sex":"woman"}]'


def test_orjson_loads_dict_by_bytes():
    # loads（）将JSON反序列化为Python对象。 loads可以接收bytes和字符串
    json_str = '{"name":"你好","age":20,"sex":"man"}'
    print(json_str)
    json_bytes = json_str.encode("utf-8")
    print(json_bytes)
    data = orjson.loads(json_bytes)
    assert isinstance(data, dict)
    assert data == {"name": "你好", "age": 20, "sex": "man"}


def test_orjson_loads_dict_by_str():
    # loads（）将JSON反序列化为Python对象。
    json_str = '{"name":"你好","age":20,"sex":"man"}'
    data = orjson.loads(json_str)
    assert isinstance(data, dict)
    assert data == {"name": "你好", "age": 20, "sex": "man"}


def test_orjson_dumps_vs_stb_lib():
    data = {"name": "你好", "age": 20, "sex": "man"}
    std_json_str = json.dumps(data, ensure_ascii=False, indent=2)
    print(std_json_str)
    or_json_str = orjson.dumps(data, option=orjson.OPT_INDENT_2).decode("utf-8")
    print(or_json_str)
    assert std_json_str == or_json_str


def test_orjson_dumps_vs_stb_lib_2():
    data = {"name": "你好", "age": 20, "sex": "man"}
    std_json_str = json.dumps(data, ensure_ascii=False, indent=4)
    print(std_json_str)
    or_json_str = orjson.dumps(data, option=orjson.OPT_INDENT_4).decode("utf-8")
    print(or_json_str)
    assert std_json_str == or_json_str


def test_orjson_load_from_file():
    file_path = DATA_PATH / "output_0.json"
    with open(file_path, 'rb') as f:
        data = orjson.loads(f.read())
    print(f"data length: {len(data)}")
    assert isinstance(data, dict)
