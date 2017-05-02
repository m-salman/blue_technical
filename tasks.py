import os
import sys
import socket
import unittest
from invoke import run, task


@task
def start_elastic_search(ctx):
    """Starts an instance of ElasticSearch local in a docker container"""
    run("docker-compose up -d elastic_search")


@task
def start(ctx, docs=False):
    _assert_es_running(ctx)
    from src.app import application
    application.run(host="0.0.0.0", port=8080)


@task
def test(ctx):
    """Runs all tests"""
    _assert_es_running()
    os.environ['ENV'] = 'test'
    all_tests = unittest.TestLoader().discover("test")
    unittest.TextTestRunner().run(all_tests)


def _assert_es_running(ctx):
    if not _in_docker() and not _es_running():
        # _fail("Start ElasticSearch with 'invoke start_elastic_search'")
        start_elastic_search(ctx)


def _es_running():
    return _port_open(9200)


def _port_open(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    return True if result == 0 else False


def _in_docker():
    return os.path.isfile("/.dockerenv")


def _fail(msg):
    sys.stderr.write(msg)
    sys.exit(1)


if sys.version_info.major < 3:
    _fail("You need Python 3 to run this project")
