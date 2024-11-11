import json
from os import path, walk


class SwaggerJSONBuilder:
    """This class builds JSON file documentation from multiple files.
    Description:
    Main file is index.json. Place there main information which can be not divided in smaller parts.
    Folders names such as "components", "paths" are keys in dictionary which will be used during merging
    If you have 1 file place it into folder with a proper key.

    Returns:
        [json]: Swagger UI JSON file
    """
    files_folder = "openapi"
    main_file = "index.json"

    @classmethod
    def _get_full_path(cls, relative_path):
        return path.join(path.dirname(__file__), cls.files_folder, relative_path)

    @staticmethod
    def _read_json_file(file_path):
        return json.load(open(file_path))

    @classmethod
    def _get_main_json(cls):
        full_path = cls._get_full_path(cls.main_file)
        return cls._read_json_file(full_path)

    @classmethod
    def _read_folders(cls, result, folders_info):
        # Get subfolders inside working directory
        folders = folders_info[0][1]

        for index, folder in enumerate(folders):
            files = folders_info[index + 1][2]  # Get files in subdirectoty

            partial_result = {}

            for file in files:
                # Get file path in subfolder
                file_path = cls._get_full_path(f"{folder}/{file}")
                # Read file and merge with orher file in subfolder
                partial_result.update(cls._read_json_file(file_path))

            # write to Swagger JSON the merged file from subfolder
            result[folder] = partial_result

        return result

    @classmethod
    def call(cls):
        result = cls._get_main_json()   # Get main json file and use it as the result
        # Get current path to walk though folders
        full_path = cls._get_full_path("")
        # Get informatiton about folders to merge json files from them
        folders_info = list(walk(full_path))
        # Get json files and merge them into one JSON file
        result = cls._read_folders(result, folders_info)
        return result
