import os
import sys
import logging
import click

from .ctx2cwl import CtxCWL
from .clt import CommandLineTool
from .wf import Workflow
from .dump import dump_file

logging.basicConfig(stream=sys.stderr,
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')


@click.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True, ))
@click.option('--input_reference', '-i', 'input_reference', type=click.Path())
@click.option('--aoi', '-a', 'aoi', default=None)
@click.pass_context
def entry(ctx, **kwargs):
    extra_params = {ctx.args[i][2:]: ctx.args[i + 1] for i in range(0, len(ctx.args), 2)}

    requirement_key_and_value = [x.strip() for x in extra_params['requirement'].split('=')]
    requirement = {requirement_key_and_value[0]: requirement_key_and_value[1]}

    clt_dict = CommandLineTool(ctx, docker=extra_params['docker'], requirements=requirement).get_clt()
    wf_dict = Workflow(ctx).get_workflow()

    if 'dump' in extra_params.keys():
        dump_file(ctx, extra_params['dump'], clt_dict, wf_dict)

    print(extra_params)

    print(ctx.params['aoi'])

    sys.exit(0)


if __name__ == '__main__':
    entry()
