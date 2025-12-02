import os

root_dir = "intelligent_file_compressor"

for dirpath, dirnames, filenames in os.walk(root_dir):
    init_path = os.path.join(dirpath, "__init__.py")
    print(f"Fixing {init_path}...")
    with open(init_path, "w", encoding="utf-8") as f:
        f.write("# init\n")

print("All __init__.py files fixed.")
