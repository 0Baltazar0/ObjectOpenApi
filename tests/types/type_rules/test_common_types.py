from typing import Any
import unittest

from tests.types.smart_dataset_generator import (
    generate_bad_common_keys,
    generate_common_keys,
)


from objectopenapi.parse_errors import SchemaMismatch

from objectopenapi.types import CommonKeys

from yaml import dump


class TestCommonKeys(unittest.TestCase):
    good_datasets = generate_common_keys()
    bad_datasets = generate_bad_common_keys()
    CC = CommonKeys

    @staticmethod
    def _nullable(obj: Any, value: Any) -> None:
        obj.nullable = value

    @staticmethod
    def _title(obj: Any, value: Any) -> None:
        obj.title = value

    @staticmethod
    def _bad_parse(dataset: Any):
        TestCommonKeys.CC(**dataset)
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
            TestCommonKeys._nullable(obj, False)
            self.assertEqual(
                obj.nullable, False, "Setting nullable does not work <setting to false>"
            )
            TestCommonKeys._nullable(obj, True)
            self.assertEqual(
                obj.nullable, True, "Setting nullable does not work <setting to true>"
            )
            TestCommonKeys._nullable(obj, None)
            self.assertEqual(
                obj.nullable, None, "Setting nullable does not work <setting to None>"
            )
            TestCommonKeys._title(obj, "Title A")
            self.assertEqual(
                obj.title,
                "Title A",
                "Setting nullable does not work <setting to Title A>",
            )
            TestCommonKeys._title(obj, "Title B")
            self.assertEqual(
                obj.title,
                "Title B",
                "Setting nullable does not work <setting to Title B>",
            )
            TestCommonKeys._title(obj, None)
            self.assertEqual(
                obj.title, None, "Setting nullable does not work <setting to None>"
            )

    def test_bad_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = self.CC(**dataset)
            self.assertRaises(SchemaMismatch, TestCommonKeys._title, obj, 2)
            self.assertRaises(SchemaMismatch, TestCommonKeys._title, obj, False)
            self.assertRaises(SchemaMismatch, TestCommonKeys._nullable, obj, 2)
            self.assertRaises(SchemaMismatch, TestCommonKeys._nullable, obj, "2")

    def test_dump_yaml(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                dump(dataset),
                dump(self.CC(**dataset).dump({})),
                f"Yaml dump must match original{dataset} <{self.CC}>",
            )


if __name__ == "__main__":
    unittest.main()
