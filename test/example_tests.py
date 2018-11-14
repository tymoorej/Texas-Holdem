import unittest

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)



class ExampleTestCase(unittest.TestCase):

    def __init__(self, *args):
        super().__init__(*args)

    def test_example(self):
        self.assertTrue(True)



if __name__ == "__main__":
    unittest.main()
