import os
import sys
import shutil
import json

# Add current directory to path
sys.path.append(os.getcwd())

from intelligent_file_compressor.core.compressor import Compressor
from intelligent_file_compressor.core.decompressor import Decompressor

def test_reproduction():
    print("Starting reproduction test...")
    
    # Setup test files
    test_dir = "test_repro_env"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    input_file = os.path.join(test_dir, "test_data.json")
    data = {"id": 1, "name": "Test", "values": [1, 2, 3, 4, 5]}
    with open(input_file, 'w') as f:
        json.dump(data, f)
        
    print(f"Created test file: {input_file}")
    
    # Simulate Interactive Runner Compression Logic
    file_path = os.path.abspath(input_file)
    dir_name = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    
    output_dir = os.path.join(dir_name, "compressed_files")
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, file_name + ".ifc")
    
    print(f"Attempting to compress to: {output_path}")
    
    try:
        c = Compressor()
        c.compress(file_path, output_path)
        print("Compression successful.")
    except Exception as e:
        print(f"Compression failed: {e}")
        return

    if not os.path.exists(output_path):
        print("ERROR: Compressed file not found at expected location!")
    else:
        print(f"Verified file exists at: {output_path}")

    # Simulate Interactive Runner Decompression Logic
    # The user selects the .ifc file
    selected_ifc_path = output_path
    ifc_dir_name = os.path.dirname(selected_ifc_path)
    ifc_file_name = os.path.basename(selected_ifc_path)
    
    decomp_output_dir = os.path.join(ifc_dir_name, "decompressed_files")
    # Note: In the original code, it creates decompressed_files inside the directory of the selected file.
    # If the selected file is in `compressed_files`, then `decompressed_files` will be inside `compressed_files`.
    
    os.makedirs(decomp_output_dir, exist_ok=True)
    
    original_name = ifc_file_name[:-4] # remove .ifc
    decomp_output_path = os.path.join(decomp_output_dir, original_name)
    
    print(f"Attempting to decompress to: {decomp_output_path}")
    
    try:
        d = Decompressor()
        d.decompress(selected_ifc_path, decomp_output_path)
        print("Decompression successful.")
    except Exception as e:
        print(f"Decompression failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_reproduction()
