import sys
import os
import argparse

# Add parent dir to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from intelligent_file_compressor.core.compressor import Compressor
from intelligent_file_compressor.core.decompressor import Decompressor
from intelligent_file_compressor.cli.stats import show_stats

def main():
    parser = argparse.ArgumentParser(description="Intelligent File Compressor")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Compress
    compress_parser = subparsers.add_parser("compress", help="Compress a file")
    compress_parser.add_argument("file", help="File to compress")

    # Decompress
    decompress_parser = subparsers.add_parser("decompress", help="Decompress an .ifc file")
    decompress_parser.add_argument("file", help="File to decompress")

    # Stats
    stats_parser = subparsers.add_parser("stats", help="Show file statistics")
    stats_parser.add_argument("file", help=".ifc file to analyze")

    args = parser.parse_args()

    if args.command == "compress":
        output_file = args.file + ".ifc"
        if len(sys.argv) > 3: # Allow custom output
             # Simple hack for now, argparse handles it if we add argument
             pass
             
        c = Compressor()
        try:
            c.compress(args.file, output_file)
        except Exception as e:
            print(f"Compression failed: {e}")
        
    elif args.command == "decompress":
        if not args.file.endswith(".ifc"):
            print("Error: Input file must be .ifc")
            return
        output_file = args.file.replace(".ifc", ".restored")
        d = Decompressor()
        try:
            d.decompress(args.file, output_file)
        except Exception as e:
            print(f"Decompression failed: {e}")
        
    elif args.command == "stats":
        show_stats(args.file)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
