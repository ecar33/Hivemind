import click
from hivemind.core.extensions import db

def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """For creating and destroying the db"""
        if drop:
            db.drop_all()
            click.echo('Database dropped.')
        db.create_all()
        click.echo('Initialized database.')