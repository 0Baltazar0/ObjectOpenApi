from typing import Any
import unittest

from yaml import dump

from tests.types.smart_dataset_generator import generate_string, generate_string_bad


from objectopenapi.parse_errors import SchemaMismatch

from objectopenapi.types import StringType


class TestStringTypes(unittest.TestCase):
    good_datasets = generate_string()
    bad_datasets = generate_string_bad()

    @staticmethod
    def _enum(obj: Any, value: Any) -> None:
        obj.enum = value

    @staticmethod
    def _format(obj: Any, value: Any) -> None:
        obj.format = value

    @staticmethod
    def _pattern(obj: Any, value: Any) -> None:
        obj.pattern = value

    @staticmethod
    def _default(obj: Any, value: Any) -> None:
        obj.default = value

    @staticmethod
    def _bad_parse(dataset: Any):
        StringType(**dataset)
        print(f"Must raise on dataset {dataset}")

    def test_good_parse(self) -> None:
        for dataset in self.good_datasets:
            self.assertIsInstance(
                StringType(**dataset),
                StringType,
                "StringType could not be initiated",
            )

    def test_bad_parse(self) -> None:
        for bd in self.bad_datasets:
            self.assertRaises(SchemaMismatch, self._bad_parse, bd)

    def test_good_eq(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                StringType(**dataset),
                StringType(**dataset),
                f"Two instance must be equal,{dataset}",
            )

    def test_bad_eq(self) -> None:
        against = StringType(**self.good_datasets[0])
        for bd in self.good_datasets[1:]:
            self.assertNotEqual(
                against,
                StringType(**bd),
                f"Two instance must not be equal {bd} against {self.good_datasets[0]}",
            )

    def test_good_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = StringType(**dataset)
            enuma = ["EnumA"]
            TestStringTypes._enum(obj, enuma)
            TestStringTypes._format(obj, "RandomFormat")
            TestStringTypes._pattern(obj, "/restuff/")
            TestStringTypes._default(obj, "asdasd")
            self.assertEqual(obj.enum, enuma, "Enum assign does not work.")
            self.assertEqual(obj.format, "RandomFormat", "Format assign does not work.")
            self.assertEqual(obj.pattern, "/restuff/")
            self.assertEqual(obj.default, "asdasd")
            TestStringTypes._enum(obj, None)
            TestStringTypes._format(obj, None)
            TestStringTypes._pattern(obj, None)
            TestStringTypes._default(obj, None)
            self.assertEqual(obj.enum, None, "Enum assign does not work.")
            self.assertEqual(obj.format, None, "Format assign does not work.")
            self.assertEqual(obj.pattern, None)
            self.assertEqual(obj.default, None)

    def test_bad_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = StringType(**dataset)
            self.assertRaises(SchemaMismatch, lambda: TestStringTypes._enum(obj, 2))
            self.assertRaises(SchemaMismatch, lambda: TestStringTypes._format(obj, 2))
            self.assertRaises(SchemaMismatch, lambda: TestStringTypes._pattern(obj, 2))
            self.assertRaises(SchemaMismatch, lambda: TestStringTypes._default(obj, 2))

    def test_dump_yaml(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                dump(dataset),
                dump(StringType(**dataset).dump({})),
                f"Yaml dump must match original{dataset}",
            )
