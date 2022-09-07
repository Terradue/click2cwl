import sys
import click
from click2cwl import dump

# test1 -i a --dump cwl --requirement ramMax=1 --requirement ramMin=2 --docker aaa  --env a=1 --env b=2
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
    multiple=True,
    required=False,
)
@click.option(
    "--boi",
    "-b",
    "boi",
    help="help for the area of interest",
    default="2",
    required=False,
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
def main(ctx, **kwargs):

    dump(ctx)

    print("business as usual")
    print(kwargs)

    sys.exit(0)
    
if __name__ == "__main__":
    main()
