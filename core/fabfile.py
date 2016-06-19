from fabric.api import lcd, local, settings, task, puts, hide
from fabric.colors import green
import os
import sys

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


def info(text):
    puts(green(text))


@task
def polish():
    found_errors = False
    with lcd(ROOT_DIR):
        with settings(hide('running'), warn_only=True):
            # Remove compiled python classes
            info('Removing compiled python classes...')
            local('pyclean .')
            local('find app '
                  '-name "*.py[co]" -print0 | xargs -0 rm -f')

            # Fix directory permissions
            info('Fixing directory permissions...')
            result = local(
                '! find app '
                '-path .git -prune -o '
                '-name .webassets-cache -prune -o '
                '-name gen -prune -o '
                '-type d -not -perm 0775 -print0 | '
                'tee /dev/stderr | '
                'xargs -0 chmod 0775 >/dev/null 2>&1'
            )
            found_errors = found_errors or result.return_code != 0

            # Fix file permissions
            info('Fixing file permissions...')
            result = local(
                '! find app '
                '-path .git -prune -o '
                '-name .webassets-cache -prune -o '
                '-name gen -prune -o '
                '-name "*.py[co]" -o '
                '-type f -not -perm 0664 -print0 | '
                'tee /dev/stderr | '
                'xargs -0 chmod 0664 >/dev/null 2>&1'
            )
            found_errors = found_errors or result.return_code != 0

            # Run coding standards check
            info('Running coding standards check...')
            result = local('pep8 --exclude="settings.py, */__init__.py,\
                            *_template.py, *dump*.py" '
                           'app ./fabfile.py')
            found_errors = found_errors or result.return_code != 0

            # Run static code analyzer
            info('Running static code analyzer...')
            result = local('pyflakes app ./fabfile.py ')
            found_errors = found_errors or result.return_code != 0

            # Find merge conflict leftovers
            info('Finding merge conflict leftovers...')
            result = local(
                '! find app '
                '-path .git -prune -o '
                '-name .webassets-cache -prune -o '
                '-name gen -prune -o '
                '-name "*.png" -o '
                '-name "*.py[co]" -o '
                '-type d -o '
                '-print0 | '
                'xargs -0 grep -Pn "^(<|=|>){7}(?![<=>])"'
            )
            found_errors = found_errors or result.return_code != 0

            # Check for debug print statements
            info('Checking for debug print statements...')
            result = local(
                '! find app -type f -name "*.py" -print0 | '
                'xargs -0 grep -Pn \'(?<![Bb]lue|>>> )print\' | '
                'grep -v NOCHECK'
            )
            found_errors = found_errors or result.return_code != 0

            # Check for no servername compatibility
            info('Checking for no-servername compatibility...')
            result = local(
                '! find app -name "settings.py" -o '
                ' -type f -name "*.py" -print0 | '
                'xargs -0 grep -Pn \'SERVER_NAME|ENABLE_HTTPS|SSO_DOMAIN|'
                '(SOFTWARE(_WEBSITE)?|EPICENTER|FABRIC|PVR|PRACTONAV)_HOST\''
            )
            found_errors = found_errors or result.return_code != 0

            info('Checking migration branches...')
            result = local('!  PYTHONPATH=./core \
                python manage.py db branches| grep branchpoint')
            found_errors = found_errors or result.return_code != 0

            found_errors = found_errors or result.return_code != 0
    if found_errors:
        sys.exit(1)


@task
def grep(term, flags=''):
    with lcd(ROOT_DIR), settings(hide('running')):
        local('find api scripts tests '
              '-name "*~" -o '
              '-name "*.py[co]" -o '
              '-name "*.dot" -o '
              '-name "*.min.*" -o '
              '-name "gen" -prune -o '
              '-name ".webassets-cache" -prune -o '
              '-type d -o '
              '-print0 | '
              'xargs -0 grep -n --color=force ' + flags + ' "' + term + '"; '
              ' echo -n')
