#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `click2cwl.cwlparam` module.
"""

import click
import pytest

import click2cwl


@click.command()
@click.argument("arg")
@click.option("--opt")
def cli_argument(**kwargs):
    ...


def test_argument_required():
    with pytest.raises(click.MissingParameter):
        cli_argument.make_context("cli_argument", [])


def test_argument():
    ctx = cli_argument.make_context("cli_argument", ["val1", "--opt", "val2"])
    c2c = click2cwl.Click2CWL(ctx)
    exp = click2cwl.CWLExport(c2c)
    cwl = exp.to_dict()
    clt = cwl["$graph"][0]

    assert list(clt["inputs"]) == ["arg", "opt"]
    assert clt["inputs"]["arg"] == {"type": "string", "inputBinding": {"position": 1}}
    assert clt["inputs"]["opt"] == {"type": "string?", "inputBinding": {"position": 2, "prefix": "--opt"}}
