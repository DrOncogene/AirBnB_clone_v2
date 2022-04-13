#!/usr/bin/python3
from fabric.api import local, run, env
from fabric.decorators import task


env.hosts, env.user = ['44.192.32.161', '34.139.191.175'], 'ubuntu'


@task
def do_clean(number=0):
    '''Cleans up unncessary archives.
    Args:
        number(int): number of archives to keep
    Return: nothing
    '''
    archives = local('ls -t versions/', capture=True).splitlines()
    output = run("ls -t /data/web_static/releases | tr -s '\t\r\n' ' '")
    releases = output.split(' ')
    number = 1 if int(number) in [0, 1] else int(number)

    for i in range(number, len(archives)):
        local(f"rm versions/{archives[i]}")
    for i in range(number, len(releases)):
        run(f"rm -rf /data/web_static/releases/{releases[i]}")
