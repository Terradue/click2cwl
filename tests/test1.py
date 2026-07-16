# Copyright 2020 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
