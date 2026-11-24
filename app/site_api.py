"""The cycling site: the event behind an upload token, its protocols, and the upload.

Standard library only (``urllib``), like the sibling tools. The opener is injectable, so
tests hand in a fake and never reach the network.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
import uuid
from collections.abc import Callable
from typing import Any

Opener = Callable[..., Any]
DEFAULT_SITE = "https://universalbicycle.team"


class SiteApiError(Exception):
    """A failure talking to the site or to a sheet: HTTP status, transport, bad JSON."""


def _detail(exc: urllib.error.HTTPError) -> str:
    """The site's own reason for a refusal, when it gave one."""
    try:
        return str(json.loads(exc.read().decode("utf-8")).get("detail") or exc.reason)
    except ValueError, AttributeError, TypeError, OSError:
        return str(exc.reason)


def _multipart(
    fields: dict[str, str], files: list[tuple[str, str, str, bytes]]
) -> tuple[bytes, str]:
    """``fields`` and ``files`` (field, filename, type, content) as form-data."""
    boundary = uuid.uuid4().hex
    parts = [
        f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n'
        f"{value}\r\n".encode()
        for name, value in fields.items()
    ]
    for field, filename, file_type, content in files:
        head = (
            f'--{boundary}\r\nContent-Disposition: form-data; name="{field}";'
            f' filename="{filename}"\r\nContent-Type: {file_type}\r\n\r\n'
        )
        parts.append(head.encode() + content + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


class SiteApi:
    def __init__(
        self,
        base_url: str = DEFAULT_SITE,
        opener: Opener = urllib.request.urlopen,
        timeout: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self._opener = opener
        self.timeout = timeout

    def _open(self, request: urllib.request.Request | str) -> bytes:
        try:
            with self._opener(request, timeout=self.timeout) as answer:
                return answer.read()
        except urllib.error.HTTPError as exc:
            raise SiteApiError(f"HTTP {exc.code}: {_detail(exc)}") from exc
        except urllib.error.URLError as exc:
            raise SiteApiError(f"Connection error: {exc.reason}") from exc

    def _url(self, path: str) -> str:
        # urllib would quote the whole address, token and all, in its refusal.
        if not self.base_url.startswith(("https://", "http://")):
            raise SiteApiError(
                f"The site's address must start with https://: {self.base_url!r}"
            )
        return self.base_url + path

    def _json(self, path: str) -> Any:
        try:
            return json.loads(self._open(self._url(path)).decode("utf-8"))
        except ValueError as exc:
            # The query carries the upload token: the message names the path alone.
            where = path.partition("?")[0]
            raise SiteApiError(f"Invalid answer from {where}: {exc}") from exc

    def fetch_text(self, url: str) -> str:
        """Any address as text, such as a sheet's CSV export."""
        if not url.startswith(("https://", "http://")):
            raise SiteApiError(f"Not a web address: {url!r}")
        return self._open(url).decode("utf-8-sig")

    def competition(self, token: str) -> tuple[int, str]:
        """The id and the title of the event an upload token belongs to."""
        query = urllib.parse.urlencode({"competition_token": token})
        data = self._json(f"/api/v1/participants/?{query}")
        return int(data.get("competition_id") or 0), str(
            data.get("competition_title") or ""
        )

    def protocols(self, competition_id: int, token: str) -> list[dict[str, Any]]:
        """The event's protocols in the order of its sections, read by its upload token,
        which the site takes for an invite-only or hidden event too."""
        query = urllib.parse.urlencode(
            {"competition_id": competition_id, "competition_token": token}
        )
        return list(self._json(f"/api/v1/protocols/?{query}"))

    def protocol(self, protocol_id: int, token: str) -> dict[str, Any]:
        """One protocol with its structured document (None when the site took none: HTML
        alone, or data it refused), read by its event's upload token."""
        query = urllib.parse.urlencode({"competition_token": token})
        return dict(self._json(f"/api/v1/protocols/{int(protocol_id)}?{query}"))

    def upload(
        self,
        token: str,
        document: dict[str, Any],
        section: int,
        stage_label: str = "",
        is_live: bool = True,
        protocol_type: str = "absolute",
    ) -> str:
        """Publish ``document`` into the event's ``section``; the site's reason for not
        taking the document, or ``""``."""
        body, content_type = _multipart(
            fields={
                "competition_token": token,
                "protocol_type": protocol_type,
                "is_live": "true" if is_live else "false",
                "stage_label": stage_label,
                "section": str(section),
            },
            files=[
                (
                    "document",
                    "protocol.json",
                    "application/json",
                    json.dumps(document, ensure_ascii=False).encode("utf-8"),
                )
            ],
        )
        request = urllib.request.Request(  # noqa: S310 - the site's own https address
            self._url("/api/v1/protocols/upload/"),
            data=body,
            headers={"Content-Type": content_type},
            method="POST",
        )
        answer = self._open(request)
        try:
            return str(json.loads(answer.decode("utf-8")).get("document_error") or "")
        except ValueError, AttributeError, TypeError:
            return ""
