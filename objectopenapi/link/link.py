from copy import deepcopy
import os
from typing import Any, Optional
from objectopenapi.server.server import Server
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.validator import validate_key_type


class Link:
    _operationRef: Optional[str]

    @property
    def operationRef(self) -> Optional[str]:
        return self._operationRef

    @operationRef.setter
    def operationRef(self, value: Optional[str]) -> None:
        self._operationRef = value

    _operationId: Optional[str]

    @property
    def operationId(self) -> Optional[str]:
        return self._operationId

    @operationId.setter
    def operationId(self, value: Optional[str]) -> None:
        self._operationId = value

    _parameters: Optional[dict[str, Any]]

    @property
    def parameters(self) -> Optional[dict[str, Any]]:
        return self._parameters

    @parameters.setter
    def parameters(self, value: Optional[dict[str, Any]]) -> None:
        self._parameters = value

    _requestBody: Optional[Any]

    @property
    def requestBody(self) -> Optional[Any]:
        return self._requestBody

    @requestBody.setter
    def requestBody(self, value: Optional[Any]) -> None:
        self._requestBody = value

    _description: Optional[str]

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    _server: Optional[Server]

    @property
    def server(self) -> Optional[Server]:
        return self._server

    @server.setter
    def server(self, value: Optional[Server]) -> None:
        self._server = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "operationRef" in kwargs:
            self._operationRef = validate_key_type(
                "operationRef", str, {"operationRef": kwargs["operationRef"]}
            )
        if "operationId" in kwargs:
            self._operationId = validate_key_type(
                "operationId", str, {"operationId": kwargs["operationId"]}
            )
        if "parameters" in kwargs:
            self.parameters = deepcopy(kwargs["parameters"])
        if "requestBody" in kwargs:
            self._requestBody = kwargs["requestBody"]
        if "description" in kwargs:
            self._description = validate_key_type(
                "description", str, {"description": kwargs["description"]}
            )
        if "server" in kwargs:
            self._server = validate_key_type(
                "server", Server, {"server": kwargs["server"]}
            )

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        if self.operationRef is not None:
            source["operationRef"] = self.operationRef
        elif remove_unset:
            source.pop("operationRef", None)
        if self.operationId is not None:
            source["operationId"] = self.operationId
        elif remove_unset:
            source.pop("operationId", None)
        if self.parameters is not None:
            source["parameters"] = self.parameters
        elif remove_unset:
            source.pop("parameters", None)
        if self.requestBody is not None:
            source["requestBody"] = self.requestBody
        elif remove_unset:
            source.pop("requestBody", None)
        if self.description is not None:
            source["description"] = self.description
        elif remove_unset:
            source.pop("description", None)
        if self.server is not None:
            source["server"] = self.server.dump({})
        elif remove_unset:
            source.pop("server", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.operationRef != value.operationRef:
            return False
        if self.operationId != value.operationId:
            return False
        if (
            self.parameters
            and value.parameters
            and set(self.parameters.keys()) == set(value.parameters.keys())
        ):
            for key in self.parameters:
                if value.parameters[key] != self.parameters[key]:
                    return False
        else:
            if self.parameters != value.parameters:
                return False
        if self.requestBody != value.requestBody:
            return False
        if self.description != value.description:
            return False
        if self.server != value.server:
            return False
        return True
