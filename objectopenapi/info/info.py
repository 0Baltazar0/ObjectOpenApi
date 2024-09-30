from copy import deepcopy
import os
from typing import Any, Optional
from objectopenapi.utils.common_types import JSON_DICT
from objectopenapi.utils.parse_errors import SchemaMismatch
from objectopenapi.utils.validator import validate_key_type


class Contact:
    _name: str

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    _identifier: Optional[str]

    @property
    def identifier(self) -> Optional[str]:
        return self._identifier

    @identifier.setter
    def identifier(self, value: Optional[str]) -> None:
        self._identifier = value

    _url: Optional[str]

    @property
    def url(self) -> Optional[str]:
        return self._url

    @url.setter
    def url(self, value: Optional[str]) -> None:
        self._url = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "name" in kwargs:
            self._name = kwargs["name"]
        else:
            raise SchemaMismatch("Object document must contain a 'name' value ( str)")
        if "identifier" in kwargs:
            self._identifier = kwargs["identifier"]
        if "url" in kwargs:
            self._url = kwargs["url"]

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = self.source

        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )

        source["name"] = self._name
        if self._identifier:
            source["identifier"] = self._identifier
        elif remove_unset:
            source.pop("identifier", None)
        if self._url:
            source["url"] = self._url
        elif remove_unset:
            source.pop("url", None)
        return source


class License:
    _name: Optional[str]

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        self._name = value

    _url: Optional[str]

    @property
    def url(self) -> Optional[str]:
        return self._url

    @url.setter
    def url(self, value: Optional[str]) -> None:
        self._url = value

    _email: Optional[str]

    @property
    def email(self) -> Optional[str]:
        return self._email

    @email.setter
    def email(self, value: Optional[str]) -> None:
        self._email = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "name" in kwargs:
            self._name = kwargs["name"]
        if "url" in kwargs:
            self._url = kwargs["url"]
        if "email" in kwargs:
            self._email = kwargs["email"]

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = self.source

        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )

        if self._name:
            source["name"] = self._name
        elif remove_unset:
            source.pop("name", None)

        if self._url:
            source["url"] = self._url
        elif remove_unset:
            source.pop("url", None)

        if self._email:
            source["email"] = self._email
        elif remove_unset:
            source.pop("email", None)

        return source


class Info:
    _title: str

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        if not isinstance(value, str):
            raise SchemaMismatch("Title must be a string")
        self._title = value

    _summary: Optional[str]

    # Getter and Setter for _summary
    @property
    def summary(self) -> Optional[str]:
        return self._summary

    @summary.setter
    def summary(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise SchemaMismatch("Summary must be a string or None")
        self._summary = value

    _description: Optional[str]

    # Getter and Setter for _description
    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise SchemaMismatch("Description must be a string or None")
        self._description = value

    _termsOfService: Optional[str]

    # Getter and Setter for _termsOfService
    @property
    def termsOfService(self) -> Optional[str]:
        return self._termsOfService

    @termsOfService.setter
    def termsOfService(self, value: Optional[str]) -> None:
        if value is not None and not isinstance(value, str):
            raise SchemaMismatch("Terms of Service must be a string or None")
        self._termsOfService = value

    _contact: Optional[Contact]

    # Getter and Setter for _contact
    @property
    def contact(self) -> Optional["Contact"]:
        return self._contact

    @contact.setter
    def contact(self, value: Optional["Contact"]) -> None:
        if value is not None and not isinstance(value, Contact):
            raise SchemaMismatch("Contact must be an instance of Contact or None")
        self._contact = value

    _license: Optional[License]

    # Getter and Setter for _license
    @property
    def license(self) -> Optional["License"]:
        return self._license

    @license.setter
    def license(self, value: Optional["License"]) -> None:
        if value is not None and not isinstance(value, License):
            raise SchemaMismatch("License must be an instance of License or None")
        self._license = value

    _version: str

    # Getter and Setter for _version
    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, value: str) -> None:
        if not isinstance(value, str):
            raise SchemaMismatch("Version must be a string")
        self._version = value

    def __init__(self, **kwargs: Any) -> None:
        self.source = kwargs
        if "title" in kwargs:
            self._title = validate_key_type("title", str, {"title": kwargs["title"]})
        else:
            raise SchemaMismatch("Info document must contain 'title' value (string)")
        if "version" in kwargs:
            self._version = validate_key_type(
                "version", str, {"version": kwargs["version"]}
            )
        else:
            raise SchemaMismatch("Info document must contain 'summary' value (string)")
        if "description" in kwargs:
            self._description = validate_key_type(
                "description", str, {"description": kwargs["description"]}
            )
        if "summary" in kwargs:
            self._summary = validate_key_type(
                "summary", str, {"summary": kwargs["summary"]}
            )
        if "termsOfService" in kwargs:
            self._termsOfService = validate_key_type(
                "termsOfService", str, {"termsOfService": kwargs["termsOfService"]}
            )

        if "contact" in kwargs:
            self._contact = Contact(**kwargs["contact"])
        if "license" in kwargs:
            self._license = License(**kwargs["license"])

    def dump(self, source: JSON_DICT) -> JSON_DICT:
        if not source:
            source = deepcopy(self.source)
        remove_unset = (
            os.environ.get("REMOVE_UNSET_PROPERTIES", "true").lower() == "true"
        )
        source["title"] = self.title
        source["version"] = self.version

        if self.summary:
            source["summary"] = self.summary
        elif remove_unset:
            source.pop("summary", None)

        if self.description:
            source["description"] = self.description
        elif remove_unset:
            source.pop("description", None)

        if self.termsOfService:
            source["termsOfService"] = self.termsOfService
        elif remove_unset:
            source.pop("termsOfService", None)

        if self.contact:
            source["contact"] = self.contact.dump(self.source.get("contact", {}))
        elif remove_unset:
            source.pop("contact", None)
        if self.license:
            source["license"] = self.license.dump(self.source.get("license", {}))
        elif remove_unset:
            source.pop("license", None)

        return source
