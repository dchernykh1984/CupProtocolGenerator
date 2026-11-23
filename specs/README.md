# Specifications

The specification of Cup Protocol Generator: what the program does, as the referee and
the readers of its protocol see it.

```
specs/
  app/                        the program as it works today
    cup-protocol.md           settings, sources, rules, the protocol, the site, the window
  <NNN>-<short-name>/         one feature, once one is specified ahead of its code
    spec.md                   what and why
    plan.md, tasks.md         how it will be built, once the spec is reviewed
```

**Keep `app/` true.** A change that alters described behaviour updates it in the same pull
request. The rules a cup is counted by come from its regulations, kept in
[`docs/regulations/`](../docs/regulations/); `app/` names the rules that exist, not the
regulations behind them.
