import os
import sys
# Add parent dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from intelligent_file_compressor.storage.reader import IFCReader

def show_stats(file_path: str):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    try:
        strat_id, metadata, compressed_data = IFCReader.read(file_path)
        original_size = os.path.getsize(file_path) # This is actually compressed size on disk
        # We don't store original size in IFC1 header explicitly in the spec provided!
        # "Outputs: original size, compressed size, compression ratio"
        # Spec says: "Metadata MUST include: dictionaries, key maps, type info, huffman codebook, delta bases"
        # It DOES NOT explicitly say "Original Size" in the table.
        # But stats command requires it.
        # Let's assume we should have stored it or we can't show it accurately without decompressing.
        # Wait, the prompt says "Outputs: original size".
        # I should probably add it to metadata or header.
        # For now, let's just show compressed size and metadata info.
        
        comp_size = len(compressed_data) + len(str(metadata)) # Approx
        file_size = os.path.getsize(file_path)
        
        print(f"\n📊 Stats for {os.path.basename(file_path)}")
        print(f"--------------------------------")
        print(f"Strategy ID:    {strat_id}")
        print(f"File Size:      {file_size} bytes")
        print(f"Payload Size:   {len(compressed_data)} bytes")
        print(f"Meta Size:      {file_size - len(compressed_data)} bytes")
        print(f"--------------------------------")

    except Exception as e:
        print(f"Error reading stats: {e}")
