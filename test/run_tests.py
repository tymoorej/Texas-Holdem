import os
import unittest


def main():
    loader = unittest.defaultTestLoader
    tests = loader.discover(os.path.dirname(os.path.realpath(__file__)), '*test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if not result.wasSuccessful():
        exit(1)


if __name__ == '__main__':
    main()


