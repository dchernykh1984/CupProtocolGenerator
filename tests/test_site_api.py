import io
import json
import urllib.error

import pytest

from app.site_api import SiteApi, SiteApiError


class _Answer:
    def __init__(self, body: bytes) -> None:
        self._body = body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self) -> bytes:
        return self._body


class _Opener:
    """Answers every request with the next canned body, and remembers the requests."""

    def __init__(self, *bodies) -> None:
        self.bodies = list(bodies)
        self.requests: list = []

    def __call__(self, request, timeout):
        self.requests.append(request)
        body = self.bodies.pop(0)
        if isinstance(body, Exception):
            raise body
        return _Answer(body if isinstance(body, bytes) else json.dumps(body).encode())


def _url(request) -> str:
    return request if isinstance(request, str) else request.full_url


def test_the_event_of_a_token_is_its_id_and_title():
    opener = _Opener({"competition_id": 249, "competition_title": "Cup"})
    assert SiteApi("https://site.test/", opener).competition("tok en") == (249, "Cup")
    assert _url(opener.requests[0]) == (
        "https://site.test/api/v1/participants/?competition_token=tok+en"
    )


def test_an_events_protocols_and_one_protocol_are_read_by_its_upload_token():
    # The token lets the site give an invite-only event's protocols too.
    opener = _Opener([{"id": 1}], {"id": 1, "document": None})
    api = SiteApi("https://site.test", opener)
    assert api.protocols(249, "tok en") == [{"id": 1}]
    assert api.protocol(1, "tok en") == {"id": 1, "document": None}
    assert [_url(r) for r in opener.requests] == [
        "https://site.test/api/v1/protocols/?competition_id=249&competition_token=tok+en",
        "https://site.test/api/v1/protocols/1?competition_token=tok+en",
    ]


def test_a_sheet_is_read_as_text_without_its_byte_order_mark():
    opener = _Opener(b"\xef\xbb\xbfTimestamp,Bib,Result\n")
    assert (
        SiteApi(opener=opener).fetch_text("https://docs.test/x")
        == "Timestamp,Bib,Result\n"
    )


def test_only_a_web_address_is_fetched():
    with pytest.raises(SiteApiError, match="Not a web address"):
        SiteApi(opener=_Opener()).fetch_text("file:///etc/passwd")


def test_a_refusal_says_the_sites_own_reason():
    refusal = urllib.error.HTTPError(
        "https://site.test",
        404,
        "Not Found",
        {},
        io.BytesIO(b'{"detail": "No such token"}'),
    )
    with pytest.raises(SiteApiError, match="HTTP 404: No such token"):
        SiteApi(opener=_Opener(refusal)).competition("x")


def test_a_refusal_without_a_reason_says_its_status():
    refusal = urllib.error.HTTPError(
        "https://site.test", 500, "Server Error", {}, io.BytesIO(b"<html>")
    )
    with pytest.raises(SiteApiError, match="HTTP 500: Server Error"):
        SiteApi(opener=_Opener(refusal)).protocols(1, "tok")


def test_a_broken_connection_and_a_broken_answer_are_errors():
    with pytest.raises(SiteApiError, match="Connection error"):
        SiteApi(opener=_Opener(urllib.error.URLError("down"))).protocol(1, "tok")
    with pytest.raises(SiteApiError, match="Invalid answer"):
        SiteApi(opener=_Opener(b"<html>")).protocol(1, "tok")


def test_the_upload_sends_the_document_into_its_section():
    opener = _Opener({"id": 5, "document_error": None})
    api = SiteApi("https://site.test", opener)
    assert (
        api.upload(
            "tok",
            {"schema": 1, "sections": []},
            section=2,
            stage_label="Final",
            is_live=False,
        )
        == ""
    )
    request = opener.requests[0]
    body = request.data.decode()
    assert request.full_url == "https://site.test/api/v1/protocols/upload/"
    assert request.get_header("Content-type").startswith(
        "multipart/form-data; boundary="
    )
    for field, value in (
        ("competition_token", "tok"),
        ("section", "2"),
        ("is_live", "false"),
        ("stage_label", "Final"),
    ):
        assert f'name="{field}"\r\n\r\n{value}\r\n' in body
    assert 'name="document"; filename="protocol.json"' in body
    assert '{"schema": 1, "sections": []}' in body


def test_the_upload_reports_a_document_the_site_did_not_take():
    opener = _Opener({"id": 5, "document_error": "bad cell"}, b"not json")
    api = SiteApi(opener=opener)
    assert api.upload("tok", {}, section=2) == "bad cell"
    assert api.upload("tok", {}, section=2) == ""
