from typing import Any
import unittest

from yaml import dump

from tests.types.smart_dataset_generator import (
    generate_bad_min_max,
    generate_good_min_max,
)


from objectopenapi.utils.parse_errors import SchemaMismatch
from objectopenapi.data_types.types import MinMaxLength


class TestMinMaxLength(unittest.TestCase):
    good_datasets = generate_good_min_max()
    bad_datasets = generate_bad_min_max()
    CC = MinMaxLength

    @staticmethod
    def _maxLength(obj: Any, value: Any) -> None:
        obj.maxLength = value

    @staticmethod
    def _minLength(obj: Any, value: Any) -> None:
        obj.minLength = value

    @staticmethod
    def _bad_parse(dataset: Any) -> None:
        TestMinMaxLength.CC(**dataset)
        print(f"Must raise on dataset {dataset}")

    def test_good_parse(self) -> None:
        for dataset in self.good_datasets:
            self.assertIsInstance(
                self.CC(**dataset),
                self.CC,
                f"{self.CC} could not be initiated",
            )

    def test_bad_parse(self) -> None:
        for bd in self.bad_datasets:
            self.assertRaises(SchemaMismatch, self._bad_parse, bd)

    def test_good_eq(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                self.CC(**dataset),
                self.CC(**dataset),
                f"Two instance must be equal,{dataset}",
            )

    def test_bad_eq(self) -> None:
        against = self.CC(**self.good_datasets[0])
        for bd in self.good_datasets[1:]:
            self.assertNotEqual(
                against,
                self.CC(**bd),
                f"Two instance must not be equal {bd} against {self.good_datasets[0]}",
            )

    def test_good_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = self.CC(**dataset)
            TestMinMaxLength._maxLength(obj, 100)
            self.assertEqual(
                obj.maxLength, 100, "Setting maxLength does not work <setting to 100>"
            )
            TestMinMaxLength._maxLength(obj, 150)
            self.assertEqual(
                obj.maxLength, 150, "Setting maxLength does not work <setting to 150>"
            )
            TestMinMaxLength._maxLength(obj, None)
            self.assertEqual(
                obj.maxLength, None, "Setting maxLength does not work <setting to None>"
            )
            TestMinMaxLength._minLength(obj, 100)
            self.assertEqual(
                obj.minLength,
                100,
                "Setting minLength does not work <setting to 100>",
            )
            TestMinMaxLength._minLength(obj, 150)
            self.assertEqual(
                obj.minLength,
                150,
                "Setting minLength does not work <setting to 150>",
            )
            TestMinMaxLength._minLength(obj, None)
            self.assertEqual(
                obj.minLength, None, "Setting minLength does not work <setting to None>"
            )

    def test_bad_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = self.CC(**dataset)
            self.assertRaises(SchemaMismatch, TestMinMaxLength._maxLength, obj, "2")
            self.assertRaises(SchemaMismatch, TestMinMaxLength._maxLength, obj, False)
            self.assertRaises(SchemaMismatch, TestMinMaxLength._minLength, obj, "2")
            self.assertRaises(SchemaMismatch, TestMinMaxLength._minLength, obj, False)

    def test_dump_yaml(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                dump(dataset),
                dump(self.CC(**dataset).dump({})),
                f"Yaml dump must match original{dataset} <{self.CC}>",
            )
