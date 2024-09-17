from typing import Any
import unittest

from yaml import dump

from tests.types.smart_dataset_generator import generate_int, generate_int_bad


from objectopenapi.parse_errors import SchemaMismatch


from objectopenapi.types import IntegerType


class TestIntegerType(unittest.TestCase):
    good_datasets = generate_int()
    bad_datasets = generate_int_bad()

    def test_good_parse(self) -> None:
        for dataset in self.good_datasets:
            self.assertIsInstance(
                IntegerType(**dataset),
                IntegerType,
                "IntegerType could not be initiated",
            )

    @staticmethod
    def _bad_parse(dataset: Any):
        IntegerType(**dataset)
        print(f"Must raise on dataset {dataset}")

    def test_bad_parse(self) -> None:
        for bd in self.bad_datasets:
            self.assertRaises(SchemaMismatch, self._bad_parse, bd)

    def test_good_eq(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                IntegerType(**dataset),
                IntegerType(**dataset),
                f"Two instance must be equal,{dataset}",
            )

    def test_bad_eq(self) -> None:
        against = IntegerType(**self.good_datasets[0])
        for bd in self.good_datasets[1:]:
            self.assertNotEqual(
                against,
                IntegerType(**bd),
                f"Two instance must not be equal {bd} against {self.good_datasets[0]}",
            )

    @staticmethod
    def _format(object: IntegerType, value: Any) -> None:
        object.format = value

    def test_good_assign(self) -> None:
        for dataset in self.good_datasets:
            nt = IntegerType(**dataset)
            self._format(nt, "int32")
            self.assertEqual(
                nt.format,
                "int32",
                f"Assign not working, for target 'int32' on {dataset=}",
            )
            self._format(nt, "int64")
            self.assertEqual(
                nt.format,
                "int64",
                f"Assign not working, for target 'int64' on {dataset=}",
            )
            self._format(nt, None)
            self.assertEqual(
                nt.format,
                None,
                f"Assign not working, for target <None> on {dataset=}",
            )

    def test_bad_assign(self) -> None:
        for bd in self.good_datasets:
            set_a = IntegerType(**bd)
            self.assertRaises(SchemaMismatch, self._format, set_a, "dummy")

    def test_dump_yaml(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                dump(dataset),
                dump(IntegerType(**dataset).dump({})),
                f"Yaml dump must match original{dataset}",
            )
