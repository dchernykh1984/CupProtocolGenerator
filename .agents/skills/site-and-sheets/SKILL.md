---
name: site-and-sheets
description: The data contracts of the two connectors -- the cycling site (upload tokens, protocols, the protocol document) and Google Forms response sheets. Use when reading or changing app/site_api.py, app/protocol_reader.py, app/sheets.py or app/document.py.
---

# The connectors

## The cycling site (`app/site_api.py`)

The site is universalbicycle.team (`DEFAULT_SITE`); its API has no language prefix.

- `GET /api/v1/participants/?competition_token=<token>` answers `competition_id` and
  `competition_title` for an event's upload token (and its registrations, which carry
  no bibs: bibs come from the protocols).
- `GET /api/v1/protocols/?competition_id=<id>` lists the event's protocols in section
  order: `id`, `section`, `section_name`, `protocol_type` (`absolute` or `group`),
  `stage_label`, `is_live`, `last_updated`, `file_hash`, `shown` (`document` or `html`),
  `has_html`.
- `GET /api/v1/protocols/<id>` adds `document` (null when the last upload was HTML
  alone) and the update history. A stage protocol must be uploaded "with data".
- Reading needs no token for a published event. An invite-only event's protocols need
  the reader's personal token, and a hidden, unpublished or deleted event's protocols
  answer 404 to everybody -- test on a published event.
- `POST /api/v1/protocols/upload/`, multipart: `competition_token`, `protocol_type`,
  `is_live`, `stage_label`, `section`, and the file `document` (`protocol.json`,
  `application/json`). The section must exist: the organizer adds it on the event's
  "Protocol sections" page. The answer's `document_error` says why the site did not
  take the document.

## The protocol document (schema 1)

`tests/fixtures/protocol-document-v1.json` is the site's JSON Schema; the tests validate
every document against it, so keep it in sync with the site's
`protocols/schema/protocol-document-v1.json`. Cells are strings: the site never parses a
time or a place. Columns say what they hold by `role` (`place`, `bib`, `name`, `team`,
`result`, `gap`, `group`); `place` and `result` stay visible on a phone; a column id is
`[A-Za-z0-9_-]{1,64}`; a section's or a row's `group` must be declared in `groups`.

## Google Forms sheets (`app/sheets.py`)

- One form per stage (or exercise), two questions in this order: the bib, then the
  result. Its response sheet has three columns -- timestamp, bib, result -- read by
  position. The first readable answer for a bib counts; a later one is reported as an
  error and never taken, so a second mark is seen (the maintainer, 2026-11-23).
- The sheet is shared as "Anyone with the link: Viewer"; the tool reads its CSV export
  (`/export?format=csv&gid=<tab>`, the first tab without a `gid`). An unshared sheet
  answers HTTP 401, which the build reports as it is; a sign-in page in its place, as
  Google used to send, is recognised and reported. Forms must not collect e-mail
  addresses.
