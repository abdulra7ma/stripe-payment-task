from black import List
from rest_framework.fields import Field


def serializer_error_messages(fields: List[Field]) -> dict:
    error_messages = {}

    required = "required"
    max_length = "max_length"

    # for field in fields:
    #     print("Field: ", field)
    #     field_name = field.field_name

    #     if field.required:
    #         error_messages[field_name][required] = True

    return error_messages