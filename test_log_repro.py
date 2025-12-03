import os
import sys
import shutil
from datetime import datetime

# Add current directory to path
sys.path.append(os.getcwd())

from intelligent_file_compressor.core.compressor import Compressor
from intelligent_file_compressor.core.decompressor import Decompressor

def test_log_reproduction():
    print("Starting Log reproduction test...")
    
    # Setup test files
    test_dir = "test_log_env"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    input_file = os.path.join(test_dir, "test.log")
    
    # Create sample log content
    log_lines = [
        "2023-10-27 10:00:00 INFO System started",
        "2023-10-27 10:00:05 WARN Low memory",
        "2023-10-27 10:00:10 ERROR Crash detected"
    ]
    
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(log_lines))
        
    print(f"Created test file: {input_file}")
    
    output_path = os.path.join(test_dir, "test.log.ifc")
    
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

    decomp_output_path = os.path.join(test_dir, "restored_test.log")
    
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
    with open(decomp_output_path, 'r', encoding='utf-8') as f:
        restored_content = f.read().strip()
        
    original_content = "\n".join(log_lines).strip()
    
    # Note: The reconstruction might slightly change formatting (e.g. spaces)
    # But semantic content should be same.
    # Our reconstructor does: f"{ts_str} {sev_str} {msg_str}".strip()
    # And replaces multiple spaces with single space.
    
    if restored_content == original_content:
        print("VERIFICATION SUCCESS: Restored data matches original.")
    else:
        print("VERIFICATION FAILED: Data mismatch.")
        print("Expected:\n", original_content)
        print("Got:\n", restored_content)

if __name__ == "__main__":
    test_log_reproduction()
