# IFC1 File Format

The Intelligent File Compressor uses a custom binary format `IFC1`.

## Structure

| Field | Size | Type | Description |
|---|---|---|---|
| **MAGIC** | 4 bytes | ASCII | `IFC1` |
| **VERSION** | 1 byte | uint8 | Format version (currently 1) |
| **STRATEGY** | 1 byte | uint8 | ID of the strategy used (1=JSON, 2=CSV, 3=LOG, 4=TEXT) |
| **META_LEN** | 4 bytes | uint32 | Length of the metadata block (Big Endian) |
| **METADATA** | Variable | JSON | JSON-serialized metadata (dictionaries, Huffman trees) |
| **DATA** | Variable | Bytes | The compressed binary payload |

## Strategy IDs
- 1: JSON
- 2: CSV
- 3: LOG
- 4: TEXT
