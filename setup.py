import os

from set_bing_wallpaper import SAVE_PATH

GREEN = "\033[92m"
RESET = "\033[0m"

def set_start_up():
    """
    Set the script to run on start up.
    """
    print(f"save path is {SAVE_PATH}")
    # create the bat file
    bat_path = os.path.join(SAVE_PATH, "run_set_wallpaper.bat")
    with open(bat_path, "w") as bat_file:
        bat_file.write("@echo off\n")
        bat_file.write(f"python {SAVE_PATH}\set_bing_wallpaper.py")
    
    # create the vbs file
    vbs_path = os.path.join(SAVE_PATH, "run_set_wallpaper.vbs")
    with open(vbs_path, "w") as vbs_file:
        vbs_file.write("Set WshShell = CreateObject(\"WScript.Shell\")\n")
        vbs_file.write(f"WshShell.Run \"{SAVE_PATH}\\run_set_wallpaper.bat\",0\n")

    # copy the vbs file to the startup folder
    os.system(f"copy {vbs_path} \"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\"")

    # ANSI escape codes for green text
    print(f"{GREEN}***** DONE! Script set to run on start up. *****{RESET}")

    

if __name__ == "__main__":
    set_start_up()