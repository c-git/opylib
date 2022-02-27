import ntpath
import os
from pathlib import Path


def mkdir(folder):
    Path(folder).mkdir(parents=True, exist_ok=True)


def change_filename_ext(fn: str, new_ext: str) -> str:
    """
    Returns the filename with the new extension
    :param fn: The filename with the old extension
    :param new_ext: The new extension to put on the filename
    :return: The filename with the new extension
    """
    result, _ = os.path.splitext(fn)
    return f'{result}{new_ext}'


def ensure_parent_folder_exists(fn: str):
    """
    Expects fn to be a file name. Removes the file name and ensures that
    it's parent folder exists
    :param fn: Filename to use to find parent folder
    :return:
    """
    folder, _ = ntpath.split(fn)
    mkdir(folder)


def ensure_output_folder_empty(folder):
    """
    Ensure that output exists and does not already contain files
    Usually used to ensure that output is not overwritten
    NB: If output folder does not already exist. It is created.
    :param folder:
    :return:
    """
    if os.path.exists(folder):
        listing = os.listdir(folder)
        if len(listing) > 0:
            raise Exception(
                f'Output Folder ("{folder}") is '
                f'not empty: {len(listing)} file(s) found')
    else:
        mkdir(folder)
