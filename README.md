# linkml-integration package
Integration test for various linkml modules.

This module carries the majority of the test cases for the various linkml modules.  It allow one to do a unit test
against any branch of [linkml](https://github.com/hsolbrig/linkml), [linkml-runtime](https://github.com/hsolbrig/linkml-runtime)
and [linkml-model](https://github.com/hsolbrig/linkml-model)

## Layout
```text
linkml-integration
     |
     + config                 -- test harness configuration files
     |
     + src                    -- test harness implementation
     |
     + input                  -- files used for the actual integration test
     |
     + model                  -- LinkML model of test harness
     |
     + output                 -- expected output of the integration tests.  Actual output compared to these
     |
     + submodules             -- submodules being tested (e.g. linkml, linkml-runtime)
     |
     + tests                  -- "meta" tests - testing code for the harness implementation and model
     |
     ...                      -- bookkeeping
```

## Installation
`> git clone --recurse-submodules --remote-submodules git@github.com:hsolbrig/linkml-integration.git`
Edit the following files;
* submodules/linkml-runtime/pyproject.toml
* submodules/linkml/pyproject.toml

Changing the "0.0.0" version identifier to whatever is in pypi + 1.dev.  If, for instance, linkml-runtime is version 1.4.2,
edit the version to be "1.4.3.dev"
