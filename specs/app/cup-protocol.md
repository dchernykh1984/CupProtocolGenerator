# Cup protocol: sources, rules, the protocol, the site

Written from the code (`app/`) on 2026-11-23. Where the code does not say why, this file
does not guess.

## What it does

A cup is a set of stages; an all-round event is a cup whose exercises are its stages.
For every stage the program reads the results from a connector -- a protocol published on
the cycling site, or a Google Forms response sheet -- scores them by the stage's rule,
adds the stages up by the cup's rule within every category, builds the site's structured
protocol document (schema 1) and uploads it into a protocol section of the cup's event.
Every build reads every stage again, so a correction anywhere is followed by a new build
and nothing else.

## Settings

Kept in `data/config.json` next to the program (`app/config.py`). The file holds upload
tokens, so `data/` is never committed. A setting the file lacks, or holds in a shape the
program does not read, takes its default; a file that cannot be read gives every default.

| Cup setting | Default | Meaning |
| --- | --- | --- |
| `site_url` | `https://universalbicycle.team` | the site, for every stage and the upload |
| `token` | empty | the cup event's upload token; its protocol is published there |
| `title` | empty | the protocol's title; empty: the cup event's title on the site |
| `rule` | `sum_smallest_wins` | the cup rule |
| `publish_section` | 2 | the cup event's protocol section to publish into (1 or more) |
| `final` | false | a final protocol: the site stops checking it for updates |
| `place_everybody` | false | a broadcast: those who missed stages are placed too |
| `stages` | one empty stage | the stages, in order |

| Stage setting | Default | Meaning |
| --- | --- | --- |
| `name` | empty | the stage's column label; empty: `Stage <n>` by its place |
| `source` | `site` | `site` (a protocol on the site) or `sheet` (a Google Forms sheet) |
| `token` | empty | the stage event's upload token; empty: the cup event's |
| `section` | 1 | the stage event's protocol section, for a site protocol |
| `link` | empty | the response sheet's link, for a sheet |
| `rule` | `place_lower_better` | the stage rule |
| `leader_laps_only` | true | a site protocol: a result counts only beside the laps of its category's leader |

## Sources

### A protocol on the site (`app/site_api.py`, `app/protocol_reader.py`)

1. The upload token is looked up (`GET /api/v1/participants/?competition_token=`) for the
   event's id and title; each token once per build. An event the site does not know stops
   the build.
2. The event's protocols are listed (`GET /api/v1/protocols/?competition_id=`); in the
   stage's section the group protocol is taken, else the absolute one. Neither stops the
   build.
3. The protocol's structured document is read (`GET /api/v1/protocols/<id>`). A protocol
   whose last upload brought no data the site took -- HTML alone, or data it refused --
   has none and stops the build: it has to be published with data the site takes (the
   timing tool's log has the site's reason for a refusal).

Both reads carry the stage's upload token (`competition_token`), which the site takes for
an invite-only or hidden event too (cycling-site, 2026-11-24); a site without that reads
only a published event's protocols and ignores the token.

The document is read by the columns' roles: `bib`, `name`, `team`, `result`. Every
section with rows is read, nested ones too; a row's category is its own `group`, else its
section's (inherited down the nesting). A row without a bib is skipped. An athlete listed
twice -- an absolute table and a group table of one run -- is read where first listed. A
row whose `status` is `dns`, `dnf` or `dsq` has no result, whatever its result cell says;
so has a result that is not a number or a time.

Laps have no role: they are the columns named `lap<n>`, as the finish protocol generator
writes them when it shows lap times (`lap<n>_s<m>`, a split, is no lap), and a row's laps
are those of its lap cells that hold a time. With `leader_laps_only` a result counts only
beside as many laps as its category's leader has -- the most among the category's
results; a rider short of them has no result in that stage, as one who did not finish,
and the log names them. A protocol without lap columns leaves every result counted. The
generator writes the attempts of a Number of Tries race in the same columns, so a stage
of one has the setting off. The maintainer's word of 2026-11-24
([`docs/regulations/lap-races/decisions.txt`](../../docs/regulations/lap-races/decisions.txt)).

### A Google Forms response sheet (`app/sheets.py`)

The form asks two questions, in this order: the bib, then the result. The sheet's link
is turned into its CSV export, its tab (`gid`) kept; a link without a tab exports the
first one. A link of a sheet published to the web (`/d/e/<id>/...`) is turned into its
published CSV, its tab kept too. The columns are read by position -- the timestamp
Google adds, the bib, the result -- so the questions may be worded in any language.
Rows are read in the sheet's order, the order Google wrote the answers in, which may
part from their timestamps by a second; a blank row is skipped.

- The first readable answer for a bib counts. A later answer for the same bib is never
  taken; it is reported, with both values and the line that counts.
- Reported, line by line: a row with fewer than three columns, a row without a bib, a
  result that is neither a number nor a time, an answer given again.
- An answer that cannot be read leaves the next one for that bib to count.
- A web page in place of the export (a sign-in page) stops the build and says to share
  the sheet as "Anyone with the link: Viewer". An unshared sheet that answers HTTP 401
  stops it with that status.
- A sheet names nobody: its bibs get names and categories from the site's stages.

### Bibs and results (`app/results.py`)

