"""
Runs commands from deploy config
"""

import subprocess


def deploy(data, config):
    """ Checks config and runs scripts """

    for field in ['order', 'path']:
        if field not in config:
            raise AttributeError('No {} field in config'.format(field))

    for step in config['order']:
        step_commands = config.get(step)
        commands_list = (
            # if it is one command in step,
            # convert it into a list for easy iteration
            [step_commands], step_commands
        )[isinstance(step_commands, list)]

        for command in commands_list:
            if not command:
                raise KeyError(
                    'No command \'{}\' in your config'.format(command)
                )
            completed_process = subprocess.run(
                command,
                cwd=config.get('path'),
                shell=True
            )

            print(completed_process)

    return ''

# print(action)
# output, err = call.communicate()
# if (output):
#     print('output: ' + str(output))
# if (err and action['name'] != 'build'):
#     print('err: ' + str(err))
#     if action['name'] == 'start':
#         return action['errMessage']


# deploy('frontend')
