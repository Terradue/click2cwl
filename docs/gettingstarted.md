# Getting started

Add `click2cwl` dependency and `terradue` channel in your environment.yml file, e.g.:

```yaml
name: my_env
channels:
  - terradue
  - conda-forge
dependencies:
  - python
  - click2cwl
```

## Usage

First import the click2cwl `dump` function with:

```python
from click2cwl import dump
```

Then, in the Python application entry point function, update and enrich the Click function decorator with the information for generating the CWL document.

The information defined at the Click function decorator is explained below:

### @click.command

The `@click.command` decorator must:

- set the `allow_extra_args` flag to `True`. This allows using the command line interface to pass the runtime information to generate the CWL.
- set the `short_help` to define the CWL Workflow class **label**
- set the `help` to define the CWL Workflow class **doc**

```python
@click.command(
    short_help="This is Workflow class label",
    help="This is Workflow class doc",
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ),
)
```

### @click.option

The `@click.option` decorator must:

- define the option type that can be `click.Path` for a `Directory`, a `click.File` for a `File` or the default, a `String` to map as `string`
- set the `help` to define the CWL Workflow class **doc** and **label**
- set the `required` flag to `False` if the parameter is optional

```python
@click.option(
    "--input_path",
    "-i",
    "input_path",
    type=click.Path(),
    help="this input path",
    multiple=False,
    required=True,
)
```

Finally, invoke the `dump` function in your Click decorated function with:

```python
@click.command ...
@click.option ...
@click.pass_context
def main(ctx, **kwargs):

    dump(ctx)

    print("business as usual")
    print(kwargs)

if __name__ == '__main__':
    main()
```

**Note:** See the examples folder to discover typical use cases.

Install your application with:

```console
python setup.py install
```

When the app help is invoked, it will only show the arguments defined by the click.decorators:  

```console
myapp --help
```

but it now supports additional args to drive the generation of the CWL document and associated parameters:

The additional args are:

- `--dump` `cwl`|`params`|`clt`. Example `--dump cwl --dump params` will dump the CWL document and the CWL parameters template in YAML. `clt` will dump the CWl `CommandLineTool` class only (no Workflow)
- `--requirement` with `requirement=value` where requirement here is one of `"coresMin"`, `"coresMax"`, `"ramMin"`, `"ramMax"`. Example: 
 `--requirement ramMax=1 --requirement ramMin=2`
 - `--docker <docker image>` if set, the `DockerRequirement` hint is set to pull the `<docker image>`
 - `--env` sets environment variables in the CWL with `env_var=env_var_value`. Example `--env A=1 --env B=2` where A and B are the environment variables to set in the CWL `EnvVarRequirement` requirement
