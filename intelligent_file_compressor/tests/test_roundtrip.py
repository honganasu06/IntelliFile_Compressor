import unittest
import os
import json
from intelligent_file_compressor.core.compressor import Compressor
from intelligent_file_compressor.core.decompressor import Decompressor

class TestRoundTrip(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_rt.json"
        self.ifc_file = "test_rt.json.ifc"
        self.restored_file = "test_rt.json.restored"
        
        data = {"id": [1, 2, 3], "name": "Test"}
        with open(self.test_file, 'w') as f:
            json.dump(data, f)

    def tearDown(self):
        if os.path.exists(self.test_file): os.remove(self.test_file)
        if os.path.exists(self.ifc_file): os.remove(self.ifc_file)
        if os.path.exists(self.restored_file): os.remove(self.restored_file)

    def test_json_roundtrip(self):
        c = Compressor()
        c.compress(self.test_file, self.ifc_file)
        
        d = Decompressor()
        d.decompress(self.ifc_file, self.restored_file)
        
        with open(self.test_file, 'r') as f:
            orig = json.load(f)
        with open(self.restored_file, 'r') as f:
            restored = json.load(f)
            
        self.assertEqual(orig, restored)

if __name__ == '__main__':
    unittest.main()
