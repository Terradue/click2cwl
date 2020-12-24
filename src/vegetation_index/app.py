import sys
import logging
import click
from .cwl_constructor import CwlCreator

logging.basicConfig(stream=sys.stderr,
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')


@click.command(short_help='hello I\'m the label of Workflow class',
               help='hello I\'m the doc of Workflow class',
               context_settings=dict(
                   ignore_unknown_options=True,
                   allow_extra_args=True, ))
@click.option('--input_reference', '-i', 'input_reference', type=click.Path(), required=True)
@click.option('--aoi', '-a', 'aoi', help='help for the area of interest', default=None, type=click.STRING)
@click.option('--file', '-f', 'conf_file', help='help for the conf file', type=click.File())
@click.pass_context
def entry(ctx, **kwargs):
    extra_params = {ctx.args[i][2:]: ctx.args[i + 1] for i in range(0, len(ctx.args), 2)}
    print(ctx.params)
    print(ctx.command.params)
    print(type(ctx.command.params[0].type))
    print(type(ctx.command.params[0].type) == click.Path)

    docker = None
    requirement = None
    env = None
    scatter = None

    if 'requirement' in extra_params.keys():
        requirement = get_key_and_value_of_extra_params(extra_params['requirement'])
    if 'env' in extra_params.keys():
        env = get_key_and_value_of_extra_params(extra_params['env'])
    if 'docker' in extra_params.keys():
        docker = extra_params['docker']
    if 'scatter' in extra_params.keys():
        scatter = get_key_and_value_of_extra_params(extra_params['scatter'])

    cwl_object = CwlCreator(ctx, docker=docker, requirements=requirement, env=env, scatter=scatter)
    if 'dump' in extra_params.keys():
        cwl_object.dump_file(extra_params['dump'])

    sys.exit(0)


def get_key_and_value_of_extra_params(params):
    params_key_and_value = [x.strip() for x in params.split('=')]
    param_dict = {params_key_and_value[0]: params_key_and_value[1]}
    return param_dict


if __name__ == '__main__':
    entry()
