from copy import deepcopy
import os
from typing import Any, Optional
from objectopenapi.external_doc.external_doc import ExternalDocs
from objectopenapi.parameter.parameter import Parameter, ParseParameter
from objectopenapi.reference.reference import Reference
from objectopenapi.request_body.request_body import RequestBody
from objectopenapi.responses.responses import Responses
from objectopenapi.security_requirement.security_requirement import SecurityRequirement
from objectopenapi.server.server import Server
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch
from objectopenapi.utils.validator import is_value_type, validate_key_type


class Operation:
    _tags: Optional[list[str]]

    @property
    def tags(self) -> Optional[list[str]]:
        return self._tags

    @tags.setter
    def tags(self, value: Optional[list[str]]) -> None:
        self._tags = value

    _summary: Optional[str]

    @property
    def summary(self) -> Optional[str]:
        return self._summary

    @summary.setter
    def summary(self, value: Optional[str]) -> None:
        self._summary = value

    _description: Optional[str]

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        self._description = value

    _externalDocs: Optional[ExternalDocs]

    @property
    def externalDocs(self) -> Optional[ExternalDocs]:
        return self._externalDocs

    @externalDocs.setter
    def externalDocs(self, value: Optional[ExternalDocs]) -> None:
        self._externalDocs = value

    _operationId: Optional[str]

    @property
    def operationId(self) -> Optional[str]:
        return self._operationId

    @operationId.setter
    def operationId(self, value: Optional[str]) -> None:
        self._operationId = value

    _parameters: Optional[list[Parameter | Reference]]

    @property
    def parameters(self) -> Optional[list[Parameter | Reference]]:
        return self._parameters

    @parameters.setter
    def parameters(self, value: Optional[list[Parameter | Reference]]) -> None:
        self._parameters = value

    _requestBody: Optional[RequestBody | Reference]

    @property
    def requestBody(self) -> Optional[RequestBody | Reference]:
        return self._requestBody

    @requestBody.setter
    def requestBody(self, value: Optional[RequestBody | Reference]) -> None:
        self._requestBody = value

    _responses: Responses

    @property
    def responses(self) -> Responses:
        return self._responses

    @responses.setter
    def responses(self, value: Responses) -> None:
        self._responses = value

    # TODO _callbacks
    _deprecated: Optional[bool]

    @property
    def deprecated(self) -> Optional[bool]:
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value: Optional[bool]) -> None:
        self._deprecated = value

    _security: Optional[list[SecurityRequirement]]

    @property
    def security(self) -> Optional[list[SecurityRequirement]]:
        return self._security

    @security.setter
    def security(self, value: Optional[list[SecurityRequirement]]) -> None:
        self._security = value

    _servers: Optional[list[Server]]

    @property
    def servers(self) -> Optional[list[Server]]:
        return self._servers

    @servers.setter
    def servers(self, value: Optional[list[Server]]) -> None:
        self._servers = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "tags" in kwargs:
            self._tags = validate_key_type("tags", list[str], {"tags": kwargs["tags"]})
        if "summary" in kwargs:
            self._summary = validate_key_type(
                "summary", str, {"summary": kwargs["summary"]}
            )
        if "description" in kwargs:
            self._description = validate_key_type(
                "description", str, {"description": kwargs["description"]}
            )
        if "externalDocs" in kwargs:
            self._externalDocs = ExternalDocs(**kwargs["externalDocs"])
        if "operationId" in kwargs:
            self._operationId = validate_key_type(
                "operationId", str, {"operationId": kwargs["operationId"]}
            )
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
        if "requestBody" in kwargs:
            try:
                req = RequestBody(**kwargs["requestBody"])
                self._requestBody = req
            except Exception as reqError:
                try:
                    ref = Reference(**kwargs["examples"])
                    self._requestBody = ref
                except Exception as refError:
                    raise SchemaMismatch(
                        f"Operation 'requestBody' must be of instance RequestBody or Reference. {reqError=} {refError=}"
                    )
        if "responses" in kwargs:
            self._responses = Responses(**kwargs["responses"])
        else:
            raise SchemaMismatch('Object must contain "responses" value (Responses)')
        if "deprecated" in kwargs:
            self._deprecated = validate_key_type(
                "deprecated", bool, {"deprecated": kwargs["deprecated"]}
            )
        if "security" in kwargs:
            if not isinstance(kwargs["security"], list):
                raise SchemaMismatch(
                    "Openapi document 'security' must be of value ([Security Object])"
                )
            self._security = [
                SecurityRequirement(**s)
                for s in kwargs["security"]
                if is_value_type(s, dict)
                and isinstance(
                    s, dict
                )  # pretty stupid but it works with language servers
            ]

        if "servers" in kwargs:
            if not isinstance(kwargs["servers"], list):
                raise SchemaMismatch(
                    "Openapi document 'servers' must be of value ([Server Object])"
                )
            self._servers = [
                Server(**s)
                for s in kwargs["servers"]
                if is_value_type(s, dict)
                and isinstance(
                    s, dict
                )  # pretty stupid but it works with language servers
            ]

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        if self.tags is not None:
            source["tags"] = self.tags  # type:ignore
        elif remove_unset:
            source.pop("tags", None)
        if self.summary is not None:
            source["summary"] = self.summary
        elif remove_unset:
            source.pop("summary", None)
        if self.description is not None:
            source["description"] = self.description
        elif remove_unset:
            source.pop("description", None)
        if self.externalDocs is not None:
            source["externalDocs"] = self.externalDocs.dump({})
        elif remove_unset:
            source.pop("externalDocs", None)
        if self.operationId is not None:
            source["operationId"] = self.operationId
        elif remove_unset:
            source.pop("operationId", None)
        if self.parameters is not None:
            source["parameters"] = [p.dump({}) for p in self.parameters]
        elif remove_unset:
            source.pop("parameters", None)
        if self.requestBody is not None:
            source["requestBody"] = self.requestBody.dump({})
        elif remove_unset:
            source.pop("requestBody", None)
        source["responses"] = self.responses.dump({})
        if self.deprecated is not None:
            source["deprecated"] = self.deprecated
        elif remove_unset:
            source.pop("deprecated", None)
        if self.security is not None:
            source["security"] = [s.dump({}) for s in self.security]
        elif remove_unset:
            source.pop("security", None)
        if self.servers is not None:
            source["servers"] = [s.dump({}) for s in self.servers]
        elif remove_unset:
            source.pop("servers", None)
        return source

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, type(self)):
            return False
        if self.tags != value.tags:
            return False
        if self.summary != value.summary:
            return False
        if self.description != value.description:
            return False
        if self.externalDocs != value.externalDocs:
            return False
        if self.operationId != value.operationId:
            return False
        if self.parameters != value.parameters:
            # TODO
            pass
        if self.requestBody != value.requestBody:
            # TODO
            pass
        if self.responses != value.responses:
            # TODO
            pass
        if self.deprecated != value.deprecated:
            return False
        if self.security != value.security:
            # TODO
            pass
        if self.servers != value.servers:
            # TODO
            pass
        return True
