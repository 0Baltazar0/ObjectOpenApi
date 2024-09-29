from typing import Any
import unittest

from yaml import dump

from tests.types.smart_dataset_generator import generate_array, generate_array_bad


from objectopenapi.utils.parse_errors import SchemaMismatch

from objectopenapi.data_types.types import ArrayType


class TestArrayTypes(unittest.TestCase):
    good_datasets = generate_array()
    bad_datasets = generate_array_bad()
    CC = ArrayType

    @staticmethod
    def _items(obj: Any, value: Any) -> None:
        obj.items = value

    @staticmethod
    def _uniqueItems(obj: Any, value: Any) -> None:
        obj.uniqueItems = value

    @staticmethod
    def _minItems(obj: Any, value: Any) -> None:
        obj.minItems = value

    @staticmethod
    def _maxItems(obj: Any, value: Any) -> None:
        obj.maxItems = value

    @staticmethod
    def _bad_parse(dataset: Any) -> None:
        TestArrayTypes.CC(**dataset)
        print(f"Must raise on dataset {dataset}")

    def test_good_parse(self) -> None:
        for dataset in self.good_datasets:
            self.assertIsInstance(
                TestArrayTypes.CC(**dataset),
                TestArrayTypes.CC,
                "TestArrayTypes.CC could not be initiated",
            )

    def test_bad_parse(self) -> None:
        for bd in self.bad_datasets:
            self.assertRaises(SchemaMismatch, self._bad_parse, bd)

    def test_good_eq(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                TestArrayTypes.CC(**dataset),
                TestArrayTypes.CC(**dataset),
                f"Two instance must be equal,{dataset}",
            )

    def test_bad_eq(self) -> None:
        against = TestArrayTypes.CC(**self.good_datasets[0])
        for bd in self.good_datasets[1:]:
            self.assertNotEqual(
                against,
                TestArrayTypes.CC(**bd),
                f"Two instance must not be equal {bd} against {self.good_datasets[0]}",
            )

    def test_good_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = TestArrayTypes.CC(**dataset)
            TestArrayTypes._items(obj, {"type": "string"})
            TestArrayTypes._uniqueItems(obj, True)
            TestArrayTypes._minItems(obj, 7)
            TestArrayTypes._maxItems(obj, 11)
            le_dump = obj.items.dump({})
            self.assertEqual(
                dump(le_dump), dump({"type": "string"}), "Items assign does not work."
            )
            self.assertEqual(obj.uniqueItems, True, "uniqueItems assign does not work.")
            self.assertEqual(obj.minItems, 7, "minItems assign does not work.")
            self.assertEqual(obj.maxItems, 11, "maxItems assign does not work.")
            TestArrayTypes._uniqueItems(obj, False)
            self.assertEqual(
                obj.uniqueItems, False, "uniqueItems assign does not work."
            )

    def test_bad_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = TestArrayTypes.CC(**dataset)
            self.assertRaises(SchemaMismatch, lambda: TestArrayTypes._items(obj, 2))
            self.assertRaises(
                SchemaMismatch, lambda: TestArrayTypes._uniqueItems(obj, 2)
            )
            self.assertRaises(
                SchemaMismatch, lambda: TestArrayTypes._minItems(obj, "2")
            )
            self.assertRaises(
                SchemaMismatch, lambda: TestArrayTypes._maxItems(obj, "2")
            )

    def test_dump_yaml(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                dump(dataset),
                dump(TestArrayTypes.CC(**dataset).dump({})),
                f"Yaml dump must match original{dataset}",
            )
