"""
Reports about github changes to telegram bot
"""

from message import send_message


def report(app_id, event, data, config):
    """ Collects data from json and sends message to bot """

    message = "New #{} activity:\n".format(app_id)

    if event == "push":
        message += gen_push_report(data)

    send_message(message, config.get('chats'))
    return


def gen_push_report(data):
    """ Generates push report using data """

    commits = data.get('commits')
    branch = data.get('ref').split('/')[-1]

    message = '{} pushed {} {} to branch *{}*:\n'.format(
        get_userlink(data),
        len(commits),
        'commit' if (len(commits) == 1) else 'commits',
        branch
    )
    for commit in commits:
        message += '    `* {}`\n'.format(commit.get('message'))

    return message


def get_userlink(data):
    """ Creates markdown-styled userlink from data """
    username = data.get('sender').get('login')
    userurl = data.get('sender').get('html_url')
    return "[{}]({})".format(username, userurl)
