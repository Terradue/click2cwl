import yaml


def dump_file(ctx, type_of_file, clt_dict, wf_dict):
    if type_of_file == 'cwl':
        with open(ctx.command_path + '.cwl', 'a') as file:
            yaml.dump(clt_dict, file)
            yaml.dump(wf_dict, file)
            file.close()
    elif type_of_file == 'params':
        with open(ctx.command_path + '.yml', 'a') as file:
            yaml.dump(ctx.params, file)
            file.close()
