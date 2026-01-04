import os


def get_files_info(working_directory, directory="."):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(wd_abs, directory))

        is_valid_target_dir = os.path.commonpath([wd_abs, target_dir]) == wd_abs

        if not is_valid_target_dir:
            f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not directory:
            f'Error: "{directory}" is not a directory'

        for item in os.listdir(target_dir):
            print(
                f"- {item}: file_size={os.path.getsize(item)} is_dir={os.path.isdir()}"
            )
    except Exception as e:
        return f"Error: {e}"
