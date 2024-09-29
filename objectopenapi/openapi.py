from typing import Optional
from objectopenapi.components.components import Components
from objectopenapi.external_doc.external_doc import ExternalDocs
from objectopenapi.info.info import Info
from objectopenapi.paths.paths import Paths
from objectopenapi.security.security import Security
from objectopenapi.server.server import Server
from objectopenapi.tag.tag import Tag
from objectopenapi.utils.common_types import JSON_DICT
from .utils.validator import validate_key_type


class OpenApi:
    _openapi: str

    @property
    def openapi(self) -> str:
        return self._openapi

    @openapi.setter
    def openapi(self, value: str) -> None:
        self._nullable = validate_key_type("openapi", str, {"openapi": value})

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
    def jsonSchemaDialect(self, value: str) -> None:
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

    _security: Optional[list[Security]]

    @property
    def security(self) -> Optional[list[Security]]:
        return self._security

    @security.setter
    def security(self, value: Optional[list[Security]]) -> None:
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
