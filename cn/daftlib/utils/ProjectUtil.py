import os

class ProjectUtil:

    @staticmethod
    def cleanPythonCache(folder_path:str) -> None:

        for root, dirs, files in os.walk(folder_path):
            for name in files:
                if name.endswith('.pyc'):
                    file_path = os.path.join(root, name)
                    print(f"Deleting file {file_path}")
                    try:
                        os.remove(file_path)
                    except OSError as error:
                        print(error)

        for root, dirs, files in os.walk(folder_path):
            for name in dirs:
                if name == '__pycache__':
                    dir_path = os.path.join(root, name)
                    print(f"Deleting directory {dir_path}")
                    try:
                        # shutil.rmtree(dir_path)
                        os.rmdir(dir_path)
                    except OSError as error:
                        print(error)