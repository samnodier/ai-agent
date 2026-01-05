import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(wd_abs, directory))

        is_valid_target_dir = os.path.commonpath([wd_abs, target_dir]) == wd_abs

        if not is_valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        dir_items = []
        for item in os.listdir(target_dir):
            dir_items.append(
                f"  - {item}: file_size={os.path.getsize('/'.join([target_dir, item]))}, is_dir={os.path.isdir('/'.join([target_dir, item]))}"
            )

        return "\n".join(dir_items)

    except Exception as e:
        return f"Error: {e}"
