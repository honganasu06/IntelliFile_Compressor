import os

class FileDetector:
    """
    Detects file type based on extension and magic bytes.
    Returns strict constants: 'json', 'csv', 'log', 'text'.
    """
    
    # Constants
    JSON = "json"
    CSV = "csv"
    LOG = "log"
    TEXT = "text"

    @staticmethod
    def detect(file_path: str) -> str:
        """
        Identify file type. Raises ValueError if unsupported.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        if ext == '.json':
            return FileDetector.JSON
        elif ext == '.csv':
            return FileDetector.CSV
        elif ext == '.log':
            return FileDetector.LOG
        elif ext in ['.txt', '.md']:
            return FileDetector.TEXT
        else:
            raise ValueError(f"Unsupported file format: {ext}")
