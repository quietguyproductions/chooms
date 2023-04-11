import json
from typing import Any, Dict, Union
from call_ai_function import call_ai_function
from config import Config
from json_utils import correct_json

cfg = Config()

JSON_SCHEMA = """
{
    "command": {
        "name": "command name",
        "args":{
            "arg name": "value"
        }
    },
    "thoughts":
    {
        "text": "thought",
        "reasoning": "reasoning",
        "plan": "- short bulleted\n- list that conveys\n- long-term plan",
        "criticism": "constructive self-criticism",
        "speak": "thoughts summary to say to user"
    }
}
"""


def fix_and_parse_json(    
    json_str: str,
    try_to_fix_with_gpt: bool = True
) -> Union[str, Dict[Any, Any]]:
    """Fix and parse JSON string"""
    try:
        json_str = json_str.replace('\t', '')
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        if "Expecting property name" in str(e):
            error_message = "JSON syntax error: property name is missing or invalid."
        elif "Expecting value" in str(e):
            error_message = "JSON syntax error: property value is missing or invalid."
        else:
            error_message = "JSON parsing error."
        raise ValueError(f"{error_message} Original error message: {str(e)}")
    except TypeError as e:
        raise ValueError(f"JSON string is empty or None. Original error message: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error while parsing JSON. Original error message: {str(e)}")
    # ... rest of the code
    

def fix_json(json_str: str, schema: str) -> str:
    """Fix the given JSON string to make it parseable and fully complient with the provided schema."""
    
    try:
        json.loads(json_str)  # just check the validity
        return json_str
    except json.JSONDecodeError as e:
        if "Expecting property name" in str(e):
            error_message = "JSON syntax error: property name is missing or invalid."
        elif "Expecting value" in str(e):
            error_message = "JSON syntax error: property value is missing or invalid."
        else:
            error_message = "JSON parsing error."
        raise ValueError(f"{error_message} Original error message: {str(e)}")
    except TypeError as e:
        raise ValueError(f"JSON string is empty or None. Original error message: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error while fixing JSON. Original error message:
