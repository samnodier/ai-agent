import os
from google.genai import types
import subprocess


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file given as path and optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="A python file that will be run which can be accessed relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments passed for the python file with a function that handles the user input",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="This is a math expression that will be solved",
                ),
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(wd_abs, file_path))

        is_valid_target_file_path = (
            os.path.commonpath([wd_abs, target_file_path]) == wd_abs
        )

        if not is_valid_target_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        absolute_file_path = os.path.abspath(target_file_path)
        command = ["python", absolute_file_path]

        # if any additional args were provided -> add them to the command
        if args:
            command.extend(args)

        # run the command
        process = subprocess.run(
            command, cwd=working_directory, capture_output=True, text=True, timeout=30
        )

        output_string = ""
        if not process:
            output_string = "Process exited with code X"
        elif process is None:
            output_string = "No output produced"
        else:
            output_string = f"STDOUT: {process.stdout}\nSTDERR: {process.stderr}"

        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"
