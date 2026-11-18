# Changelog

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
