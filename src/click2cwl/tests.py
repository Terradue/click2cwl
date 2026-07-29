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

from .entry import dump


# test1 -i a --dump cwl --requirement ramMax=1 --requirement ramMin=2 --docker aaa  --env a=1 --env b=2
@click.command(
    short_help="hello Im the label of Workflow class",
    help="hello Im the doc of Workflow class",
    context_settings={
        "ignore_unknown_options": True,
        "allow_extra_args": True,
    },
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
    "--optional_reference",
    "-o",
    "optional_reference",
    type=click.Path(),
    help="this input reference is optional",
    multiple=True,
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
@click.option(
    "--flag",
    "flag",
    help="help for the flag ",
    is_flag=True,
)
@click.pass_context
def test1(ctx, **kwargs):
    dump(ctx)

    print("business as usual")
    print(kwargs)

    sys.exit(0)


@click.command(
    context_settings={
        "ignore_unknown_options": True,
        "allow_extra_args": True,
    }
)
@click.option(
    "--input_reference",
    "-i",
    "input_reference",
    help="help for input reference",
    type=click.Path(),
)
@click.option(
    "--aoi",
    "-a",
    "aoi",
    help="help for the area of interest",
    multiple=True,
    default=None,
)
@click.pass_context
def test2(ctx, input_reference, aoi):
    dump(ctx)

    print("business as usual")
    print(input_reference, aoi)

    sys.exit(0)
