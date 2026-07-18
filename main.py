import pathlib 
import shutil
import csv
import logging
import json

logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    force="%(levelname)s %(message)s"
)

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

def get_search_mode():
    while True:
        print('''Search mode :
              1.Current folder only
              2.Current folder + subfolder''')
        mode = input("Chose(1/2):")
        if mode == '1':
            return False
        elif mode == '2':
            return True
        else :
            print("Invalid choice...")

def get_files(folder_path):
    files = []
    for file in folder_path.iterdir():
        if file.is_file():
            files.append(file)
    return files


def get_all_files(folder_path):
    files = []
    for file in folder_path.rglob("*"):
        if file.is_file():
            files.append(file)
    return files

def load_config(config_path):
    with open(config_path,"r") as file:
        config = json.load(file)
    return config
    
def get_file_type(files,config):
    file_type  = {}
    for file in files:
        suff = file.suffix.lower()
        suffix_folder = config.get(suff,"Other")
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
            logging.info(f"Moved {file_path.name}")
        except Exception as e :
            logging.info(f"Failed to move {file_path.name} : {e}")


        
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
    mode = get_search_mode()
    config = load_config("config.json")
    if mode :   
        files = get_all_files(folder_path)
    else:
        files = get_files(folder_path)
    file_info =get_file_type(files,config)
    move_file(file_info)
    report = create_report(file_info)
    output_path = folder_path / "report.csv"
    save_report(report, output_path)


if __name__ == "__main__":
    main()