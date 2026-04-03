import typer
import csv
from tabulate import tabulate
from sqlmodel import select
from app.database import create_db_and_tables, get_cli_session, drop_all
#from app.models.user import *
from app.models.user import User, UserBase
#from app.models.models import Exercise
from app.utilities.security import encrypt_password

cli = typer.Typer()

@cli.command()
def initialize():
    with get_cli_session() as db: # Get a connection to the database

        drop_all() # delete all tables
        create_db_and_tables() #recreate all tables

        bob = User.model_validate(UserBase(
            username='bob',
            email='bob@mail.com',
            password=encrypt_password("bobpass")
        ))
        pam = User.model_validate(UserBase(
            username='pam',
            email='pam@mail.com',
            password=encrypt_password("bobpass")
        ))
        tommy = User.model_validate(UserBase(
            username='tom',
            email='tomm@mail.com',
            password=encrypt_password("bobpass")
        ))
        
        print(bob, pam, tommy)
        #ex = Exercise(name="Strength", type ="BodyBuild", muscle="Biceps")
        db.add(bob)
        db.add(pam)
        db.add(tommy)
        print("Before commit:", db.exec(select(User)).all())
        #db.add(ex)
        db.commit()
    print("DB INITIALIZED")

if __name__ == "__main__":
    cli()