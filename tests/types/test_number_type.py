from typing import Any
import unittest

from yaml import dump

from tests.types.smart_dataset_generator import generate_number, generate_number_bad


from objectopenapi.parse_errors import SchemaMismatch

from objectopenapi.types import NumberType


class TestNumberType(unittest.TestCase):
    good_datasets = generate_number()
    bad_datasets = generate_number_bad()

    def test_good_parse(self) -> None:
        for dataset in self.good_datasets:
            self.assertIsInstance(
                NumberType(**dataset),
                NumberType,
                "NumberType could not be initiated",
            )

    def test_bad_parse(self) -> None:
        for bd in self.bad_datasets:
            self.assertRaises(
                SchemaMismatch,
                lambda: NumberType(**bd),
            )

    def test_good_eq(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                NumberType(**dataset),
                NumberType(**dataset),
                f"Two instance must be equal,{dataset}",
            )

    def test_bad_eq(self) -> None:
        against = NumberType(**self.good_datasets[0])
        for bd in self.good_datasets[1:]:
            self.assertNotEqual(
                against,
                NumberType(**bd),
                f"Two instance must not be equal {bd} against {self.good_datasets[0]}",
            )

    @staticmethod
    def _format(object: NumberType, value: Any) -> None:
        object.format = value

    def test_good_assign(self) -> None:
        for dataset in self.good_datasets:
            nt = NumberType(**dataset)
            self._format(nt, "float")
            self.assertEqual(
                nt.format,
                "float",
                f"Assign not working, for target 'int32' on {dataset=}",
            )
            self._format(nt, "double")
            self.assertEqual(
                nt.format,
                "double",
                f"Assign not working, for target 'double' on {dataset=}",
            )
            self._format(nt, None)
            self.assertEqual(
                nt.format,
                None,
                f"Assign not working, for target <None> on {dataset=}",
            )

    def test_bad_assign(self) -> None:
        for bd in self.good_datasets:
            set_a = NumberType(**bd)
            self.assertRaises(SchemaMismatch, self._format, set_a, "dummy")

    def test_dump_yaml(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                dump(dataset),
                dump(NumberType(**dataset).dump({})),
                f"Yaml dump must match original{dataset}",
            )
