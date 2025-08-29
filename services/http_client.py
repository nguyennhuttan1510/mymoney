from typing import Any, Dict, Optional, Union
import httpx
from httpx import Response, Timeout
import logging
from urllib.parse import urljoin

from mymoney.config import HTTP

logger = logging.getLogger(__name__)


class API:
    """
    A reusable API client class that uses httpx for making HTTP requests.
    
    This class provides methods for making GET, POST, PUT, DELETE requests with
    configurable options like headers, authentication, timeouts, and retries.
    """

    def __init__(
            self,
            base_url: str,
            headers: Optional[Dict[str, str]] = None,
            timeout: int = 30,
            max_retries: int = 3,
            auth: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize the API client.
        
        Args:
            base_url: The base URL for the API.
            headers: Optional headers to include in all requests.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries for failed requests.
            auth: Optional authentication credentials.
        """
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.auth = auth

    def _build_url(self, endpoint: str) -> str:
        """
        Build the full URL by joining the base URL and endpoint.
        
        Args:
            endpoint: The API endpoint.
            
        Returns:
            The full URL.
        """
        return urljoin(self.base_url, endpoint)

    def _handle_response(self, response: Response) -> Dict[str, Any]:
        """
        Handle the API response.
        
        Args:
            response: The httpx Response object.
            
        Returns:
            The parsed response data.
            
        Raises:
            httpx.HTTPStatusError: If the response contains an HTTP error status.
        """
        response.raise_for_status()

        if response.headers.get("content-type") == "application/json":
            return response.json()
        return {"data": response.text}

    def _make_request(
            self,
            method: str,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request with retry logic.
        
        Args:
            method: The HTTP method (GET, POST, PUT, DELETE).
            endpoint: The API endpoint.
            params: Optional query parameters.
            data: Optional form data.
            json_data: Optional JSON data.
            headers: Optional headers to override the default headers.
            timeout: Optional timeout to override the default timeout.
            
        Returns:
            The parsed response data.
            
        Raises:
            httpx.HTTPStatusError: If the response contains an HTTP error status.
            httpx.RequestError: If there's an issue with the request.
        """
        url = self._build_url(endpoint)
        request_headers = {**self.headers, **(headers or {})}
        request_timeout = Timeout(timeout or self.timeout)

        retries = 0
        last_exception = None

        while retries < self.max_retries:
            try:
                with httpx.Client(timeout=request_timeout) as client:
                    response = client.request(
                        method=method,
                        url=url,
                        params=params,
                        data=data,
                        json=json_data,
                        headers=request_headers,
                        auth=self.auth,
                    )
                    return self._handle_response(response)
            except (httpx.HTTPStatusError, httpx.RequestError) as e:
                last_exception = e
                retries += 1
                logger.warning(f"Request failed (attempt {retries}/{self.max_retries}): {str(e)}")

                # Don't retry on client errors (4xx)
                if isinstance(e, httpx.HTTPStatusError) and 400 <= e.response.status_code < 500:
                    raise

                if retries > self.max_retries:
                    break

        if last_exception:
            logger.error(f"Request failed after {self.max_retries} retries: {str(last_exception)}")
            raise last_exception

        # This should never happen, but just in case
        raise Exception("Request failed for unknown reason")

    def get(
            self,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Make a GET request.
        
        Args:
            endpoint: The API endpoint.
            params: Optional query parameters.
            headers: Optional headers to override the default headers.
            timeout: Optional timeout to override the default timeout.
            
        Returns:
            The parsed response data.
        """
        return self._make_request("GET", endpoint, params=params, headers=headers, timeout=timeout)

    def post(
            self,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Make a POST request.
        
        Args:
            endpoint: The API endpoint.
            data: Optional form data.
            json_data: Optional JSON data.
            params: Optional query parameters.
            headers: Optional headers to override the default headers.
            timeout: Optional timeout to override the default timeout.
            
        Returns:
            The parsed response data.
        """
        return self._make_request(
            "POST",
            endpoint,
            params=params,
            data=data,
            json_data=json_data,
            headers=headers,
            timeout=timeout,
        )

    def put(
            self,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Make a PUT request.
        
        Args:
            endpoint: The API endpoint.
            data: Optional form data.
            json_data: Optional JSON data.
            params: Optional query parameters.
            headers: Optional headers to override the default headers.
            timeout: Optional timeout to override the default timeout.
            
        Returns:
            The parsed response data.
        """
        return self._make_request(
            "PUT",
            endpoint,
            params=params,
            data=data,
            json_data=json_data,
            headers=headers,
            timeout=timeout,
        )

    def delete(
            self,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Make a DELETE request.
        
        Args:
            endpoint: The API endpoint.
            params: Optional query parameters.
            headers: Optional headers to override the default headers.
            timeout: Optional timeout to override the default timeout.
            
        Returns:
            The parsed response data.
        """
        return self._make_request("DELETE", endpoint, params=params, headers=headers, timeout=timeout)


class NotificationAPI(API):
    BASE_URL = HTTP.NOTIFICATION

    def __init__(self, headers: Optional[Dict[str, str]] = None, timeout: int = 30, max_retries: int = 3,
                 auth: Optional[Dict[str, str]] = None):
        super().__init__(self.BASE_URL, headers, timeout, max_retries, auth)
