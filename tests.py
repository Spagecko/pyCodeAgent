import unittest
import sys
from functions.get_files_info import get_files_info

class Test_get_files_info(unittest.TestCase):
    print(get_files_info("calculator", "."))
    print(get_files_info("calculator", "../"))
    print(get_files_info("calculator", "pkg"))

    sys.exit(0)

