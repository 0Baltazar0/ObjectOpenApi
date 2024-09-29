from typing import Any
import unittest

from yaml import dump


from objectopenapi.parse_errors import SchemaMismatch

from objectopenapi.types import BooleanType
from .smart_dataset_generator import generate_boolean, generate_boolean_bad


class TestBooleanType(unittest.TestCase):
    good_datasets = generate_boolean()
    bad_datasets = generate_boolean_bad()

    def test_good_parse(self) -> None:
        for dataset in self.good_datasets:
            self.assertIsInstance(
                BooleanType(**dataset),
                BooleanType,
                "Boolean type could not be initiated",
            )

    def test_bad_parse(self) -> None:
        for bd in self.bad_datasets:
            self.assertRaises(
                SchemaMismatch,
                lambda: BooleanType(**bd),
            )

    def test_good_eq(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                BooleanType(**dataset),
                BooleanType(**dataset),
                f"Two instance must be equal,{dataset}",
            )

    def test_bad_eq(self) -> None:
        against = BooleanType(**self.good_datasets[0])
        for bd in self.good_datasets[1:]:
            self.assertNotEqual(
                against,
                BooleanType(**bd),
                f"Two instance must not be equal {bd} against {against}",
            )

    def test_good_assign(self) -> None:
        for dataset in self.good_datasets:
            instance = BooleanType(**dataset)
            instance.default = False
            self.assertEqual(instance.default, False)
            instance.default = True
            self.assertEqual(instance.default, True)
            instance.default = None
            self.assertEqual(instance.default, None)

    def test_bad_assign(self) -> None:
        for dataset in self.good_datasets:
            instance = BooleanType(**dataset)

            def _default(value: Any) -> None:
                instance.default = value

            self.assertRaises(SchemaMismatch, _default, 2)
            self.assertRaises(SchemaMismatch, _default, 0)
            self.assertRaises(SchemaMismatch, _default, "True")

    def test_dump_yaml(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                dump(dataset),
                dump(BooleanType(**dataset).dump({})),
                f"Yaml dump must match original{dataset}",
            )
