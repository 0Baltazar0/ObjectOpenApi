from copy import deepcopy
from datetime import datetime
import logging
from typing import Any

from ..tools import merge_dict

logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
)
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler(f"set_generator_{datetime.now().timestamp()}.log")
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

rootLogger.setLevel(logging.DEBUG)


def generate_datasets(
    requireds: list[list[dict[str, Any]]], optionals: list[list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    orig = the_chosen_one(requireds)
    rootLogger.debug(f"Originals created {orig=}")
    return the_chosen_one([orig] + optionals, True)


def the_chosen_one(
    optionals: list[list[dict[str, Any]]], do_empty: bool = False
) -> list[dict[str, Any]]:
    # Don't open, recursion inside

    rootLogger.debug(f"Recursion entered, {optionals=}")
    if len(optionals) == 0:
        return []
    elif len(optionals) == 1:
        return optionals[0]
    else:
        cp = deepcopy(optionals)
        cp.pop(0)
        sets = the_chosen_one(deepcopy(cp), do_empty)
        rootLogger.debug(f"Working on {optionals[0]=}, {cp=}, {sets=}")
        res = []
        for item in optionals[0]:
            rootLogger.debug(f"Working on {item=}")
            if do_empty:
                rootLogger.debug(f"Working on {item=}->Putting empty row")
                res.append(merge_dict(item))
            for subset in sets:
                rootLogger.debug(f"Working on {item=},merging {subset=}")
                res.append(merge_dict(item, subset))
        return res
