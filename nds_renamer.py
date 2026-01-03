import os
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path



# Function to get game name by ROM serial
def get_game_name_by_serial(serial,root):
    for game in root.findall("game"):
        rom = game.find("rom")
        if rom is not None and rom.get("serial") == serial:
            return game.get("name")
    return None

def get_nds_game_code(nds_file_path):
    with open(nds_file_path, "rb") as f:
        f.seek(0x0C)  # Offset of the game code
        code_bytes = f.read(4)  # 4 bytes long
    return code_bytes.decode("ascii")


def process_nds_files(directory,root,clean_name,add_serial,excluded_dirs):
    """
    Recursively process all .nds files in the given directory and subdirectories.
    """
    if not os.path.isdir(directory):
        print(f"Directory '{directory}' does not exist.")
        return
    if directory in excluded_dirs or Path(directory).name in excluded_dirs:
        print(f"Directory '{directory}' is excluded.")
        return
    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)

        if os.path.isfile(path) and path.lower().endswith('.nds'):
            print(f"Processing .nds file: {path}")
            # Get the directory containing the file
            dir_path = os.path.dirname(path)
            try:
                serial = get_nds_game_code(path)
            except:
                print(f"WARNING : Not renaming as failed to retrieve serial. For {path}")

            print(f"    serial : {serial}")
            name = get_game_name_by_serial(serial,root)
            if name is None:
                print(f"WARNING : Not renaming as cannot find name for serial {serial}. For {path}")
                continue
            if clean_name:
                name_split=name.split('(')
                name=name_split[0].strip()
            if add_serial:
                name = f"{name} ({serial})"
            print(f"    name : {name}")
            
            good_nds_name = f"{dir_path}\\{name}.nds"
            good_sav_name = f"{dir_path}\\{name}.sav"
            current_nds_name = path
            path_without_extension = Path(current_nds_name).stem
            current_sav_name = f"{dir_path}\\{path_without_extension}.sav"

            if not (Path(current_nds_name).resolve() == Path(good_nds_name).resolve()):
                if os.path.exists(good_nds_name):
                    print(f"WARNING : Not renaming as a file with a good name already exists. Maybe caused by having 2 rom files with the same serial. For {path}")
                else:
                    print("Renaming '.nds'...")
                    os.rename(path, good_nds_name)
                    print("Renaming '.sav'...")
                    if os.path.exists(current_sav_name):
                        os.rename(current_sav_name, good_sav_name)
                    else :
                        print(f"WARNING : NO 'sav' for {path}")
            else:
                print(f"Not renaming as name is already good. For {path}")


        elif os.path.isdir(path):
            # Recursive call for subdirectory
            process_nds_files(path,root,clean_name,add_serial,excluded_dirs)
        else:
            # Ignore everything else
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recursively process .nds files in a directory.")
    parser.add_argument("--directory", required=True,type=str, help="Path to the directory to scan")
    parser.add_argument(
        "--excluded_dirs",
        nargs="*",
        default=[],
        help="Directories to exclude (relative or absolute paths)"
    )

    parser.add_argument("--xml_file", required=True,help="Path to the XML file containing the release names. Download from 'https://datomatic.no-intro.org/index.php?page=download&op=dat&s=28' (leave option default)")
    parser.add_argument(
        "--clean_name",
        action="store_true",
        help="clean name from unecessary region information"
    )
    parser.add_argument(
        "--add_serial",
        action="store_true",
        help="add serial number (internal rom identification present in file) to the filename"
    )
    args = parser.parse_args()
    
    # Load and parse the XML file
    tree = ET.parse(args.xml_file)
    root = tree.getroot()
    
    
    process_nds_files(args.directory,root,args.clean_name,args.add_serial,args.excluded_dirs)
