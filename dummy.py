class Contact:
    @property
    def var(self) -> int:
        return 1

    _var: stuff

    def __init__(self, **kwargs: Any) -> None:
        pass

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        return source
