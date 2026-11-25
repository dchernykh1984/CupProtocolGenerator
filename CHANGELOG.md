# Changelog

## [0.5.1](https://github.com/dchernykh1984/CupProtocolGenerator/compare/v0.5.0...v0.5.1) (2026-11-25)


### Bug Fixes

* **document:** the stage columns ask the site for "end", the alignment it draws, not "right" ([1b048b6](https://github.com/dchernykh1984/CupProtocolGenerator/commit/1b048b68808af0c2a70c0c11c43737dccb0fe8cf))

## [0.5.0](https://github.com/dchernykh1984/CupProtocolGenerator/compare/v0.4.0...v0.5.0) (2026-11-24)


### Features

* **document:** every stage's place in a column of its own beside its result ([8bbf38b](https://github.com/dchernykh1984/CupProtocolGenerator/commit/8bbf38b27065d30614a922c261389cc8a308ac89))
* **rules:** a cup by the smallest sum of places, or by the largest sum of results as points ([db6b95d](https://github.com/dchernykh1984/CupProtocolGenerator/commit/db6b95de0fd2727564ed64ddec12d3065de4c359))
* **scoring:** in a place stage, everybody without a result shares the place after the rest ([3d0aff6](https://github.com/dchernykh1984/CupProtocolGenerator/commit/3d0aff6c47f8518bc177f7ba222b31ddb9739225))


### Bug Fixes

* **config:** a save a full disk cuts short leaves the old settings file whole ([5a614cc](https://github.com/dchernykh1984/CupProtocolGenerator/commit/5a614cca52130c706beb4a77b63b84bb9e03c86a))
* **config:** a save keeps the settings file's own permissions, and a new file is its owner's alone ([52ad1d1](https://github.com/dchernykh1984/CupProtocolGenerator/commit/52ad1d164807a88b41634f8a18b627dc249fec1c))
* **config:** a settings file made read-only is refused, not saved over ([9debc55](https://github.com/dchernykh1984/CupProtocolGenerator/commit/9debc5559db8f55b2a30833b259401e5cdd45a06))
* **config:** a settings file reached through a link is saved through it, the link kept ([7e59f12](https://github.com/dchernykh1984/CupProtocolGenerator/commit/7e59f12f85f8e742e48d6f0927fd2a2e1a9e9eab))
* **config:** a settings file that cannot be read is kept aside and said, not saved over ([61b1249](https://github.com/dchernykh1984/CupProtocolGenerator/commit/61b1249312069c9b3c831902abf968967e91408e))
* **config:** a settings file that could neither be read nor kept aside is never saved over ([d22dcd2](https://github.com/dchernykh1984/CupProtocolGenerator/commit/d22dcd24db540e0c34d50b83fb841ce212764f86))
* **config:** a settings file with a byte order mark keeps its settings, not the defaults ([834c814](https://github.com/dchernykh1984/CupProtocolGenerator/commit/834c81456054ce8abbc4454ef8c521e40e904544))
* **config:** a writable settings file in a folder the program may not write to is saved in place, as before ([1f58e82](https://github.com/dchernykh1984/CupProtocolGenerator/commit/1f58e8236a48cb0e4811938b103d491b3e5e75af))
* **document:** a total with a fraction keeps every digit, not six of them ([d3c9a3a](https://github.com/dchernykh1984/CupProtocolGenerator/commit/d3c9a3aae32ae06fa844d29796c3181491c9cb29))
* **results:** a time and the same time written in seconds are one value, so their tie holds ([f73fd08](https://github.com/dchernykh1984/CupProtocolGenerator/commit/f73fd08728d87a5a59de862011b0349cc4565542))
* **rules:** the smallest sum of places says everybody without a result takes the place after the rest ([d8e35cb](https://github.com/dchernykh1984/CupProtocolGenerator/commit/d8e35cbb1f8b468c432e2dfa6836892529f6eeae))
* **sheets:** a sheet link with a capital in its scheme still becomes its CSV export ([bf84e98](https://github.com/dchernykh1984/CupProtocolGenerator/commit/bf84e9852e9da5155d339119a70b2578f85164fd))
* **sheets:** a sheet link with a space or a letter outside ASCII is refused with the stage named, not an unexpected error ([5defd78](https://github.com/dchernykh1984/CupProtocolGenerator/commit/5defd78f5e1f89c29b18080161a27b552a44b252))
* **site:** a site address typed in capitals is still a web address ([996be0c](https://github.com/dchernykh1984/CupProtocolGenerator/commit/996be0cce8441c1f4af30c81f1afb2b2362e987e))
* **site:** a site address with a letter outside ASCII is refused before any request, not blamed on the answer ([2c62ba6](https://github.com/dchernykh1984/CupProtocolGenerator/commit/2c62ba6c182ac908ee93035d3e44edeef9db925d))
* **site:** a site address with a space or a control character is refused before it shows the token ([bd088b5](https://github.com/dchernykh1984/CupProtocolGenerator/commit/bd088b5e0c456a2ade92b71ff0e8a4fbde05912a))
* **site:** a site address without https:// is refused before a request can show the token ([e87daa9](https://github.com/dchernykh1984/CupProtocolGenerator/commit/e87daa94ddc861c79acaf410416c21353143b1c3))
* **site:** a timeout or a dropped connection is a site error, named with its stage ([fd61e2c](https://github.com/dchernykh1984/CupProtocolGenerator/commit/fd61e2cc103a3f9c4f6a7c7db77b7fcbffc32eea))
* **window:** a build that fails leaves nothing to publish, not the build before it ([b78d5e9](https://github.com/dchernykh1984/CupProtocolGenerator/commit/b78d5e9623286ae432d724d3b47769273fc65247))
* **window:** settings that cannot be saved are said, at a build and on closing ([d6bb363](https://github.com/dchernykh1984/CupProtocolGenerator/commit/d6bb363ef13350c5ba051832f11b84af3931725a))


### Documentation

* a cup by the sum of places or of results as points, every stage's place in a column ([2bf3d8f](https://github.com/dchernykh1984/CupProtocolGenerator/commit/2bf3d8f72a8bfeb7d685337e37077180ff477e29))
* **agents:** the test rule's note is a paragraph of its own, not part of the last rule's bullet ([1fb131d](https://github.com/dchernykh1984/CupProtocolGenerator/commit/1fb131d8bd7117ff100ccf79548404eb9de21c3d))
* **config:** an unreadable settings file is kept aside when it can be, and the line says when not ([7e9e953](https://github.com/dchernykh1984/CupProtocolGenerator/commit/7e9e9534c754197f82ba84effc1cea6dd77009e0))
* in a place stage everybody without a result shares the place after the rest ([39e32d4](https://github.com/dchernykh1984/CupProtocolGenerator/commit/39e32d426c6f427bdf41527ac1dfc5eb95b9454c))
* **regulations:** a missed stage is unplaced only in a sum of results, as the decision above it says ([a4cb5ef](https://github.com/dchernykh1984/CupProtocolGenerator/commit/a4cb5efcf3b8c1f4c1da3b0640183f504c348b36))
* **regulations:** the reworded line is wrapped at the width of the rest ([2cc829c](https://github.com/dchernykh1984/CupProtocolGenerator/commit/2cc829c3c8452a1dd68b85b8539809f4749eca50))
* **rules:** Better is the way a result, a stage's points or a cup's sum improves ([8f57749](https://github.com/dchernykh1984/CupProtocolGenerator/commit/8f577492e3fa36ef48f57be13576d252b329615d))
* **rules:** the three new rules quote the decision each comes from ([ed2807a](https://github.com/dchernykh1984/CupProtocolGenerator/commit/ed2807a05ac23ee86f6ceedb31c4a3ca6ea9f9cc))
* **scoring:** a cup row's stage is None only where the stage does not score the athlete ([e7facf9](https://github.com/dchernykh1984/CupProtocolGenerator/commit/e7facf92b20fdf9082b2b96cb0e952e0e809a72d))
* **spec:** a stage's place is empty only where the stage does not score somebody ([feca3a2](https://github.com/dchernykh1984/CupProtocolGenerator/commit/feca3a29c4b9349a4690eeb6ecd43547f6c0f8e6))
* **spec:** settings not saved come after Not built when the build fails ([d341e38](https://github.com/dchernykh1984/CupProtocolGenerator/commit/d341e38f4c8927fae2e925dd32e0a9e2ba6d4337))
* **spec:** what the window and the site connector say when saving or reaching the site fails ([f8ff9f8](https://github.com/dchernykh1984/CupProtocolGenerator/commit/f8ff9f823f934cb459eb155b749f7592f9b26d47))

## [0.4.0](https://github.com/dchernykh1984/CupProtocolGenerator/compare/v0.3.0...v0.4.0) (2026-11-24)


### Features

* a lap race counts only riders with their leader's laps ([12f4dfa](https://github.com/dchernykh1984/CupProtocolGenerator/commit/12f4dfad9df838b188a62cac48dffb8cca78ff48))
* **pipeline:** mark what a build could not read as ERROR lines ([a432424](https://github.com/dchernykh1984/CupProtocolGenerator/commit/a43242476b9482a702791812cea56bb80a218b94))
* **rules:** a made-up all-round stage rule for testing, a second off per repetition ([85bcfd5](https://github.com/dchernykh1984/CupProtocolGenerator/commit/85bcfd5ee4231ce0d21987ddcb705c4c0b950a99))
* **sheets:** the last answer for a bib counts, so a judge can correct a mark ([d2088bc](https://github.com/dchernykh1984/CupProtocolGenerator/commit/d2088bcd783b4b0e30f47007ec6ea637f6970588))
* **site:** read a stage's protocols by its upload token, an invite-only event's too ([baf20d5](https://github.com/dchernykh1984/CupProtocolGenerator/commit/baf20d51b37deca6d9cf56cbfe2177c3c5139408))
* **window:** the log on a tab of its own, a status line on the Cup tab ([0a3436b](https://github.com/dchernykh1984/CupProtocolGenerator/commit/0a3436b3c934216c335d7c735f7c3785e518ec77))


### Bug Fixes

* **pipeline:** say a protocol without data may have had its data refused ([d04eb92](https://github.com/dchernykh1984/CupProtocolGenerator/commit/d04eb92d0ee1bd41f7b37cb305daf6e72c8159ba))
* **reader:** a rider who missed the start check leads no laps, as in the timing generator ([0056b14](https://github.com/dchernykh1984/CupProtocolGenerator/commit/0056b1401888dc945f0871517d71d1168ec22796))
* **reader:** the leader still on course sets the laps a live cup counts ([e72c0f8](https://github.com/dchernykh1984/CupProtocolGenerator/commit/e72c0f8043400c5442d7841063f5de6030a808b7))
* **sheets:** read a sheet published to the web by its published link ([e1e2e67](https://github.com/dchernykh1984/CupProtocolGenerator/commit/e1e2e679a62c96e3a550cbd2ec82dc5c4c31bf31))
* **site:** keep the upload token out of an invalid answer's message ([6d0670c](https://github.com/dchernykh1984/CupProtocolGenerator/commit/6d0670cc18d5e6ebfd3e42095bc91abdba81cd33))
* **window:** show the status line as plain text, never as markup ([4a1be3a](https://github.com/dchernykh1984/CupProtocolGenerator/commit/4a1be3a1dd0cfd2f76479b4efce9a6186012fbca))


### Documentation

* a lap race counts only riders with their leader's laps ([8f7dab3](https://github.com/dchernykh1984/CupProtocolGenerator/commit/8f7dab3bc04c1993e66c7e5d85bd0c38eaf5891a))
* a live lap race needs the timing tool to print its DNF riders ([fa2ac06](https://github.com/dchernykh1984/CupProtocolGenerator/commit/fa2ac0684661430c3531db58ab178934a90e2f61))
* a rider who abandoned leads the laps as one still on course does ([e571beb](https://github.com/dchernykh1984/CupProtocolGenerator/commit/e571beb229a19e4a6fedada76933fadd1b6daf7a))
* a stage's protocols are read by its upload token ([6d68348](https://github.com/dchernykh1984/CupProtocolGenerator/commit/6d683482f4b48cbfaf2722e8a84b712b194d6631))
* add the program's specification ([dab3e1b](https://github.com/dchernykh1984/CupProtocolGenerator/commit/dab3e1b22115d24c35b7126e202a0656fbb59af8))
* name the made-up test rule in the cup-rules skill ([bd4f559](https://github.com/dchernykh1984/CupProtocolGenerator/commit/bd4f5590bb695b4bd18bcf5f6d14092bdab739db))
* **results:** drop the claim that totals are written as the timing tools write ([48e5777](https://github.com/dchernykh1984/CupProtocolGenerator/commit/48e5777a08d75f8551cc51411f3b1e26e616e698))
* **sheets:** say the rows are read in the sheet's order, not the timestamps' ([52003cb](https://github.com/dchernykh1984/CupProtocolGenerator/commit/52003cbe696a8110f696517e0a5be958675c906f))
* the agent docs name the lap rule beside the rules ([4416740](https://github.com/dchernykh1984/CupProtocolGenerator/commit/4416740d823c71e2f4724e934edb120ebd5036e7))
* the log has a tab of its own ([7aeff36](https://github.com/dchernykh1984/CupProtocolGenerator/commit/7aeff36ee4ea2019cdd56e871ad5ead354cd6283))
* the last sheet answer counts, every one it replaces is an error ([ea5776b](https://github.com/dchernykh1984/CupProtocolGenerator/commit/ea5776bcceb3f7516b3b539145c0516094d58d5c))
* the README says the last readable sheet answer counts, an unreadable one replaces nothing ([cbb1c38](https://github.com/dchernykh1984/CupProtocolGenerator/commit/cbb1c38e37dc2449f85b989f80ce21ef30e392ad))
* wrap the lap-rule paragraphs as the rest is wrapped ([1381281](https://github.com/dchernykh1984/CupProtocolGenerator/commit/138128162ca2fdf5f5160f0198408aff87836ea4))
* wrap the spec's paragraphs as the rest of it is wrapped ([44ec1da](https://github.com/dchernykh1984/CupProtocolGenerator/commit/44ec1da2e3ff4fa5c6a61d533e352bc9cb01e88e))

## [0.3.0](https://github.com/dchernykh1984/CupProtocolGenerator/compare/v0.2.0...v0.3.0) (2026-11-19)


### Features

* **config:** keep whether a build places everybody, for a broadcast ([32df0c3](https://github.com/dchernykh1984/CupProtocolGenerator/commit/32df0c3e8768fa7f2ef1d341042c24a7041758f1))
* **rules:** place everybody on request, who missed more stages lower ([b7e7837](https://github.com/dchernykh1984/CupProtocolGenerator/commit/b7e7837f9fd1e7103a9104d25dacccee51fb9d9e))
* **scoring:** list the unranked by how many stages they missed, fewer first ([4e22a08](https://github.com/dchernykh1984/CupProtocolGenerator/commit/4e22a088275f9eae66847bd8d8d7867acd27c344))
* **window:** a checkbox to place everybody, for a broadcast ([df43731](https://github.com/dchernykh1984/CupProtocolGenerator/commit/df43731edb91b0a658a198ae4266d41f8d375bf9))


### Bug Fixes

* **window:** word the broadcast checkbox so it reads one way ([cc1b955](https://github.com/dchernykh1984/CupProtocolGenerator/commit/cc1b955390c90666587f15b32d4a1c4ce8858b8c))


### Documentation

* record the maintainer's confirmation of the sum-of-times decisions ([879fd7d](https://github.com/dchernykh1984/CupProtocolGenerator/commit/879fd7d9ea6ad9845e6591abba0778c7de38d21a))
* **rules:** quote the broadcast word as it was said ([689e82c](https://github.com/dchernykh1984/CupProtocolGenerator/commit/689e82c1525c444cffa00d18ac4e710711744a91))
* **rules:** say whose word places everybody for a broadcast ([2a579c1](https://github.com/dchernykh1984/CupProtocolGenerator/commit/2a579c14f0a3b3790d3a7e52c11754da6536ee52))
* say how a broadcast places everybody who missed stages ([d992f8b](https://github.com/dchernykh1984/CupProtocolGenerator/commit/d992f8b80ed1457f7a269d0308537c02ad344c68))
* say in the README where the unranked go and that a broadcast places them ([1afd0ea](https://github.com/dchernykh1984/CupProtocolGenerator/commit/1afd0eae37cff221bef87cd51db083921cfa5d8e))

## [0.2.0](https://github.com/dchernykh1984/CupProtocolGenerator/compare/v0.1.2...v0.2.0) (2026-11-18)


### Features

* **pipeline:** refuse a stage not scored by its time when the cup adds times up ([9961120](https://github.com/dchernykh1984/CupProtocolGenerator/commit/99611203a610ea7a80831838bd4381e3e3647ffa))
* **rules:** add the stages' times up as the cup's total, written as a time ([76dc65f](https://github.com/dchernykh1984/CupProtocolGenerator/commit/76dc65f074b43203b0854b61d5f0440e17fad454))
* **rules:** score a stage by its time, kept as the stage's points ([e2ad36a](https://github.com/dchernykh1984/CupProtocolGenerator/commit/e2ad36a62a9ca40557b336506e1fdc1ed84b63e4))


### Bug Fixes

* **pipeline:** name the cup rule to pick for a stage counted by its time ([672c5a6](https://github.com/dchernykh1984/CupProtocolGenerator/commit/672c5a66646022410a711f4eb57365bff9e012e8))
* **pipeline:** name the stage rule to pick when the cup rule adds times up ([390a333](https://github.com/dchernykh1984/CupProtocolGenerator/commit/390a33392d66441aa820ae35ae558bf3185fd429))
* **pipeline:** refuse a stage counted by its time when the cup rule adds places up ([5dbfaed](https://github.com/dchernykh1984/CupProtocolGenerator/commit/5dbfaedec951fe6051e04904a20ac6b304c76d7b))


### Documentation

* name the cup rule in the README as its drop-down does ([55c775a](https://github.com/dchernykh1984/CupProtocolGenerator/commit/55c775a89edd63bb6f3480743d709cc00a6977a9))
* **results:** say the module writes a sum of times back as a time ([b318721](https://github.com/dchernykh1984/CupProtocolGenerator/commit/b31872142de6e699603b2ae62db1bc4894d02658))
* **rules:** say which float noise the sum of times is rounded against ([65ce0f8](https://github.com/dchernykh1984/CupProtocolGenerator/commit/65ce0f89c36347b3624ba06431085414c391aaa1))
* **rules:** say whose word the time rules come from ([e74ca2c](https://github.com/dchernykh1984/CupProtocolGenerator/commit/e74ca2cdcfb6d2aa19b5d04aff856dc8cde863cc))
* say how a cup of summed times is counted and shown ([3b91c97](https://github.com/dchernykh1984/CupProtocolGenerator/commit/3b91c979d9faed438ab05923ed380794082345b0))

## [0.1.2](https://github.com/dchernykh1984/CupProtocolGenerator/compare/v0.1.1...v0.1.2) (2026-11-18)


### Documentation

* a pull request from the maintainer's account needs --admin only while nobody else approved it ([1c17154](https://github.com/dchernykh1984/CupProtocolGenerator/commit/1c171545e151b0f67738fdcd9fea0e1a7b3a1512))
* carry the pipeline-repair exception into the shipping skill ([1e06f36](https://github.com/dchernykh1984/CupProtocolGenerator/commit/1e06f362afe8590178a4da0460145c728fdea825))
* give merging a section of its own in the shipping skill ([f5ac595](https://github.com/dchernykh1984/CupProtocolGenerator/commit/f5ac595da8f4d81bd5f6b155dba5e6c3967a95d2))
* how pull requests merge under main's ruleset ([42dee72](https://github.com/dchernykh1984/CupProtocolGenerator/commit/42dee7278a43cbedb411fce2476f637ffdee20a9))
* name every commit type release-please releases, docs included ([5c95a4c](https://github.com/dchernykh1984/CupProtocolGenerator/commit/5c95a4c2698d1266ad76390958ab2cffe14b9d60))
* name the Actions setting release-please's pull request needs ([abe8f92](https://github.com/dchernykh1984/CupProtocolGenerator/commit/abe8f92b13aa94cccd23200283809d34709dd914))
* questions name a concrete gap, and an issue's claims are checked first ([ceb17a4](https://github.com/dchernykh1984/CupProtocolGenerator/commit/ceb17a40a1c3ca814be25dde682c997320af9057))
* word the questions rule so it cannot be read the other way ([485aec5](https://github.com/dchernykh1984/CupProtocolGenerator/commit/485aec5b91a9474db33e105259def247e07d2686))

## [0.1.1](https://github.com/dchernykh1984/CupProtocolGenerator/compare/v0.1.0...v0.1.1) (2026-11-18)


### Documentation

* say how a release is built, checked and rebuilt ([c8a7a57](https://github.com/dchernykh1984/CupProtocolGenerator/commit/c8a7a57b982ab39d965b2007161d767334483ef0))
* wrap the README's paragraph on the pipeline as the rest is wrapped ([e2fefb7](https://github.com/dchernykh1984/CupProtocolGenerator/commit/e2fefb734629fa041da994ca8e8e6594b8820fcf))

## 0.1.0 (2026-11-18)


### Features

* a window with the cup's settings and a tab per stage, to build and publish ([79736ac](https://github.com/dchernykh1984/CupProtocolGenerator/commit/79736ac43594edabed97a37150a6b3313c0be2ea))
* build the cup from its stages and publish it to its section ([ef8effa](https://github.com/dchernykh1984/CupProtocolGenerator/commit/ef8effa301e828d42e58d302fa216dbb76fa70c4))
* connectors to the cycling site by an upload token and to Google Forms sheets ([0ebda06](https://github.com/dchernykh1984/CupProtocolGenerator/commit/0ebda06ba808eb20ae9413ecaabd93d62ed8a10d))
* stage rules and the cup rule, stubs that the regulations will replace ([cfe3b5a](https://github.com/dchernykh1984/CupProtocolGenerator/commit/cfe3b5ab21246a53b4dfd24f15b6f470789f2e87))
* the cup's protocol as the cycling site's structured document ([645e0b4](https://github.com/dchernykh1984/CupProtocolGenerator/commit/645e0b4fbb93c2730fd4623781fa30eadf5f8895))


### Bug Fixes

* a bib typed in small letters matches the same bib in capitals ([dee5a25](https://github.com/dchernykh1984/CupProtocolGenerator/commit/dee5a257bb7fb5c7ace4e8267a038622c237c1e7))
* a bib with a digit int() refuses is kept as text, not a crash of the build ([20c962c](https://github.com/dchernykh1984/CupProtocolGenerator/commit/20c962c08772daf20a9cebcbf17c80492b3bc693))
* a deleted stage's tab is freed, not only taken off the screen ([706f5ef](https://github.com/dchernykh1984/CupProtocolGenerator/commit/706f5ef981db79b0ee92b179baed448c70c392b4))
* a stage the site or Google fails to give is named in the error ([1282388](https://github.com/dchernykh1984/CupProtocolGenerator/commit/128238868c2bd5f6a24ebb6bcb1f224531d018e9))
* an unexpected failure of a build or an upload is said in the log ([58c46ff](https://github.com/dchernykh1984/CupProtocolGenerator/commit/58c46ff4b374667b204252c5791d2896272f3404))
* an unnamed stage's tab keeps the number the protocol will give it ([eca68c7](https://github.com/dchernykh1984/CupProtocolGenerator/commit/eca68c70ce3880948f35773c7528284ad83e01eb))
* the window's stage tabs are typed as they are, and the full mypy run passes ([bf55c36](https://github.com/dchernykh1984/CupProtocolGenerator/commit/bf55c36dc43db9bc0a532b46ee2cdffd705a942a))


### Documentation

* only the project's own mypy checks the window's Qt types, not the hook's ([1f7242f](https://github.com/dchernykh1984/CupProtocolGenerator/commit/1f7242f47e1dcfe3d1ebee5a70118751a0c0d5a3))
* what the cup needs and the window asks for, and how an agent works here ([474fef9](https://github.com/dchernykh1984/CupProtocolGenerator/commit/474fef90dcf79bd86cd9a99d2932d9ebfb59f93c))
