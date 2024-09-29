from typing import Any
import unittest

from yaml import dump

from tests.types.smart_dataset_generator import (
    generate_bad_number_rules_float,
    generate_bad_number_rules_int,
    generate_good_number_rules_float,
    generate_good_number_rules_int,
)

from objectopenapi.utils.parse_errors import SchemaMismatch

from objectopenapi.data_types.types import NumberRules


def floatify(**kwargs) -> NumberRules[float]:  # type:ignore
    return NumberRules(number_type=float, **kwargs)


def intify(**kwargs) -> NumberRules[int]:  # type:ignore
    return NumberRules(number_type=int, **kwargs)


with open("res.json", "w") as out:
    import json

    json.dump(generate_good_number_rules_float(), out)


class TestNumberRulesFloat(unittest.TestCase):
    good_datasets = generate_good_number_rules_float()
    bad_datasets = generate_bad_number_rules_float()
    CC = floatify

    @staticmethod
    def _exclusiveMinimum(obj: Any, value: Any) -> None:
        obj.exclusiveMinimum = value

    @staticmethod
    def _exclusiveMaximum(obj: Any, value: Any) -> None:
        obj.exclusiveMaximum = value

    @staticmethod
    def _maximum(obj: Any, value: Any) -> None:
        obj.maximum = value

    @staticmethod
    def _minimum(obj: Any, value: Any) -> None:
        obj.minimum = value

    @staticmethod
    def _multipleOf(obj: Any, value: Any) -> None:
        obj.multipleOf = value

    @staticmethod
    def _bad_parse(dataset: Any) -> None:
        TestNumberRulesFloat.CC(**dataset)
        print(f"Must raise on dataset {dataset}")

    def test_good_parse(self) -> None:
        for dataset in self.good_datasets:
            self.assertIsInstance(
                TestNumberRulesFloat.CC(**dataset),
                NumberRules,
                f"{NumberRules} could not be initiated",
            )

    def test_bad_parse(self) -> None:
        for bd in self.bad_datasets:
            self.assertRaises(SchemaMismatch, self._bad_parse, bd)

    def test_good_eq(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                TestNumberRulesFloat.CC(**dataset),
                TestNumberRulesFloat.CC(**dataset),
                f"Two instance must be equal,{dataset}",
            )

    def test_bad_eq(self) -> None:
        against = TestNumberRulesFloat.CC(**self.good_datasets[0])
        for bd in self.good_datasets[1:]:
            self.assertNotEqual(
                against,
                TestNumberRulesFloat.CC(**bd),
                f"Two instance must not be equal {bd} against {self.good_datasets[0]}",
            )

    def test_good_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = TestNumberRulesFloat.CC(**dataset)
            TestNumberRulesFloat._exclusiveMinimum(obj, True)
            self.assertEqual(
                obj.exclusiveMinimum,
                True,
                "Setting _exclusiveMinimum does not work <setting to true>",
            )
            TestNumberRulesFloat._exclusiveMinimum(obj, False)
            self.assertEqual(
                obj.exclusiveMinimum,
                False,
                "Setting _exclusiveMinimum does not work <setting to False>",
            )
            TestNumberRulesFloat._exclusiveMinimum(obj, None)
            self.assertEqual(
                obj._exclusiveMinimum,
                None,
                "Setting _exclusiveMinimum does not work <setting to None>",
            )
            TestNumberRulesFloat._exclusiveMaximum(obj, True)
            self.assertEqual(
                obj.exclusiveMaximum,
                True,
                "Setting exclusiveMaximum does not work <setting to true>",
            )
            TestNumberRulesFloat._exclusiveMaximum(obj, False)
            self.assertEqual(
                obj.exclusiveMaximum,
                False,
                "Setting exclusiveMaximum does not work <setting to False>",
            )
            TestNumberRulesFloat._exclusiveMaximum(obj, None)
            self.assertEqual(
                obj.exclusiveMaximum,
                None,
                "Setting exclusiveMaximum does not work <setting to None>",
            )

            TestNumberRulesFloat._maximum(obj, 100)
            self.assertEqual(
                obj.maximum,
                100,
                "Setting maximum does not work <setting to 100>",
            )
            TestNumberRulesFloat._maximum(obj, 0.5)
            self.assertEqual(
                obj.maximum,
                0.5,
                "Setting maximum does not work <setting to 0.5>",
            )
            TestNumberRulesFloat._maximum(obj, None)
            self.assertEqual(
                obj.maximum,
                None,
                "Setting maximum does not work <setting to None>",
            )
            TestNumberRulesFloat._minimum(obj, 100)
            self.assertEqual(
                obj.minimum,
                100,
                "Setting minimum does not work <setting to 100>",
            )
            TestNumberRulesFloat._minimum(obj, 0.5)
            self.assertEqual(
                obj.minimum,
                0.5,
                "Setting minimum does not work <setting to 0.5>",
            )
            TestNumberRulesFloat._minimum(obj, None)
            self.assertEqual(
                obj.minimum,
                None,
                "Setting minimum does not work <setting to None>",
            )
            TestNumberRulesFloat._multipleOf(obj, 100)
            self.assertEqual(
                obj.multipleOf,
                100,
                "Setting multipleOf does not work <setting to 100>",
            )
            TestNumberRulesFloat._multipleOf(obj, 0.5)
            self.assertEqual(
                obj.multipleOf,
                0.5,
                "Setting multipleOf does not work <setting to 0.5>",
            )
            TestNumberRulesFloat._multipleOf(obj, None)
            self.assertEqual(
                obj.multipleOf,
                None,
                "Setting multipleOf does not work <setting to None>",
            )

    def test_bad_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = TestNumberRulesFloat.CC(**dataset)
            self.assertRaises(
                SchemaMismatch, TestNumberRulesFloat._exclusiveMaximum, obj, 0
            )
            self.assertRaises(
                SchemaMismatch, TestNumberRulesFloat._exclusiveMaximum, obj, "0"
            )
            self.assertRaises(
                SchemaMismatch, TestNumberRulesFloat._exclusiveMinimum, obj, 0
            )
            self.assertRaises(
                SchemaMismatch, TestNumberRulesFloat._exclusiveMinimum, obj, "0"
            )
            self.assertRaises(SchemaMismatch, TestNumberRulesFloat._minimum, obj, False)
            self.assertRaises(SchemaMismatch, TestNumberRulesFloat._minimum, obj, "0")
            self.assertRaises(SchemaMismatch, TestNumberRulesFloat._maximum, obj, False)
            self.assertRaises(SchemaMismatch, TestNumberRulesFloat._maximum, obj, "0")
            self.assertRaises(
                SchemaMismatch, TestNumberRulesFloat._multipleOf, obj, False
            )
            self.assertRaises(
                SchemaMismatch, TestNumberRulesFloat._multipleOf, obj, "0"
            )

    def test_dump_yaml(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                dump(dataset),
                dump(TestNumberRulesFloat.CC(**dataset).dump({})),
                f"Yaml dump must match original{dataset} <{NumberRules}>",
            )


