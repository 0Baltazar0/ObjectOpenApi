from typing import Any
import unittest

from yaml import dump

from objectopenapi.utils.parse_errors import SchemaMismatch

from objectopenapi.data_types.types import FileType
from tests.types.smart_dataset_generator import generate_file, generate_file_bad


class TestFileType(unittest.TestCase):
    good_datasets = generate_file()
    bad_datasets = generate_file_bad()
    CC = FileType

    @staticmethod
    def _bad_parse(dataset: Any) -> None:
        TestFileType.CC(**dataset)
        print(f"Must raise on dataset {dataset}")

    def test_good_parse(self) -> None:
        for dataset in self.good_datasets:
            self.assertIsInstance(
                TestFileType.CC(**dataset),
                TestFileType.CC,
                "FileType could not be initiated",
            )

    def test_bad_parse(self) -> None:
        for bd in self.bad_datasets:
            self.assertRaises(SchemaMismatch, TestFileType._bad_parse, bd)

    def test_good_eq(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                TestFileType.CC(**dataset),
                TestFileType.CC(**dataset),
                f"Two instance must be equal,{dataset}",
            )

    def test_bad_eq(self) -> None:
        against = TestFileType.CC(**self.good_datasets[0])
        for bd in self.good_datasets[1:]:
            self.assertNotEqual(
                against,
                TestFileType.CC(**bd),
                f"Two instance must not be equal {bd} against {self.good_datasets[0]}",
            )

    @staticmethod
    def _format(object: Any, value: Any) -> None:
        object.format = value

    def test_good_assign(self) -> None:
        for dataset in self.good_datasets:
            set_a = TestFileType.CC(**dataset)
            self._format(set_a, "binary")
            self.assertEqual(
                set_a.format, "binary", "Format setter is not working @binary"
            )
            self._format(set_a, "base64")
            self.assertEqual(
                set_a.format, "base64", "Format setter is not working @base64"
            )

    def test_bad_assign(self) -> None:
        for bd in self.good_datasets:
            set_a = TestFileType.CC(**bd)
            self.assertRaises(SchemaMismatch, self._format, set_a, "dummy")

    def test_dump_yaml(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                dump(dataset),
                dump(TestFileType.CC(**dataset).dump({})),
                f"Yaml dump must match original{dataset}",
            )
