import os
import sys
import tkinter as tk
from tkinter import filedialog
import time

# Ensure we can import from the package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from intelligent_file_compressor.core.compressor import Compressor
from intelligent_file_compressor.core.decompressor import Decompressor
from intelligent_file_compressor.storage.reader import IFCReader

def main():
    # 1. Initialize GUI (Hidden)
    root = tk.Tk()
    root.withdraw() # Hide the main window

    print("Please select a file from the dialog window...")
    
    # 2. Select File
    file_path = filedialog.askopenfilename(title="Select a file to Compress or Decompress")
    
    if not file_path:
        print("No file selected. Exiting.")
        return

    print(f"\nSelected: {file_path}")
    
    dir_name = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    
    # 3. Determine Mode
    if file_path.endswith(".ifc"):
        # DECOMPRESS
        print("Mode: DECOMPRESSION detected.")
        
        output_dir = os.path.join(dir_name, "decompressed_files")
        os.makedirs(output_dir, exist_ok=True)
        
        # Construct output filename (remove .ifc)
        original_name = file_name[:-4] 
        # If original name doesn't have extension, we might guess or just leave it.
        # Our compressor doesn't store original filename in metadata currently, 
        # so we rely on the user having kept the name or just stripping .ifc
        output_path = os.path.join(output_dir, original_name)
        
        try:
            start_time = time.time()
            d = Decompressor()
            d.decompress(file_path, output_path)
            duration = time.time() - start_time
            
            # Stats
            compressed_size = os.path.getsize(file_path)
            restored_size = os.path.getsize(output_path)
            
            print("\n" + "="*40)
            print("       DECOMPRESSION SUCCESSFUL")
            print("="*40)
            print(f"Input File:      {file_name}")
            print(f"Output File:     {os.path.basename(output_path)}")
            print(f"Location:        {os.path.abspath(output_dir)}")
            print("-" * 40)
            print(f"Compressed Size: {compressed_size:,} bytes")
            print(f"Restored Size:   {restored_size:,} bytes")
            print(f"Time Taken:      {duration:.4f} seconds")
            print("="*40)
            print(f"\n[INFO] File saved to: {os.path.abspath(output_path)}")
            
        except Exception as e:
            print(f"\nERROR: Decompression failed - {e}")

    else:
        # COMPRESS
        print("Mode: COMPRESSION detected.")
        
        # User requested "compressed files" folder (handling typo "compressed filed")
        output_dir = os.path.join(dir_name, "compressed_files")
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, file_name + ".ifc")
        
        try:
            start_time = time.time()
            c = Compressor()
            c.compress(file_path, output_path)
            duration = time.time() - start_time
            
            # Stats
            original_size = os.path.getsize(file_path)
            compressed_size = os.path.getsize(output_path)
            ratio = (1 - (compressed_size / original_size)) * 100
            
            print("\n" + "="*40)
            print("        COMPRESSION SUCCESSFUL")
            print("="*40)
            print(f"Input File:      {file_name}")
            print(f"Output File:     {os.path.basename(output_path)}")
            print(f"Location:        {os.path.abspath(output_dir)}")
            print("-" * 40)
            print(f"Original Size:   {original_size:,} bytes")
            print(f"Compressed Size: {compressed_size:,} bytes")
            print(f"Reduction:       {ratio:.2f}%")
            print(f"Time Taken:      {duration:.4f} seconds")
            print("="*40)
            print(f"\n[INFO] File saved to: {os.path.abspath(output_path)}")
            
        except ValueError as ve:
            print(f"\nERROR: {ve}")
            print("Supported formats: .json, .csv, .log, .txt, .md")
        except Exception as e:
            print(f"\nERROR: Compression failed - {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
    except Exception as e:
        print(f"\nUnexpected Error: {e}")
    
    input("\nPress Enter to exit...")
