import os
import shutil
from subprocess import Popen

# Get the root project directory
PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def init_git():
    """
    Initialises git on the new project folder
    """
    GIT_COMMANDS = [
        ["git", "init"],
        ["git", "add", "."],
        ["git", "commit", "-a", "-m", "Initial Commit."]
    ]

    for command in GIT_COMMANDS:
        git = Popen(command, cwd=PROJECT_DIRECTORY)
        git.wait()


def remove_task_app():
    shutil.rmtree(os.path.join(
        PROJECT_DIRECTORY,
        'project/apps/taskapp'
    ))
    os.remove(os.path.join(
        PROJECT_DIRECTORY,
        'project/apps/common/tasks.py'
    ))


def remove_rest_files():
    for item in ['common/exceptions.py', 'users/jwt.py', 'users/serializers.py']:
        file_location = os.path.join(
            PROJECT_DIRECTORY,
            'project/apps',
            item,
        )
        os.remove(file_location)
    os.remove(os.path.join(
        PROJECT_DIRECTORY,
        'config/api_docs.py'
    ))
    shutil.rmtree(os.path.join(
        PROJECT_DIRECTORY,
        'project/templates/rest_framework'
    ))


def remove_allauth_files():
    shutil.rmtree(os.path.join(
        PROJECT_DIRECTORY,
        'project/templates/account'
    ))


if '{{ cookiecutter.use_celery }}'.lower() == 'n':
    remove_task_app()

if '{{ cookiecutter.use_rest }}'.lower() == 'n':
    remove_rest_files()

if '{{ cookiecutter.use_allauth }}'.lower() == 'n':
    remove_allauth_files()

init_git()
