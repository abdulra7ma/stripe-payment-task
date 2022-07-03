from .constants import SerializerConst


def clean_field_name(field_name: str) -> str:
    return (field_name[0].upper() + field_name[1:]).replace("_", " ")


def serializer_error_messages(
    field_name, max_length=False, min_lenght=False
) -> dict:
    error_messages = {}

    if max_length:
        error_messages["max_length"] = (
            clean_field_name(field_name) + " " + SerializerConst.MAX_LENGTH
        )

    if min_lenght:
        error_messages["min_length"] = (
            clean_field_name(field_name) + " " + SerializerConst.MIN_LENGHT
        )

    return error_messages


def model_serializer_error_messages_formatter(
    field_name, max_length=False, min_lenght=False, required=False
) -> dict:
    error_messages = {"error_messages": {}}

    if required:
        error_messages["required"] = True

    if max_length:
        error_messages["error_messages"]["max_length"] = (
            clean_field_name(field_name) + " " + SerializerConst.MAX_LENGTH
        )

    if min_lenght:
        error_messages["error_messages"]["min_length"] = (
            clean_field_name(field_name) + " " + SerializerConst.MIN_LENGHT
        )

    return error_messages


def model_serializer_error_messages(
    fields: list, **error_messages_func_params
) -> dict:
    """
    Generate the
    Params:
        fields (list) -> list of the serailizer fields
    """
    return {
        k: v
        for k, v in zip(
            fields,
            [
                model_serializer_error_messages_formatter(
                    f, **error_messages_func_params
                )
                for f in fields
            ],
        )
    }