class TestNumberRulesInt(unittest.TestCase):
    good_datasets = generate_good_number_rules_int()
    bad_datasets = generate_bad_number_rules_int()
    CC = intify

    @staticmethod
    def _exclusiveMinimum(obj: Any, value: Any) -> None:
        obj.exclusiveMinimum = value

    @staticmethod
    def _exclusiveMaximum(obj: Any, value: Any) -> None:
        obj.exclusiveMaximum = value

    @staticmethod
    def _maximum(obj: Any, value: Any) -> None:
        obj.maximum = value

    @staticmethod
    def _minimum(obj: Any, value: Any) -> None:
        obj.minimum = value

    @staticmethod
    def _multipleOf(obj: Any, value: Any) -> None:
        obj.multipleOf = value

    @staticmethod
    def _bad_parse(dataset: Any) -> None:
        TestNumberRulesFloat.CC(**dataset)
        print(f"Must raise on dataset {dataset}")

    def test_good_parse(self) -> None:
        for dataset in self.good_datasets:
            self.assertIsInstance(
                TestNumberRulesInt.CC(**dataset),
                NumberRules,
                f"{NumberRules} could not be initiated",
            )

    def test_bad_parse(self) -> None:
        for bd in self.bad_datasets:
            self.assertRaises(SchemaMismatch, self._bad_parse, bd)

    def test_good_eq(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                TestNumberRulesInt.CC(**dataset),
                TestNumberRulesInt.CC(**dataset),
                f"Two instance must be equal,{dataset}",
            )

    def test_bad_eq(self) -> None:
        against = TestNumberRulesInt.CC(**self.good_datasets[0])
        for bd in self.good_datasets[1:]:
            self.assertNotEqual(
                against,
                TestNumberRulesInt.CC(**bd),
                f"Two instance must not be equal {bd} against {self.good_datasets[0]}",
            )

    def test_good_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = TestNumberRulesInt.CC(**dataset)
            TestNumberRulesInt._exclusiveMinimum(obj, True)
            self.assertEqual(
                obj.exclusiveMinimum,
                True,
                "Setting _exclusiveMinimum does not work <setting to true>",
            )
            TestNumberRulesInt._exclusiveMinimum(obj, False)
            self.assertEqual(
                obj.exclusiveMinimum,
                False,
                "Setting _exclusiveMinimum does not work <setting to False>",
            )
            TestNumberRulesInt._exclusiveMinimum(obj, None)
            self.assertEqual(
                obj._exclusiveMinimum,
                None,
                "Setting _exclusiveMinimum does not work <setting to None>",
            )
            TestNumberRulesInt._exclusiveMaximum(obj, True)
            self.assertEqual(
                obj.exclusiveMaximum,
                True,
                "Setting exclusiveMaximum does not work <setting to true>",
            )
            TestNumberRulesInt._exclusiveMaximum(obj, False)
            self.assertEqual(
                obj.exclusiveMaximum,
                False,
                "Setting exclusiveMaximum does not work <setting to False>",
            )
            TestNumberRulesInt._exclusiveMaximum(obj, None)
            self.assertEqual(
                obj.exclusiveMaximum,
                None,
                "Setting exclusiveMaximum does not work <setting to None>",
            )

            TestNumberRulesInt._maximum(obj, 100)
            self.assertEqual(
                obj.maximum,
                100,
                "Setting maximum does not work <setting to 100>",
            )
            TestNumberRulesInt._maximum(obj, 0)
            self.assertEqual(
                obj.maximum,
                0,
                "Setting maximum does not work <setting to 0>",
            )
            TestNumberRulesInt._maximum(obj, None)
            self.assertEqual(
                obj.maximum,
                None,
                "Setting maximum does not work <setting to None>",
            )
            TestNumberRulesInt._minimum(obj, 100)
            self.assertEqual(
                obj.minimum,
                100,
                "Setting minimum does not work <setting to 100>",
            )
            TestNumberRulesInt._minimum(obj, 0)
            self.assertEqual(
                obj.minimum,
                0,
                "Setting minimum does not work <setting to 0>",
            )
            TestNumberRulesInt._minimum(obj, None)
            self.assertEqual(
                obj.minimum,
                None,
                "Setting minimum does not work <setting to None>",
            )
            TestNumberRulesInt._multipleOf(obj, 100)
            self.assertEqual(
                obj.multipleOf,
                100,
                "Setting multipleOf does not work <setting to 100>",
            )
            TestNumberRulesInt._multipleOf(obj, 0)
            self.assertEqual(
                obj.multipleOf,
                0,
                "Setting multipleOf does not work <setting to 0>",
            )
            TestNumberRulesInt._multipleOf(obj, None)
            self.assertEqual(
                obj.multipleOf,
                None,
                "Setting multipleOf does not work <setting to None>",
            )

    def test_bad_assign(self) -> None:
        for dataset in self.good_datasets:
            obj = TestNumberRulesInt.CC(**dataset)
            self.assertRaises(
                SchemaMismatch, TestNumberRulesInt._exclusiveMaximum, obj, 0
            )
            self.assertRaises(
                SchemaMismatch, TestNumberRulesInt._exclusiveMaximum, obj, "0"
            )
            self.assertRaises(
                SchemaMismatch, TestNumberRulesInt._exclusiveMinimum, obj, 0
            )
            self.assertRaises(
                SchemaMismatch, TestNumberRulesInt._exclusiveMinimum, obj, "0"
            )
            self.assertRaises(SchemaMismatch, TestNumberRulesInt._minimum, obj, False)
            self.assertRaises(SchemaMismatch, TestNumberRulesInt._minimum, obj, 0.5)
            self.assertRaises(SchemaMismatch, TestNumberRulesInt._minimum, obj, "0")
            self.assertRaises(SchemaMismatch, TestNumberRulesInt._maximum, obj, False)
            self.assertRaises(SchemaMismatch, TestNumberRulesInt._maximum, obj, 0.5)
            self.assertRaises(SchemaMismatch, TestNumberRulesInt._maximum, obj, "0")
            self.assertRaises(
                SchemaMismatch, TestNumberRulesInt._multipleOf, obj, False
            )
            self.assertRaises(SchemaMismatch, TestNumberRulesInt._multipleOf, obj, 0.5)
            self.assertRaises(SchemaMismatch, TestNumberRulesInt._multipleOf, obj, "0")

    def test_dump_yaml(self) -> None:
        for dataset in self.good_datasets:
            self.assertEqual(
                dump(dataset),
                dump(TestNumberRulesInt.CC(**dataset).dump({})),
                f"Yaml dump must match original{dataset} <{NumberRules}>",
            )
