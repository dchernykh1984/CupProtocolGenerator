# Changelog

## [0.4.0](https://github.com/dchernykh1984/CupProtocolGenerator/compare/v0.3.0...v0.4.0) (2026-11-24)


### Features

* a lap race counts only riders with their leader's laps ([12f4dfa](https://github.com/dchernykh1984/CupProtocolGenerator/commit/12f4dfad9df838b188a62cac48dffb8cca78ff48))
* **pipeline:** mark what a build could not read as ERROR lines ([a432424](https://github.com/dchernykh1984/CupProtocolGenerator/commit/a43242476b9482a702791812cea56bb80a218b94))
* **rules:** a made-up all-round stage rule for testing, a second off per repetition ([85bcfd5](https://github.com/dchernykh1984/CupProtocolGenerator/commit/85bcfd5ee4231ce0d21987ddcb705c4c0b950a99))
* **sheets:** count the first answer for a bib and report every later one ([39b9c3f](https://github.com/dchernykh1984/CupProtocolGenerator/commit/39b9c3f5ef1a50faa9c27f696aff93ea316b3d6b))
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
* the first sheet answer counts, and the log has a tab of its own ([7aeff36](https://github.com/dchernykh1984/CupProtocolGenerator/commit/7aeff36ee4ea2019cdd56e871ad5ead354cd6283))
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
