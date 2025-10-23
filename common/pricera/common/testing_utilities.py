import os
from pathlib import Path
from typing import Optional, Union


def load_file_from_sub_folder(
    filename: str,
    base_dir: str = os.getcwd(),  # This gets the launch directory
    sub_folder: str = "test_cases",
    mode: str = "r",
    encoding: str = "utf-8",
) -> str:
    """
    Loads a file from a subfolder relative to the launch directory.

    :param filename: name of the file (e.g., "hotline_listings.html")
    :param base_dir: base directory (defaults to current working directory - launch dir)
    :param sub_folder: name of the subfolder (e.g., "test_cases")
    :param mode: file open mode (default: 'r')
    :param encoding: file encoding (default: 'utf-8')
    :return: file content as a string
    """
    file_path = os.path.join(base_dir, sub_folder, filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, mode, encoding=encoding) as f:
        return f.read()
