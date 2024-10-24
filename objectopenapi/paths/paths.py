from copy import deepcopy
import os
from typing import Any, Optional
from objectopenapi.operation.operation import Operation
from objectopenapi.parameter.parameter import Parameter, ParseParameter
from objectopenapi.reference.reference import Reference
from objectopenapi.server.server import Server
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch
from objectopenapi.utils.validator import is_value_type, validate_key_type


class PathItem:
    _ref: Optional[str] = None

    @property
    def ref(self) -> Optional[str]:
        return self._ref

    @ref.setter
    def ref(self, value: Optional[str]) -> None:
        self._ref = value

    _summary: Optional[str] = None

    @property
    def summary(self) -> Optional[str]:
        return self._summary

    @summary.setter
    def summary(self, value: Optional[str]) -> None:
        self._summary = value

    _description: Optional[str] = None

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    _get: Optional[Operation] = None

    @property
    def get(self) -> Optional[Operation]:
        return self._get

    @get.setter
    def get(self, value: Optional[Operation]) -> None:
        self._get = value

    _post: Optional[Operation] = None

    @property
    def post(self) -> Optional[Operation]:
        return self._post

    @post.setter
    def post(self, value: Optional[Operation]) -> None:
        self._post = value

    _delete: Optional[Operation] = None

    @property
    def delete(self) -> Optional[Operation]:
        return self._delete

    @delete.setter
    def delete(self, value: Optional[Operation]) -> None:
        self._delete = value

    _options: Optional[Operation] = None

    @property
    def options(self) -> Optional[Operation]:
        return self._options

    @options.setter
    def options(self, value: Optional[Operation]) -> None:
        self._options = value

    _head: Optional[Operation] = None

    @property
    def head(self) -> Optional[Operation]:
        return self._head

    @head.setter
    def head(self, value: Optional[Operation]) -> None:
        self._head = value

    _patch: Optional[Operation] = None

    @property
    def patch(self) -> Optional[Operation]:
        return self._patch

    @patch.setter
    def patch(self, value: Optional[Operation]) -> None:
        self._patch = value

    _trace: Optional[Operation] = None

    @property
    def trace(self) -> Optional[Operation]:
        return self._trace

    @trace.setter
    def trace(self, value: Optional[Operation]) -> None:
        self._trace = value

    _servers: Optional[list[Server]] = None

    @property
    def servers(self) -> Optional[list[Server]]:
        return self._servers

    @servers.setter
    def servers(self, value: Optional[list[Server]]) -> None:
        self._servers = value

    _parameters: Optional[list[Parameter | Reference]] = None

    @property
    def parameters(self) -> Optional[list[Parameter | Reference]]:
        return self._parameters

    @parameters.setter
    def parameters(self, value: Optional[list[Parameter | Reference]]) -> None:
        self._parameters = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "ref" in kwargs:
            self._ref = validate_key_type("ref", str, {"ref": kwargs["ref"]})
        if "summary" in kwargs:
            self._summary = validate_key_type(
                "summary", str, {"summary": kwargs["summary"]}
            )
        if "description" in kwargs:
            self._description = validate_key_type(
                "description", str, {"description": kwargs["description"]}
            )
        if "get" in kwargs:
            if not isinstance(kwargs["get"], dict):
                raise SchemaMismatch("Path Item, 'get' object must be a dict")
            self._get = Operation(**kwargs["get"])
        if "post" in kwargs:
            if not isinstance(kwargs["post"], dict):
                raise SchemaMismatch("Path Item, 'post' object must be a dict")
            self._post = Operation(**kwargs["post"])
        if "delete" in kwargs:
            if not isinstance(kwargs["delete"], dict):
                raise SchemaMismatch("Path Item, 'delete' object must be a dict")
            self._delete = Operation(**kwargs["delete"])
        if "options" in kwargs:
            if not isinstance(kwargs["options"], dict):
                raise SchemaMismatch("Path Item, 'options' object must be a dict")
            self._options = Operation(**kwargs["options"])
        if "head" in kwargs:
            if not isinstance(kwargs["head"], dict):
                raise SchemaMismatch("Path Item, 'head' object must be a dict")
            self._head = Operation(**kwargs["head"])
        if "patch" in kwargs:
            if not isinstance(kwargs["patch"], dict):
                raise SchemaMismatch("Path Item, 'patch' object must be a dict")
            self._patch = Operation(**kwargs["patch"])
        if "trace" in kwargs:
            if not isinstance(kwargs["trace"], dict):
                raise SchemaMismatch("Path Item, 'trace' object must be a dict")
            self._trace = Operation(**kwargs["trace"])
        if "servers" in kwargs:
            if not isinstance(kwargs["servers"], list):
                raise SchemaMismatch("Path Item, 'server' object must be a list")
            self._servers = [
                Server(**s)
                for s in kwargs["servers"]
                if isinstance(s, dict) and is_value_type(s, dict)
            ]
        if "parameters" in kwargs:
            if not isinstance(kwargs["parameters"], list):
                raise SchemaMismatch(
                    f"Path Item, 'parameters' object must be a list, is {type(kwargs['parameters'])}"
                )
            self._parameters = []
            for parameter in kwargs["parameters"]:
                if not isinstance(parameter, dict):
                    raise SchemaMismatch(
                        f"Path Item, each 'parameter' inside 'parameters' must a dict, is {type(parameter)}"
                    )
                try:
                    ref = Reference(**parameter)
                    self._parameters.append(ref)
                    continue
                except Exception as refException:
                    try:
                        par = ParseParameter(**parameter)
                        self._parameters.append(par)
                    except Exception as error:
                        raise SchemaMismatch(
                            f"Path Item, parsing a parameter object has raised an {error=}, {refException=}"
                        )

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        if self.ref is not None:
            source["ref"] = self.ref
        elif remove_unset:
            source.pop("ref", None)
        if self.summary is not None:
            source["summary"] = self.summary
        elif remove_unset:
            source.pop("summary", None)
        if self.description is not None:
            source["description"] = self.description
        elif remove_unset:
            source.pop("description", None)
        if self.get is not None:
            source["get"] = self.get.dump({})
        elif remove_unset:
            source.pop("get", None)
        if self.post is not None:
            source["post"] = self.post.dump({})
        elif remove_unset:
            source.pop("post", None)
        if self.delete is not None:
            source["delete"] = self.delete.dump({})
        elif remove_unset:
            source.pop("delete", None)
        if self.options is not None:
            source["options"] = self.options.dump({})
        elif remove_unset:
            source.pop("options", None)
        if self.head is not None:
            source["head"] = self.head.dump({})
        elif remove_unset:
            source.pop("head", None)
        if self.patch is not None:
            source["patch"] = self.patch.dump({})
        elif remove_unset:
            source.pop("patch", None)
        if self.trace is not None:
            source["trace"] = self.trace.dump({})
        elif remove_unset:
            source.pop("trace", None)
        if self.servers is not None:
            source["servers"] = [s.dump({}) for s in self.servers]
        elif remove_unset:
            source.pop("servers", None)
        if self.parameters is not None:
            source["parameters"] = [p.dump({}) for p in self.parameters]
        elif remove_unset:
            source.pop("parameters", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.ref != value.ref:
            return False
        if self.summary != value.summary:
            return False
        if self.description != value.description:
            return False
        if self.get != value.get:
            return False
        if self.post != value.post:
            return False
        if self.delete != value.delete:
            return False
        if self.options != value.options:
            return False
        if self.head != value.head:
            return False
        if self.patch != value.patch:
            return False
        if self.trace != value.trace:
            return False
        if len(self.servers or []) != len(value.servers or []):
            return False
        for s, v in zip(self.servers or [], value.servers or []):
            if s != v:
                return False
        if len(self.parameters or []) != len(value.parameters or []):
            return False
        for sp, vp in zip(self.parameters or [], value.parameters or []):
            if sp != vp:
                return False
        return True


class Paths:
    _paths: dict[str, PathItem]

    @property
    def paths(self) -> dict[str, PathItem]:
        return self._paths

    @paths.setter
    def paths(self, value: dict[str, PathItem]) -> None:
        self._paths = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        for item in kwargs:
            if not isinstance(kwargs[item], dict):
                raise SchemaMismatch(
                    f"Paths must contain path items, and each path item must be a dict (is {type(kwargs[item])})"
                )
            self._paths[item] = PathItem(**kwargs[item])

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        if not source and (not remove_unset):
            source = self.source
        source = {p: self._paths[p].dump({}) for p in self._paths}
        return source

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Paths):
            return False
        self_set = set(self._paths.keys())
        val_set = set(value._paths.keys())
        if val_set != self_set:
            return False
        for key in val_set:
            if self._paths[key] != value._paths[key]:
                return False
        return True
