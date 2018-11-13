import unittest


class StateTestCase(unittest.TestCase):

    def __init__(self, *args):
        super().__init__(*args)

    def test_example(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
