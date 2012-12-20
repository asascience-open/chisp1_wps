from __future__ import with_statement
from fabric.api import run, local, cd, settings, lcd, abort, env
from fabric.contrib.console import confirm

env.hosts = []

def prepare_deploy():
    with settings(warn_only=True):
        result = local('git commit -a')
        result = local('git push origin master')

def test():
    with settings(warn_only=True):
        result = local('python manage.py test')
    if result.failed and not confirm("Tests Failed...Continue?"):
        abort("Aborting...")

def deploy():
    clean()
    test()
    prepare_deploy()


def clean():
    local('rm -rf *.pyc')
    local('rm -rf *.py~')
    local('rm -rf *.xml~')
    local('rm -rf *.csv~')


