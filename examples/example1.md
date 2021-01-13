## Example 1 

Python code:

```python
import sys
import click
from click2cwl import dump

@click.command(
    short_help="hello Im the label of Workflow class",
    help="hello Im the doc of Workflow class",
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ),
)
@click.option(
    "--input_reference",
    "-i",
    "input_reference",
    type=click.Path(),
    help="this input reference",
    multiple=False,
    required=True,
)
@click.option(
    "--aoi",
    "-a",
    "aoi",
    help="help for the area of interest",
    default="POLYGON()",
    required=False,
)
@click.option(
    "--file",
    "-f",
    "conf_file",
    help="help for the conf file",
    type=click.File(mode="w"),
)
@click.option(
    "--mode", "-m", "mode", type=click.Choice(["local", "ftp"]), required=False
)
@click.pass_context
def test1(ctx, **kwargs):

    dump(ctx)

    print("business as usual")
    print(kwargs)

    sys.exit(0)

```

Invoke with:

```console
test1 --input_reference a --dump cwl --requirement ramMax=1 --requirement ramMin=2 --docker aaa  --env a=1 --env b=2
```

Note: We provide a dummy value to `--input_reference` arg since it's set as `required=True`
