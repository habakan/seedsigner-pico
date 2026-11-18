# The release build: the same modules, with boot.py and main.py frozen in
include("manifest.py")
module("boot.py", base_path="release")
module("main.py", base_path="release")
