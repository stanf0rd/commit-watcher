import subprocess
from config import DEPLOY_CONFIG


def deploy(repo_name):
    if not repo_name in DEPLOY_CONFIG:
        raise AttributeError('No repo \'{}\' in your config'.format(repo_name))

    config = DEPLOY_CONFIG.get(repo_name)

    for field in ['order', 'path']:
        if not field in config:
            raise AttributeError('No {} field in config'.format(field))

    for step in config['order']:
        stepCommands = config.get(step)
        commands_list = (
            # if it is one command in step,
            # convert it into a list for easy iteration
            [stepCommands], stepCommands
        )[isinstance(stepCommands, list)]

        for command in commands_list:
            if not command:
                raise KeyError('No command \'{}\' in your config'.format(command))
            completed_process = subprocess.run(command, cwd=config.get('path'), shell=True)
            print(completed_process)


        # print(action)
        # output, err = call.communicate()
        # if (output):
        #     print('output: ' + str(output))
        # if (err and action['name'] != 'build'):
        #     print('err: ' + str(err))
        #     if action['name'] == 'start':
        #         return action['errMessage']


deploy('frontend')
