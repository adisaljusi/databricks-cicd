import glob
import os

from databricks_cli.sdk import JobsService


def get_file_paths(directory_path: str) -> list[str]:
    """Generates a list that contains the file paths of of all files in the directory
    provided in the argument `directory_path`.

    Args:
        `directory_path` (str): Directory path

    Returns:
        list[str]: List of all files of the provided directory as absolute paths
    """

    directory_path = directory_path.split("/")
    path = os.path.join(os.getcwd(), *directory_path, "*")
    file_paths = [
        os.path.abspath(file) for file in glob.glob(path) if os.path.isfile(file)
    ]

    return file_paths
