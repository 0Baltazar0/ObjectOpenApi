from copy import deepcopy
import os
from typing import Any, Optional
from objectopenapi.components.components import Components
from objectopenapi.external_doc.external_doc import ExternalDocs
from objectopenapi.info.info import Info
from objectopenapi.paths.paths import Paths
from objectopenapi.security_requirement.security_requirement import SecurityRequirement
from objectopenapi.server.server import Server
from objectopenapi.tag.tag import Tag
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch
from .utils.validator import is_value_type, validate_key_type


class OpenApi:
    _openapi: str

    @property
    def openapi(self) -> str:
        return self._openapi

    @openapi.setter
    def openapi(self, value: str | Any) -> None:
        self._openapi = validate_key_type("openapi", str, {"openapi": value})

    _info: Info

    @property
    def info(self) -> Info:
        return self._info

    @info.setter
    def info(self, value: JSON_DICT | Info) -> None:
        if isinstance(value, Info):
            self._info = value
        else:
            self._info = Info(**value)

    _jsonSchemaDialect: str

    @property
    def jsonSchemaDialect(self) -> str:
        return self._jsonSchemaDialect

    @jsonSchemaDialect.setter
    def jsonSchemaDialect(self, value: Any) -> None:
        self._jsonSchemaDialect = validate_key_type("info", str, {"info": value})

    _servers: list[Server]

    @property
    def servers(self) -> list[Server]:
        return self._servers

    @servers.setter
    def servers(self, value: list[Server]) -> None:
        self._servers = value

    _paths: Optional[Paths]

    @property
    def paths(self) -> Optional[Paths]:
        return self._paths

    @paths.setter
    def paths(self, value: Optional[Paths]) -> None:
        self._paths = value

    _components: Optional[Components]

    @property
    def components(self) -> Optional[Components]:
        return self._components

    @components.setter
    def components(self, value: Components) -> None:
        self._components = value

    _security: Optional[list[SecurityRequirement]]

    @property
    def security(self) -> Optional[list[SecurityRequirement]]:
        return self._security

    @security.setter
    def security(self, value: Optional[list[SecurityRequirement]]) -> None:
        self._security = value

    _tags: Optional[list[Tag]]

    @property
    def tags(self) -> Optional[list[Tag]]:
        return self._tags

    @tags.setter
    def tags(self, value: Optional[list[Tag]]) -> None:
        self._tags = value

    _externalDocs: Optional[ExternalDocs]

    @property
    def externalDocs(self) -> Optional[ExternalDocs]:
        return self._externalDocs

    @externalDocs.setter
    def externalDocs(self, value: Optional[ExternalDocs]) -> None:
        self._externalDocs = value

    def __init__(self, **kwargs: JSON_DICT) -> None:
        if "openapi" not in kwargs:
            raise SchemaMismatch(
                "Openapi document must contain an 'openapi' value (string)"
            )
        self._openapi = validate_key_type(
            "openapi", str, {"openapi": kwargs["openapi"]}
        )
        if "info" not in kwargs:
            raise SchemaMismatch(
                "Openapi document must contain 'info' value (Info Object)"
            )
        self._info = Info(**kwargs["info"])
        if "jsonSchemaDialect" in kwargs:
            self._jsonSchemaDialect = validate_key_type(
                "jsonSchemaDialect",
                str,
                {"jsonSchemaDialect": kwargs["jsonSchemaDialect"]},
            )
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
        if "paths" in kwargs:
            if not isinstance(kwargs["paths"], dict):
                raise SchemaMismatch(
                    "Openapi document 'paths' must be of value (Paths Object)"
                )
            self._paths = Paths(**kwargs["paths"])

        #  TODO webhooks

        if "components" in kwargs:
            if not isinstance(kwargs["components"], dict):
                raise SchemaMismatch(
                    "Openapi document 'components' must be of value (Components Object)"
                )
            self._components = Components(**kwargs["components"])

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
        if "tags" in kwargs:
            if not isinstance(kwargs["tags"], list):
                raise SchemaMismatch(
                    "Openapi document 'tags' must be of value ([Tag Object])"
                )
            self._tags = [
                Tag(**s)
                for s in kwargs["tags"]
                if is_value_type(s, dict)
                and isinstance(
                    s, dict
                )  # pretty stupid but it works with language servers
            ]

        if "externalDocs" in kwargs:
            if not isinstance(kwargs["externalDocs"], dict):
                raise SchemaMismatch(
                    "Openapi document 'externalDocs' must be of value (ExternalDocs Object)"
                )
            self._externalDocs = ExternalDocs(**kwargs["externalDocs"])

        self.source = kwargs

    def dump(self, source: dict[str, Any] = {}) -> dict[str, Any]:
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )

        if not source:
            source = deepcopy(self.source)

        source["openapi"] = self.openapi

        source["info"] = self.info.dump(self.source.get("dump", {}))

        if self.jsonSchemaDialect:
            source["jsonSchemaDialect"] = self.jsonSchemaDialect
        else:
            if remove_unset:
                source.pop("jsonSchemaDialect", None)

        if self.servers:
            source["servers"] = [s.dump({}) for s in self.servers]
        else:
            if remove_unset:
                source.pop("servers", None)

        if self.paths:
            source["paths"] = self.paths.dump(self.source.get("paths", {}))
        else:
            if remove_unset:
                source.pop("paths", None)

        # TODO webhooks

        if self.components:
            source["components"] = self.components.dump(
                self.source.get("components", {})
            )
        else:
            if remove_unset:
                source.pop("components", None)

        if self.security:
            source["security"] = [s.dump({}) for s in self.security]
        else:
            if remove_unset:
                source.pop("security", None)

        if self.tags:
            source["tags"] = [t.dump({}) for t in self.tags]
        else:
            if remove_unset:
                source.pop("tags", None)

        if self.externalDocs:
            source["externalDocs"] = self.externalDocs.dump(
                self.source.get("externalDocs", {})
            )
        else:
            if remove_unset:
                source.pop("externalDocs", None)

        return source
