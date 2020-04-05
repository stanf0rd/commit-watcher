"""
Runs commands from deploy config
"""

# Standard library imports
import os
import shutil
import subprocess
from io import BytesIO
from zipfile import ZipFile

# Third party imports
import requests


def deploy(data, config):
    """ Checks config and runs scripts """

    check_config(config)

    branch = data.get('ref').split('/')[-1]
    if branch != config.get('branch'):
        return

    load_src(config.get('repo_name'), config.get('path'))

    for step in config['order']:
        step_commands = config.get(step)

        # if it is one command in step,
        # convert it into a list for easy iteration
        commands_list = (
            step_commands if isinstance(step_commands, list)
            else [step_commands]
        )

        for command in commands_list:
            if not command:
                raise KeyError(
                    'No command \'{}\' in your config'.format(command)
                )
            completed_process = subprocess.run(
                command,
                cwd=config.get('path'),
                shell=True,
                check=True,
            )

            print(completed_process)

    return ''


def check_config(config):
    """ Raises errors if some of fields is missed """
    for field in ['order', 'path', 'branch']:
        if field not in config:
            raise AttributeError('No {} field in config'.format(field))


def load_src(repo_name, path):
    """ Downloads project to directory by path """
    clear_dir(path)

    response = requests.get(
        'https://api.github.com/repos/' + repo_name + '/zipball'
    )

    print('response status:', response.status_code)

    packed = ZipFile(BytesIO(response.content))
    packed.extractall(path)


def clear_dir(path):
    """ Remove all files and subdirs from directory """
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


# print(action)
# output, err = call.communicate()
# if (output):
#     print('output: ' + str(output))
# if (err and action['name'] != 'build'):
#     print('err: ' + str(err))
#     if action['name'] == 'start':
#         return action['errMessage']


# deploy('frontend')
