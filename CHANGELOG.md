# Changelog

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
