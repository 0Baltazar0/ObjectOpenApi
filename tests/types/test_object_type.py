from typing import Any
import unittest

from yaml import dump

from tests.types.smart_dataset_generator import generate_object, generate_object_bad


from objectopenapi.utils.parse_errors import SchemaMismatch

from objectopenapi.data_types.types import ObjectType


class TestObjectTypes(unittest.TestCase):
    good_datasets = generate_object()
    bad_datasets = generate_object_bad()
    CC = ObjectType

    @staticmethod
    def _additionalProperties(obj: Any, value: Any) -> None:
        obj.additionalProperties = value

    @staticmethod
    def _minProperties(obj: Any, value: Any) -> None:
        obj.minProperties = value

    @staticmethod
    def _maxProperties(obj: Any, value: Any) -> None:
        obj.maxProperties = value

    @staticmethod
    def _properties(obj: Any, value: Any) -> None:
        obj.properties = value

    @staticmethod
    def _required(obj: Any, value: Any) -> None:
        obj.required = value

    @staticmethod
    def _bad_parse(dataset: Any) -> None:
        TestObjectTypes.CC(**dataset)
        print(f"Must raise on dataset {dataset}")

    def test_good_parse(self) -> None:
        for dataset in self.good_datasets:
            self.assertIsInstance(
                TestObjectTypes.CC(**dataset),
                TestObjectTypes.CC,
                "TestObjectTypes.CC could not be initiated",
            )

    def test_bad_parse(self) -> None:
        for bd in self.bad_datasets:
            self.assertRaises(SchemaMismatch, self._bad_parse, bd)

    def test_good_eq(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                TestObjectTypes.CC(**dataset),
                TestObjectTypes.CC(**dataset),
                f"Two instance must be equal,{dataset}",
            )

    def test_bad_eq(self) -> None:
        against = TestObjectTypes.CC(**self.good_datasets[0])
        for bd in self.good_datasets[1:]:
            self.assertNotEqual(
                against,
                TestObjectTypes.CC(**bd),
                f"Two instance must not be equal {bd} against {self.good_datasets[0]}",
            )

    def test_good_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = TestObjectTypes.CC(**dataset)
            TestObjectTypes._properties(obj, {"test": {"type": "string"}})
            TestObjectTypes._required(obj, ["test"])
            TestObjectTypes._additionalProperties(obj, True)
            TestObjectTypes._minProperties(obj, 7)
            TestObjectTypes._maxProperties(obj, 11)
            le_dump = {}
            props = obj.properties or {}
            for entry in props:
                le_dump[entry] = props[entry].dump({})
            self.assertEqual(
                dump(le_dump),
                dump({"test": {"type": "string"}}),
                "properties assign does not work.",
            )
            self.assertEqual(
                obj.additionalProperties,
                True,
                "additionalProperties assign does not work.",
            )
            self.assertEqual(
                obj.minProperties, 7, "minProperties assign does not work."
            )
            self.assertEqual(
                obj.maxProperties, 11, "maxProperties assign does not work."
            )
            self.assertEqual(
                obj.required, ["test"], "maxProperties assign does not work."
            )
            TestObjectTypes._additionalProperties(obj, False)
            self.assertEqual(
                obj.additionalProperties,
                False,
                "additionalProperties assign does not work.",
            )

    def test_bad_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = TestObjectTypes.CC(**dataset)
            self.assertRaises(
                SchemaMismatch, lambda: TestObjectTypes._properties(obj, 2)
            )
            self.assertRaises(
                SchemaMismatch, lambda: TestObjectTypes._additionalProperties(obj, 2)
            )
            self.assertRaises(
                SchemaMismatch, lambda: TestObjectTypes._minProperties(obj, "2")
            )
            self.assertRaises(
                SchemaMismatch, lambda: TestObjectTypes._maxProperties(obj, "2")
            )
            self.assertRaises(
                SchemaMismatch, lambda: TestObjectTypes._required(obj, "2")
            )

    def test_dump_yaml(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                dump(dataset),
                dump(TestObjectTypes.CC(**dataset).dump({})),
                f"Yaml dump must match original{dataset}",
            )
