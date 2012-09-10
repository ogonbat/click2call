
"""Module Containing generic utilities."""

__author__ = 'cingusoft'


class General(object):
    """Class with the utility."""
    def getHeadersAccepted(self,header):
        """Check if the Client has configured the Accept header.
        if the accept header is configured, check if is one of the permitted xml or json support
        if not force to JSON string formatting."""
        accept=header.get("accept")
        if accept is not None:
            if "text/xml" in accept or "application/xml" in accept:
                return "xml"
        return "json"