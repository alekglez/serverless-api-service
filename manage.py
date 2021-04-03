# -*- coding: utf-8 -*-

import os
import unittest

import click
import coverage
import uvicorn

from main import create_app


@click.group()
def cli_main():
    pass


@cli_main.command('run')
def run():
    app = create_app(os.environ.get("PROJECT_NAME", "Serverless Generic API"), debug=False)
    uvicorn.run(app, host="0.0.0.0", port=8000)


@click.group()
def cli_tests():
    pass


@cli_tests.command('test')
def test():
    """ Runs the test without generating a coverage report """

    tests = unittest.TestLoader().discover("project/", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return result.wasSuccessful()


@cli_tests.command('coverage')
def cov():
    """ Runs the unit tests and generates a coverage report on success """

    coverage_ = coverage.coverage(branch=True, include=["project/*"], omit=["project/api/tests/*"])
    coverage_.start()

    tests = unittest.TestLoader().discover("project/", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        coverage_.stop()
        coverage_.save()

        try:
            print("Coverage Summary:")
            coverage_.report()
            coverage_.html_report()
            coverage_.erase()

        except coverage.CoverageException as error:
            print(error)

    return result.wasSuccessful()


cli = click.CommandCollection(sources=[cli_main, cli_tests])
if __name__ == "__main__":
    cli()
