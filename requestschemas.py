PROCESS_QUESTIONS = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "questions_num": {
            "type": "integer",
            "minimum": 0
        }
    },
    "required": [
        "questions_num"
    ]
}