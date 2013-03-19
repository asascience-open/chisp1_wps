from __future__ import with_statement
from fabric.api import run, local, cd, settings, lcd, abort, prefix, env
from fabric.contrib.console import confirm

env.hosts = ["chisp@192.168.250.103"] # local asa address

def prepare_deploy():
    with settings(warn_only=True):
        result = local('git commit -a')
        result = local('git pull origin master')
        if result.failed and not confirm("Failed Pulling New Updates from Git Repository...Continue?"):
                abort("Aborting...")
        result = local('git push origin master')
        if result.failed and not confirm("Failed Pusing Changes to Git Repository...Continue?"):
                abort("Aborting...")

def test():
    modules = ['wps',
               'nlcs',
              ]
    for module in modules:
        with settings(warn_only=True):
            result = local('python manage.py test %s' % module)
        if result.failed and not confirm("Tests Failed...Continue?"):
            abort("Aborting...")


def deploy():
    clean()
    test()
    prepare_deploy()
    #with run('source venvs/chisp/bin/activate'):
    env.activate = 'source /home/chisp/envs/standard/bin/activate'
    with cd('chisp1_wps/'):
        with settings(warn_only=True):
            run("kill -9 $(ps aux | grep run_gunicorn | awk '{print $2}')")
        with settings(warn_only=True):
            run("rm *pyc")
        run('git pull -f')
        with prefix(env.activate):
            run('python manage.py run_gunicorn -w 1 -k sync -b 0.0.0.0:8080')
    #print 'Please run the following command on the server to start the service:\n\npython manage.py run_gunicorn -w 3 -k eventlet -b 0.0.0.0:8080 &'

def clean():
    local('rm -rf */*.pyc')
    local('rm -rf */*.py~')
    local('rm -rf */*.xml~')
    local('rm -rf */*.csv~')

