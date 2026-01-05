import os
from google.genai import types


schema_write_file_content = types.FunctionDeclaration(
    name="write_file_content",
    description="Writes the provided content to the file_path provided an argument as well. Both file_path and content are provided and if the file path contains new directories which are not available, they will be created. As always this will overwrite the file if it already exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="A file in which the contents will be written",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents that will be written to the file in file_path",
            ),
        },
    ),
)


def write_file_content(working_directory, file_path, content):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(wd_abs, file_path))

        is_valid_target_file_path = (
            os.path.commonpath([wd_abs, target_file_path]) == wd_abs
        )

        if not is_valid_target_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{target_file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        with open(target_file_path, "w") as file:
            file.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
