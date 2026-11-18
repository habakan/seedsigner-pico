# The release build: manifest.py's modules but the port's _boot.py, with ours, boot.py and main.py frozen in
freeze("$(PORT_DIR)/modules", "rp2.py")
freeze("../build/pico/py")
module("_boot.py", base_path="release")
module("boot.py", base_path="release")
module("main.py", base_path="release")
