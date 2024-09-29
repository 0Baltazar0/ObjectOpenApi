import os
from typing import Any
import unittest

from yaml import dump

from tests.types.smart_dataset_generator import (
    generate_all_of,
    generate_all_of_bad,
)


from objectopenapi.utils.parse_errors import SchemaMismatch

from objectopenapi.data_types.types import AllOfType, StringType


class TestAllOfTypes(unittest.TestCase):
    good_datasets = generate_all_of()[
        :: 1 if os.environ.get("LONG_TEST", "False").lower() == "true" else 16
    ]
    bad_datasets = generate_all_of_bad()
    CC = AllOfType

    @staticmethod
    def _bad_parse(dataset: Any) -> None:
        TestAllOfTypes.CC(**dataset)
        print(f"Must raise on dataset {dataset}")

    @staticmethod
    def _allOf(obj: AllOfType, value: Any) -> None:
        obj.allOf = value

    def test_good_parse(self) -> None:
        for dataset in self.good_datasets:
            self.assertIsInstance(
                TestAllOfTypes.CC(**dataset),
                TestAllOfTypes.CC,
                "TestAllOfTypes.CC could not be initiated",
            )

    def test_bad_parse(self) -> None:
        for bd in self.bad_datasets:
            self.assertRaises(SchemaMismatch, self._bad_parse, bd)

    def test_good_eq(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                TestAllOfTypes.CC(**dataset),
                TestAllOfTypes.CC(**dataset),
                f"Two instance must be equal,{dataset}",
            )

    def test_bad_eq(self) -> None:
        against = TestAllOfTypes.CC(**self.good_datasets[0])
        for bd in self.good_datasets[1:]:
            self.assertNotEqual(
                against,
                TestAllOfTypes.CC(**bd),
                f"Two instance must not be equal {bd} against {self.good_datasets[0]}",
            )

    def test_good_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = TestAllOfTypes.CC(**dataset)
            TestAllOfTypes._allOf(obj, [{"type": "string"}])
            self.assertEqual(
                obj._allOf[0],
                StringType(**{"type": "string"}),
                "Changing the value of anyOf should be automatically parsed",
            )

    def test_bad_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = TestAllOfTypes.CC(**dataset)
            self.assertRaises(SchemaMismatch, lambda: TestAllOfTypes._allOf(obj, 2))
            self.assertRaises(SchemaMismatch, lambda: TestAllOfTypes._allOf(obj, None))

    def test_dump_yaml(self) -> None:
        if os.environ.get("ANY_OF_DUMP_TEST", "false").lower() != "true":
            return
        for dataset in self.good_datasets:
            self.assertEqual(
                dump(dataset),
                dump(TestAllOfTypes.CC(**dataset).dump({})),
                f"Yaml dump must match original{dataset}",
            )
