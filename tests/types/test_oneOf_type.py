import os
from typing import Any
import unittest

from yaml import dump

from tests.types.smart_dataset_generator import (
    generate_one_of,
    generate_one_of_bad,
)


from objectopenapi.parse_errors import SchemaMismatch

from objectopenapi.types import OneOfType, StringType


class TestOneOfTypes(unittest.TestCase):
    good_datasets = generate_one_of()[
        :: 1 if os.environ.get("LONG_TEST", "False").lower() == "true" else 16
    ]
    bad_datasets = generate_one_of_bad()
    CC = OneOfType

    @staticmethod
    def _bad_parse(dataset: Any):
        TestOneOfTypes.CC(**dataset)
        print(f"Must raise on dataset {dataset}")

    @staticmethod
    def _oneOf(obj: OneOfType, value: Any):
        obj.oneOf = value

    def test_good_parse(self) -> None:
        for dataset in self.good_datasets:
            self.assertIsInstance(
                TestOneOfTypes.CC(**dataset),
                TestOneOfTypes.CC,
                "TestOneOfTypes.CC could not be initiated",
            )

    def test_bad_parse(self) -> None:
        for bd in self.bad_datasets:
            self.assertRaises(SchemaMismatch, self._bad_parse, bd)

    def test_good_eq(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                TestOneOfTypes.CC(**dataset),
                TestOneOfTypes.CC(**dataset),
                f"Two instance must be equal,{dataset}",
            )

    def test_bad_eq(self) -> None:
        against = TestOneOfTypes.CC(**self.good_datasets[0])
        for bd in self.good_datasets[1:]:
            self.assertNotEqual(
                against,
                TestOneOfTypes.CC(**bd),
                f"Two instance must not be equal {bd} against {self.good_datasets[0]}",
            )

    def test_good_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = TestOneOfTypes.CC(**dataset)
            TestOneOfTypes._oneOf(obj, [{"type": "string"}])
            self.assertEqual(
                obj.oneOf[0],
                StringType(**{"type": "string"}),
                "Changing the value of anyOf should be automatically parsed",
            )

    def test_bad_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = TestOneOfTypes.CC(**dataset)
            self.assertRaises(SchemaMismatch, lambda: TestOneOfTypes._oneOf(obj, 2))
            self.assertRaises(SchemaMismatch, lambda: TestOneOfTypes._oneOf(obj, None))

    def test_dump_yaml(self) -> None:
        if os.environ.get("ANY_OF_DUMP_TEST", "false").lower() != "true":
            return
        for dataset in self.good_datasets:
            self.assertEqual(
                dump(dataset),
                dump(TestOneOfTypes.CC(**dataset).dump({})),
                f"Yaml dump must match original{dataset}",
            )
