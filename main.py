import pathlib 
import shutil
import csv

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
        if file.is_file():
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
        suffix_folder = extension_map.get(suff,"Other")
        file_type[file] = suffix_folder
    return file_type


def move_file(file_info):
    for  file_path, folder_name in file_info.items():
        parent_folder = file_path.parent
        destination_folder = parent_folder/folder_name
        create_folder(destination_folder)
        destination_path = destination_folder/file_path.name
        try: 
            shutil.move(file_path,destination_path)
        except Exception as e :
            print("Could not move file:")
            print(file_path.name)
            print(f"Reason: {e}")


        
def create_folder(destination_folder):
     destination_folder.mkdir(parents = True , exist_ok = True)

def create_report(file_info):
    report ={}
    for folder_name in file_info.values():
       count = report.get(folder_name,0)
       count +=1
       report[folder_name]=count 
    return report


def save_report(report,output_path):
    with open(output_path,
          "w",
          newline="",
          encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Category","Count"])
        for category,count in report.items():
            writer.writerow([category,count])

    
def main():
    folder_path = get_folder_path()
    files = get_files(folder_path)
    file_info =get_file_type(files)
    move_file(file_info)
    report = create_report(file_info)
    output_path = folder_path / "report.csv"
    save_report(report, output_path)


if __name__ == "__main__":
    main()