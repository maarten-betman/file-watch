import os
import sys
from pathlib import Path

try:
    from pip import main as pipmain
except:
    from pip._internal import main as pipmain


class TestUtils:

    _name_external = "externals"
    _name_local = "test-data"

    @staticmethod
    def install_package(package: str):
        """Installs a package that is normally only used
        by a test configuration.

        Arguments:
            package {str} -- Name of the PIP package.
        """
        pipmain(["install", package])

    @staticmethod
    def get_local_test_data_dir(dir_name: str) -> Path:
        """
        Returns the desired directory relative to the test data.
        Avoiding extra code on the tests.
        """
        directory = TestUtils.get_test_data_dir(
            dir_name, TestUtils._name_local
        )
        return directory

    @staticmethod
    def get_external_test_data_dir(dir_name: str) -> Path:
        """
        Returns the desired directory relative to the test external data.
        Avoiding extra code on the tests.
        """
        directory = TestUtils.get_test_data_dir(
            dir_name, TestUtils._name_external
        )
        return directory

    @staticmethod
    def get_test_data_dir(dir_name: str, test_data_name: str) -> Path:
        """
        Returns the desired directory relative to the test external data.
        Avoiding extra code on the tests.
        """
        test_dir = Path(__file__).parent
        try:
            test_dir = test_dir / test_data_name / dir_name
        except:
            print("An error occurred trying to find {}".format(dir_name))
        return test_dir

    @staticmethod
    def get_test_dir(dir_name: str) -> Path:
        """Returns the desired directory inside the Tests folder

        Arguments:
            dir_name {str} -- Target directory.

        Returns:
            {str} -- Path to the target directory.
        """
        test_dir = Path(__file__).parent
        dir_path = test_dir / dir_name
        return dir_path

    @staticmethod
    def get_local_test_file(filepath: str) -> Path:
        """Gets the absolute Path for the given file name located in a local test directory.

        Args:
            filepath (str): Name of the file to search.

        Returns:
            Path: Found path.
        """
        return Path(__file__).parent / TestUtils._name_local / filepath
