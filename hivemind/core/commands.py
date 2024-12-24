import click
from hivemind.core.extensions import db
from hivemind.models import ChatMessage, Chatroom, User
from hivemind.lorem import get_random_body

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

    @app.cli.command()
    @click.option('--num', required=True, type=int, help='Number of messages to add.')
    @click.option('--id', required=True, prompt=True, type=int, help='Chatroom to add messages to')
    def forge(num, id):
        """ For adding messages to the db """
        if num <= 0:
            click.echo('The number of messages must be greater than 0.')
            return
        chatroom_id = db.session.execute(db.select(Chatroom).where(Chatroom.id == id)).scalars().first().id
        if chatroom_id:
            try:
                for _ in range(int(num)):
                    cm = ChatMessage(user_id = 1, chatroom_id=chatroom_id, content=get_random_body())
                    db.session.add(cm)
                
                db.session.commit()
                click.echo(f"{num} messages successfully added to Chatroom {chatroom_id}")

            except Exception as e:
                db.session.rollback()
                click.echo(f'Something went wrong {e}')
        else:
            click.echo("Chatroom doesn't exist")
    
    @app.cli.command()
    @click.option('--id', required=True, type=int, help='Chatroom ID')
    def create_chatroom(id):
        """ For adding messages to the db """
        if id <= 0:
            click.echo("Chatroom ID can't be 0")
            return
        chatroom_id = db.session.execute(db.select(Chatroom).where(Chatroom.id == 1)).scalars().first()
        if not chatroom_id:
            try:
                chatroom = Chatroom(id=id)
                db.session.add(chatroom)
                db.session.commit()
                click.echo(f"Chatroom {id} created.")

            except Exception as e:
                db.session.rollback()
                click.echo(f'Something went wrong {e}')
        else:
            click.echo("Chatroom {id} already exists!")
    
    @app.cli.command()
    @click.option('--user', is_flag=True, type=int, help='User table')
    @click.option('--chatroom', is_flag=True, type=int, help='User table')
    @click.option('--chat-message', is_flag=True, type=int, help='User table')
    def reset_table(user, chatroom, chat_message):
        """ For dropping a specified table """
        if user:
            User.__table__.drop(db.engine)
            User.__table__.create(db.engine)
            click.echo('User table reset.')
        if chatroom:
            Chatroom.__table__.drop(db.engine)
            Chatroom.__table__.create(db.engine)
            click.echo('Chatroom table reset.')
        if chat_message:
            ChatMessage.__table__.drop(db.engine)
            ChatMessage.__table__.create(db.engine)
            click.echo('ChatMessage table reset.')
        else:
            click.echo('Please specify a table and try again.')
