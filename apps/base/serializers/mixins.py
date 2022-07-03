# external imports
from rest_framework.fields import Field


class RequiredMessageSerializerMixin:
    def get_fields(self):
        fields = super().get_fields()

        for field_name, field in fields.items():
            field: Field = field
            error_messages = field.error_messages
            default_error_messages = field.default_error_messages

            validated_field_name: str = (
                field_name[0].upper() + field_name[1:]
            ).replace("_", " ")

            # if the field is blank
            error_messages.update(
                {"blank": f"{validated_field_name} may not be blank"}
            )

            # if the field is required
            if field.required:
                error_messages.update(
                    {
                        "required": f"{validated_field_name} field may not be blank."
                    }
                )

        return fields
