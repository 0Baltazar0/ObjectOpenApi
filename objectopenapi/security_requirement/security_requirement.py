from objectopenapi.utils.common_types import JSON_DICT


class SecurityRequirement:
    def __init__(self) -> None:
        pass

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        return source