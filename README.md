# Click2CWL - from a Click context to a CWL document

## Rational and context

EO application developers use Click to create command line tools to process EO data.

To deploy those applications on an Exploitation Plaform on the Cloud, the EO application developers generate a CWL document that becomes an Application Package.

The repo contains a helpers Python module that exploits the information contained in a Click context object to generate the CWL document and eventually the parameters.

## Installation

Install this Python module using `conda` or `mamba`:

```console
conda install -c terradue click2cwl
```

## Usage

In the Python application entry point function, update and enrich the Click function decorator with the information for generating the CWL document.

The information defined at the Click function decorator is explained below.

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

The `@click.command` decorator must:

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

See the examples folder to discover typical use cases.

Install your application with:

```console
python setup.py install
```

Use additional args to drive the generation of the CWL document and associated parameters:

The additional args are:

- `--dump` `cwl`|`params`|`clt`. Example `--dump cwl --dump params`
- `--requirement` with `requirement=value` where requirement is one of `"coresMin"`, `"coresMax"`, `"ramMin"`, `"ramMax"`. Example: 
 `--requirement ramMax=1 --requirement ramMin=2`
 - `--docker <docker image>` if set, the DockerRequirement hint is set to pull the `<docker image>`
 - `--env` sets environment variables in the CWL with `env_var=env_var_value`. Example `--env a=1 --env b=2`