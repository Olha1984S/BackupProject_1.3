"""Disk-space calculations for the selected backup destination."""
from pathlib import Path
import shutil
import config
import file_utils
from project_dataclasses import DiskSpaceInfo, SpaceInfo


def calculate_required_space(source_path, current_path):
    source_size = file_utils.get_directory_size(source_path)
    current_size = file_utils.get_directory_size(current_path) if Path(current_path).exists() else 0
    return SpaceInfo(source_size=source_size, current_size=current_size,
                     required_space=source_size + current_size)


def check_free_space(space_info, destination_path=None):
    destination = Path(destination_path or config.PROJECT_PATH)
    _, _, free_space = shutil.disk_usage(destination)
    return DiskSpaceInfo(free_space=free_space,
                         required_space=space_info.required_space,
                         enough_space=free_space >= space_info.required_space)
