#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `click2cwl.cwlparam` module.
"""

import click
import pytest

import click2cwl
from click2cwl.cwlparam import CWLParam


@click.command()
@click.option("--value", type=click.Choice(["A", "B", "C"]), required=True)
def cli_enum(**kwargs):
    ...


def test_enum_dict():
    ctx = cli_enum.make_context("cli_enum", ["--value", "A"])
    c2c = click2cwl.Click2CWL(ctx)
    exp = click2cwl.CWLExport(c2c)
    cwl = exp.to_dict()
    clt = cwl["$graph"][0]
    wf = cwl["$graph"][1]

    assert list(clt["inputs"]) == ["value"]
    assert "symbols" in clt["inputs"]["value"]["type"][0]  # list is used to allow optionally having 'null'
    assert isinstance(clt["inputs"]["value"]["type"][0]["symbols"], list), (
        "ensure symbols are a Python list, not a tuple to make it JSON serializable as array"
    )
    assert clt["inputs"]["value"] == {
        "inputBinding": {"position": 1, "prefix": "--value"},
        "type": [
            {
                "type": "enum",
                "symbols": ["A", "B", "C"],
            }
        ]
    }

    assert list(wf["inputs"]) == ["value"]
    assert "symbols" in wf["inputs"]["value"]["type"][0]
    assert isinstance(clt["inputs"]["value"]["type"][0]["symbols"], list), (
        "ensure symbols are a Python list, not a tuple to make it JSON serializable as array"
    )
    assert wf["inputs"]["value"] == {  # no binding here since they are in 'steps' between wf/clt
        "type": [
            {
                "type": "enum",
                "symbols": ["A", "B", "C"],
            }
        ]
    }


@click.command()
@click.option("--value", type=click.Choice(["A", "B", "C"]), required=True)
def cli_enum(**kwargs):
    ...


def test_enum_dict():
    ctx = cli_enum.make_context("cli_enum", ["--value", "A"])
    c2c = click2cwl.Click2CWL(ctx)
    exp = click2cwl.CWLExport(c2c)
    cwl = exp.to_dict()
    clt = cwl["$graph"][0]
    wf = cwl["$graph"][1]

    assert list(clt["inputs"]) == ["value"]
    assert "symbols" in clt["inputs"]["value"]["type"][0]  # list is used to allow optionally having 'null'
    assert isinstance(clt["inputs"]["value"]["type"][0]["symbols"], list), (
        "ensure symbols are a Python list, not a tuple to make it JSON serializable as array"
    )
    assert clt["inputs"]["value"] == {
        "inputBinding": {"position": 1, "prefix": "--value"},
        "type": [
            {
                "type": "enum",
                "symbols": ["A", "B", "C"],
            }
        ]
    }

    assert list(wf["inputs"]) == ["value"]
    assert "symbols" in wf["inputs"]["value"]["type"][0]
    assert isinstance(clt["inputs"]["value"]["type"][0]["symbols"], list), (
        "ensure symbols are a Python list, not a tuple to make it JSON serializable as array"
    )
    assert wf["inputs"]["value"] == {  # no binding here since they are in 'steps' between wf/clt
        "type": [
            {
                "type": "enum",
                "symbols": ["A", "B", "C"],
            }
        ]
    }


@pytest.mark.parametrize(
    ["click_type", "cwl_type"],
    [
        (click.Option(["--test"], type=int), "int"),
        (click.Option(["--test"], type=float), "float"),
        (click.Option(["--test"], type=str), "string"),
        (click.Option(["--test"], type=click.INT), "int"),
        (click.Option(["--test"], type=click.FLOAT), "float"),
        (click.Option(["--test"], type=click.STRING), "string"),
        (click.Option(["--test"], type=click.UUID), "string"),
        (click.Option(["--test"], type=click.DateTime()), "string"),
        (click.Option(["--test"], type=click.Choice([1, 2])), "enum"),
        (click.Option(["--test"], type=click.Path()), "Directory"),
        (click.Option(["--test"], type=click.File()), "File"),
    ]
)
def test_param_mapping(click_type, cwl_type):
    param = CWLParam(click_type)
    assert param.get_type() == cwl_type
