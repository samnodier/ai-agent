import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the contents of the file which can be found in relation to the working directory and ends with a string showing where the contents were truncated if the file contains more than MAX_CHARS",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="A file path to read the contents from relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory, file_path):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(wd_abs, file_path))

        is_valid_target_file_path = (
            os.path.commonpath([wd_abs, target_file_path]) == wd_abs
        )

        if not is_valid_target_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file_path, "r") as file:
            file_content_string = file.read(MAX_CHARS)
            if file.read(1):
                file_content_string += (
                    f' [...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return file_content_string

    except Exception as e:
        return f"Error: {e}"
