import pathlib 
import shutil


def get_folder_path():
    while True:
        path_str = input("Enter your folder path:")
        path = pathlib.Path(path_str)
        if path.exists():
            if path.is_dir():
                return path
            else:
                print("Your path is not a directory")
                continue
        else:
            print("The path does not exist")
            continue


def get_files(folder_path):
    files = []
    for file in folder_path.iterdir():
        if file.isfile():
            files.append(file)
    return files

def get_file_type(files):
    file_type  = {}
    extension_map = {
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".pdf": "Documents",
    ".mp4": "Videos",
    ".mp3": "Music"
    }
    for file in files:
        suff = file.suffix.lower()
        suffix_folder = extension_map.get(suff,"Others")
        file_type[file] = suffix_folder
    return file_type


def move_file(file_info):
    for  file_path, folder_name in file_info.items():
        parent_folder = file_path.parent
        destination_folder = parent_folder/folder_name
        create_folder(destination_folder)
        destination_path = destination_folder/file_path.name
        shutil.move(file_path,destination_path)


        
def create_folder(destination_folder):
     destination_folder.mkdir(parents = True , exist_ok = True)

def create_report():
    pass
get_folder_path()