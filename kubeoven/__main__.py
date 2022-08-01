import sys
import click
from kubeoven import commands
import warnings
import logging

sys.tracebacklimit = 0
logging.basicConfig(level=logging.FATAL)
warnings.simplefilter("ignore")

@click.group()
def app():
    pass

def main():
    app.add_command(commands.deploy_command)
    app()

main()