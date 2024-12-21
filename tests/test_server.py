import pytest
from elevenlabs_mcp.server import ElevenLabsServer


def test_parse_script_valid_input():
    server = ElevenLabsServer()
    valid_json = '''
    {
        "script": [
            {
                "text": "Hello world",
                "voice_id": "voice1",
                "actor": "narrator"
            }
        ]
    }
    '''
    
    script_parts, debug_info = server.parse_script(valid_json)
    
    assert len(script_parts) == 1
    assert script_parts[0]["text"] == "Hello world"
    assert script_parts[0]["voice_id"] == "voice1"
    assert script_parts[0]["actor"] == "narrator"

# Valid JSON with script array containing multiple parts with text, voice_id, and actor
def test_parse_valid_script_json():
    server = ElevenLabsServer()
    script_json = '''
    {
        "script": [
            {"text": "Hello", "voice_id": "voice1", "actor": "Bob"},
            {"text": "World", "voice_id": "voice2", "actor": "Alice"}
        ]
    }'''

    script_parts, debug_info = server.parse_script(script_json)

    assert len(script_parts) == 2
    assert script_parts[0] == {
        "text": "Hello",
        "voice_id": "voice1", 
        "actor": "Bob"
    }
    assert script_parts[1] == {
        "text": "World",
        "voice_id": "voice2",
        "actor": "Alice"
    }
    assert len(debug_info) > 0

def test_parse_script_invalid_json():
    server = ElevenLabsServer()
    invalid_json = "{ invalid json }"
    
    with pytest.raises(Exception) as exc_info:
        server.parse_script(invalid_json)
    
    assert "Invalid JSON format" in str(exc_info.value)

def test_parse_script_only_text():
    server = ElevenLabsServer()
    json_with_only_text = '''
    {
        "script": [
            {"text": "Hello world"}
        ]
    }
    '''
    
    script_parts, debug_info = server.parse_script(json_with_only_text)
    
    assert len(script_parts) == 1
    assert script_parts[0]["text"] == "Hello world"
    assert script_parts[0]["voice_id"] is None
    assert script_parts[0]["actor"] is None

def test_parse_script_missing_voice():
    server = ElevenLabsServer()
    json_missing_voice = '''
    {
        "script": [
            {
                "text": "Hello world",
                "actor": "narrator"
            }
        ]
    }
    '''
    
    script_parts, debug_info = server.parse_script(json_missing_voice)
    
    assert len(script_parts) == 1
    assert script_parts[0]["text"] == "Hello world"
    assert script_parts[0]["voice_id"] is None
    assert script_parts[0]["actor"] == "narrator"

def test_parse_script_missing_actor():
    server = ElevenLabsServer()
    json_missing_actor = '''
    {
        "script": [
            {
                "text": "Hello world",
                "voice_id": "voice1"
            }
        ]
    }
    '''
    
    script_parts, debug_info = server.parse_script(json_missing_actor)
    
    assert len(script_parts) == 1
    assert script_parts[0]["text"] == "Hello world"
    assert script_parts[0]["voice_id"] == "voice1"
    assert script_parts[0]["actor"] is None

def test_parse_script_empty_array():
    server = ElevenLabsServer()
    empty_script = '''
    {
        "script": []
    }
    '''
    
    script_parts, debug_info = server.parse_script(empty_script)
    
    assert len(script_parts) == 0

def test_parse_script_empty_object():
    server = ElevenLabsServer()
    empty_object = '''
    {
        "script": [
            {}
        ]
    }
    '''
    
    with pytest.raises(Exception) as exc_info:
        server.parse_script(empty_object)
    
    assert "Missing required field 'text'" in str(exc_info.value)