A bib is compared without spaces, a number without leading zeros, letters in capitals
(`007` is `7`, `a7` is `A7`). A result is a number (`12`, `2,35`) or a time
(`8.43`, `0:08.43`, `12:05`, `1:02:33.4`, with a dot or a comma before the fraction) in
seconds; a unit under a larger one stays under 60. Anything else (`DNF`, a word, a minus)
is no result. The result is also kept as its source wrote it, to show.

## Athletes and categories

The athletes -- bib, name, team, category -- come from the stages read from site
protocols, the first stage that lists somebody naming them; the categories' labels from
those protocols' `groups`. A cup whose stages name nobody (sheets alone) is not built.
A bib a sheet gives a result to but no protocol names is reported.

## Rules (`app/rules.py`)

A stage rule turns one category's results of one stage into a place and points for every
athlete with a result; a cup rule adds a category's stages up into a total and a place.
Rules are picked from drop-downs; a rule's key is what the settings keep.

| Stage rule | What it does |
| --- | --- |
| `place_lower_better` (stub) | a place by the result, the lowest first; the place is the points |
| `place_higher_better` (stub) | a place by the result, the highest first; the place is the points |
| `time` | a place by the time, the lowest first; the time in seconds is the points |
| `minus_second_per_repetition_test` (test) | a place by the count, the highest first; the count as minus seconds is the points, a second off the cup's sum of times per repetition |

| Cup rule | What it does |
| --- | --- |
| `sum_smallest_wins` (stub) | the stages' points added up, the smallest sum first |
| `sum_of_times` | the stages' times added up, the smallest sum first, the total written as a time |

- Equal results share a place and the next place is skipped (1, 2, 2, 4).
- Sums are rounded to a millionth before they are compared, so equal sums of different
  times share a place.
- Somebody without a result in a stage gets no total and no place -- unless everybody is
  placed: then everybody is, those who missed fewer stages first, each group by the sum
  of the stages it has, the places running on across the groups. Somebody with no stage
  at all shares the last place, with no total.
- A cup rule that adds times up refuses a stage not scored by its time, and a stage
  scored by its time refuses a cup rule that does not add times up; the refusal names the
  rule to pick.
- `time` and `sum_of_times` are the maintainer's
  ([`docs/regulations/sum-of-times/decisions.txt`](../../docs/regulations/sum-of-times/decisions.txt));
  the stubs stand in until a cup's regulations replace them.
  `minus_second_per_repetition_test` is made up for testing all-round events, by the
  maintainer's word of 2026-11-23 (no all-round regulations yet), and may be deleted.

## The standing (`app/scoring.py`)

Every category is counted on its own, the categories in the order the athletes come in.
The placed come first, by place, a shared place keeping the order the athletes are listed
in; then everybody without a place, who missed fewer stages first.

## The protocol (`app/document.py`)

The site's structured document, schema 1 (`tests/fixtures/protocol-document-v1.json` is
the site's schema). One table per category, titled by the category's label and declared
in `groups`; athletes without a category make one untitled table.

| Column | Role | Cell |
| --- | --- | --- |
| Place | `place` | the cup place; empty without one |
| Bib | `bib` | |
| Name | `name` | |
| Team | `team` | only when anybody has one |
| a column per stage | | the result as its source wrote it, `<n> pl.` under it; empty without a result |
| Total | `result` | the total: a number, or a time when the cup adds times up |

A total that is a time is written as `m:ss` below an hour, `h:mm:ss` from one on, a
minus before a negative one -- with as many decimals as the most precise of the
athlete's stage results is written with. The title is the `title` setting, else the cup
event's title.

## Publishing

`POST /api/v1/protocols/upload/`: the cup event's token, `protocol_type` `absolute`, the
section, `stage_label` (the `title` setting), `is_live` (true unless `final`), and the
document as `protocol.json`. The site's reason for not taking the document
(`document_error`) is reported; so is an HTTP failure.

## The window (`app/main_window.py`)

- **Cup** tab: the cup's settings, Build, Publish and a status line.
- **Stages** tab: a tab per stage, titled by its name (an unnamed one by its place, as
  the protocol names it): where its results come from -- a site protocol by token and
  section, with the laps checkbox, or a sheet by its link, the other source's fields
  hidden -- and its rule. A
  copy of the current stage is added to its left or right; the last stage cannot be
  deleted.
- **Log** tab: everything the last build said and what publishing said since.

Build saves the settings and reads every stage. Its log is every line the build reported
and `Built: <n> table(s)`; a line that is an error starts with `ERROR:` --
`ERROR: <stage>: line <n>: ...` for a sheet's line, `ERROR: <stage>: bibs no protocol
names: ...` -- and the other lines say how many results a stage gave and whom it did not
count for fewer laps than their leader (`<stage>: not counted, fewer laps than their
leader: <bibs>`). The status line says
`Built: <n> table(s)`, and how many errors with a pointer to the Log tab when there were
any. A build that cannot be made says `Not built: <why>`, the stage named first when the
stage is the reason.

Publish is enabled only by a build, and any change to a setting disables it until the
next one, so what goes to the site is what the log just showed. It says `Published to
section <n>`, `The site did not take the protocol: <why>` or `Not published: <why>`. The
settings are saved on closing too.
