import subprocess
from config import DEPLOY_CONFIG


def deploy(repo_name):
    if not hasattr(DEPLOY_CONFIG, repo_name):
        raise AttributeError('No such repo in your config')

    config = DEPLOY_CONFIG[repo_name]

    for field in ['order', 'path']:
        if not hasattr(config, field):
            raise AttributeError('No {} attribute in config'.format(field))

    for step in config.order:
        commandsList = (
            # if it is one command in step,
            # make it a list for convinient iteration
            [config[step]], config[step]
        )[isinstance(config[step], list)]

        for command in commandsList:
            completedProcess = subprocess.run(command, cwd=config.path)
            print(completedProcess)


        # print(action)
        # output, err = call.communicate()
        # if (output):
        #     print('output: ' + str(output))
        # if (err and action['name'] != 'build'):
        #     print('err: ' + str(err))
        #     if action['name'] == 'start':
        #         return action['errMessage']


deploy('frontend')
