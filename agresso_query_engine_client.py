from typing import Dict

from abc import ABC, abstractmethod
from xml.etree import ElementTree

import requests


__version__ = "1.0.0"


class BaseClient(ABC):
    """
    Agresso query engine client base class.
    """

    @abstractmethod
    def get_template_result_as_xml(self, template: int) -> ElementTree.Element:
        """
        Queries the given template and returns the response as an `ElementTree.Element` instance
        if the request completed successfully.

        Arguments:
            template: The queried template ID.
        """
        pass


class AgressoQueryEngineClient(BaseClient):
    """
    Client application for Unit4 Agresso query engine service.
    """

    __slots__ = ("_username", "_password", "_client", "_service_url", "_timeout")

    def __init__(self, *, username: str, password: str, client: str, service_url: str, timeout: int = 5) -> None:
        """
        Initialization.

        Arguments:
            username: Agresso username.
            password: User password.
            client: Agresso client ID.
            service_url: The URL of the Agresso service (eg. "https://foo.bar/baz/service.svc").
            timeout: Request timeout in seconds.
        """
        self._username = username
        self._password = password
        self._client = client
        self._service_url = service_url
        self._timeout = timeout

    def get_template_result_as_xml(self, template: int) -> ElementTree.Element:
        """Inherited."""
        action = "GetTemplateResultAsXML"
        headers = self._make_request_headers(action)
        payload = self._make_template_request_payload(action, template)
        response = requests.post(url=self._service_url, data=payload, headers=headers, timeout=self._timeout)
        response.raise_for_status()
        content = ElementTree.fromstring(response.content)
        return ElementTree.fromstring(content[0][0][0][1].text)  # Raise exception if there's no text.

    def _make_request_headers(self, action: str) -> Dict[str, str]:
        """
        Creates requests headers for the given SOAP action.

        Arguments:
            action: The SOAP action that will be executed.
        """
        return {
            "Content-Type": "text/xml;charset=UTF-8",
            "Accept-Encoding": "gzip,deflate",
            "SOAPAction": f"https://services.agresso.com/QueryEngineService/QueryEngineV201101/{action}",
        }

    def _make_template_request_payload(self, action: str, template: int) -> str:
        """
        Creates the SOAP request's payload.

        Arguments:
            action: The SOAP action that will be executed.
            template: The queried template ID.
        """
        soapenv_ns = '"http://schemas.xmlsoap.org/soap/envelope/"'
        query_ns = '"http://services.agresso.com/QueryEngineService/QueryEngineV201101"'
        return (
            f"<soapenv:Envelope xmlns:soapenv={soapenv_ns} xmlns:quer={query_ns}>"
            f"  <soapenv:Header/>"
            f"  <soapenv:Body>"
            f"    <quer:{action}>"
            f"      {self._make_query_credentials()}"
            f"      <quer:input>"
            f"        <quer:TemplateId>{template}</quer:TemplateId>"
            f"      </quer:input>"
            f"    </quer:{action}>"
            f"  </soapenv:Body>"
            f"</soapenv:Envelope>"
        )

    def _make_query_credentials(self) -> str:
        """
        Creates the query's credentials part.
        """
        return (
            "<quer:credentials>"
            f"  <quer:Username>{self._username}</quer:Username>"
            f"  <quer:Client>{self._client}</quer:Client>"
            f"  <quer:Password>{self._password}</quer:Password>"
            "</quer:credentials>"
        )


class FileSystemClient(BaseClient):
    """
    Simple client for testing and development purposes that returns template
    results from the file system, instead of querying a live Agresso service.

    Template result can be registered using the `register_template_result()` method.
    """

    def __init__(self) -> None:
        """
        Initialization.
        """

        self._results: Dict[int, str] = {}
        """
        Template ID - result filename map.
        """

    def get_template_result_as_xml(self, template: int) -> ElementTree.Element:
        """Inherited."""
        path = self._results[template]
        return ElementTree.parse(path).getroot()

    def register_template_result(self, *, template: int, path: str) -> None:
        """
        Registers the result for the given template ID.

        If a result was already registered for the given template ID, it will be overwritten.

        Arguments:
            template: The template ID the result in the specified file is associated to.
            path: The path to the template result.
        """
        self._results[template] = path
