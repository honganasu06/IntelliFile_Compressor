import time
import tracemalloc
import os
import sys
from intelligent_file_compressor.core.compressor import Compressor
from intelligent_file_compressor.core.decompressor import Decompressor
import filecmp

def benchmark(input_file, output_file):
    print(f"Benchmarking compression of {input_file}...")
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    tracemalloc.start()
    start_time = time.time()
    
    compressor = Compressor()
    compressor.compress(input_file, output_file)
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    input_size = os.path.getsize(input_file)
    output_size = os.path.getsize(output_file)
    
    print(f"\n--- Results ---")
    print(f"Time: {end_time - start_time:.4f} seconds")
    print(f"Peak Memory: {peak / 1024 / 1024:.2f} MB")
    print(f"Input Size: {input_size / 1024:.2f} KB")
    print(f"Output Size: {output_size / 1024:.2f} KB")
    print(f"Ratio: {output_size / input_size * 100:.2f}%")

    # Verification
    print("\nVerifying...")
    decompressed_file = input_file + ".restored"
    decompressor = Decompressor()
    decompressor.decompress(output_file, decompressed_file)
    
    if filecmp.cmp(input_file, decompressed_file, shallow=False):
        print("SUCCESS: Decompressed file matches original.")
    else:
        print("FAILURE: Decompressed file does NOT match original.")

if __name__ == "__main__":
    input_path = "intelligent_file_compressor/examples/story.txt"
    output_path = "intelligent_file_compressor/examples/story.ifc"
    benchmark(input_path, output_path)
