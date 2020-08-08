import subprocess
import glob
import os
import argparse

ui_files = glob.glob("*.ui")

parser = argparse.ArgumentParser()
parser.add_argument("--use_git", action="store_true")
args = parser.parse_args()

changed_ui_files = []
for ui_file in ui_files:
    # Uncomment for force rebuild all
    if args.use_git:
        output = subprocess.check_output(["git", "status", ui_file])
        output_lines = output.decode('utf-8').split('\n')
        for line in output_lines:
            if "modified" in line:
                changed_ui_files.append(ui_file)
                break
    else:
        changed_ui_files.append(ui_file)

for changed_ui_file in changed_ui_files:
    base, ext = os.path.splitext(changed_ui_file)
    # This should be the standard Anaconda3 pyuic5.bat location
    # Change it if yours is different.
    print(f"Building: {base}.ui -> {base}.py")
    subprocess.run([r'C:\Users\wparsons\anaconda3\Library\bin\pyuic5.bat', changed_ui_file, ">", base + ".py"])
