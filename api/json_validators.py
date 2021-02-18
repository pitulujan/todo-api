from jsonschema import validate, Draft7Validator
from itertools import islice
from typing import List

update_task = Draft7Validator(
    {
        "type": "object",
        "properties": {
            "_id": {
                "type": "string",
                "description": "Id of the task to be modified",
            },
            "description": {
                "type": "string",
                "description": "Description of the task to be modified",
                "minLength": 3,
                "maxLength": 64,
            },
            "done": {
                "type": "boolean",
                "description": "Current statuts of the task",
            },
            "title": {
                "type": "string",
                "description": "Title of the task to be modified",
                "minLength": 3,
                "maxLength": 256,
            },
        },
        "required": ["_id", "done"],
    }
)


def iterate_properties_updatetask(
    request_json: dict,
):
    """
    Returns a small selection of the errors encountered, or an empty list if no errors encountered
    """

    errors: List[str] = []

    errors += islice(update_task.iter_errors(request_json), 3)
    return errors


new_task = Draft7Validator(
    {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "Description of the task to be modified",
                "minLength": 3,
                "maxLength": 64,
            },
            "done": {
                "type": "boolean",
                "description": "Current statuts of the task",
            },
            "title": {
                "type": "string",
                "description": "Title of the task to be modified",
                "minLength": 3,
                "maxLength": 256,
            },
        },
        "required": ["done", "title", "description"],
    }
)


def iterate_properties_newtask(
    request_json: dict,
):
    """
    Returns a small selection of the errors encountered, or an empty list if no errors encountered
    """

    errors: List[str] = []

    errors += islice(new_task.iter_errors(request_json), 3)
    return errors


delete_task = Draft7Validator(
    {
        "type": "object",
        "properties": {
            "_id": {
                "type": "string",
                "description": "Id of the task to be modified",
            },
        },
        "required": ["_id"],
    }
)


def iterate_properties_deletetask(
    request_json: dict,
):
    """
    Returns a small selection of the errors encountered, or an empty list if no errors encountered
    """

    errors: List[str] = []

    errors += islice(delete_task.iter_errors(request_json), 3)
    return errors
