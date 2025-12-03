import os
import sys
import shutil
import csv

# Add current directory to path
sys.path.append(os.getcwd())

from intelligent_file_compressor.core.compressor import Compressor
from intelligent_file_compressor.core.decompressor import Decompressor

def test_csv_reproduction():
    print("Starting CSV reproduction test...")
    
    # Setup test files
    test_dir = "test_csv_env"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    input_file = os.path.join(test_dir, "test_data.csv")
    data = [
        ["id", "name", "value"],
        [1, "Alice", 100],
        [2, "Bob", 200],
        [3, "Charlie", 300]
    ]
    
    with open(input_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
        
    print(f"Created test file: {input_file}")
    
    output_path = os.path.join(test_dir, "test_data.csv.ifc")
    
    print(f"Attempting to compress to: {output_path}")
    
    try:
        c = Compressor()
        c.compress(input_file, output_path)
        print("Compression successful.")
    except Exception as e:
        print(f"Compression failed: {e}")
        import traceback
        traceback.print_exc()
        return

    if not os.path.exists(output_path):
        print("ERROR: Compressed file not found!")
        return

    decomp_output_path = os.path.join(test_dir, "restored_test_data.csv")
    
    print(f"Attempting to decompress to: {decomp_output_path}")
    
    try:
        d = Decompressor()
        d.decompress(output_path, decomp_output_path)
        print("Decompression successful.")
    except Exception as e:
        print(f"Decompression failed: {e}")
        import traceback
        traceback.print_exc()
        return
        
    # Verify content
    with open(decomp_output_path, 'r', newline='') as f:
        reader = csv.reader(f)
        restored_data = list(reader)
        
    # Convert restored data numbers back to int for comparison if needed, 
    # but CSV reader reads strings.
    # Our original data had ints, but writing to CSV makes them strings.
    # So we should compare string representations.
    
    expected_data = [[str(c) for c in row] for row in data]
    
    if restored_data == expected_data:
        print("VERIFICATION SUCCESS: Restored data matches original.")
    else:
        print("VERIFICATION FAILED: Data mismatch.")
        print("Expected:", expected_data)
        print("Got:", restored_data)

if __name__ == "__main__":
    test_csv_reproduction()
