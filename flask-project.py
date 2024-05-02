from rich.console import Console
from faker import Faker

import sqlite3 , os , click

console = Console()
VERSION = "1.0.0"

@click.group
def cli():
    """
    Abstract FlasK Project CLI
    """
    pass

@cli.command()
def run():
    if __name__ == "__main__":
        from app import create
        app = create()
        app.run()

@cli.command()
def populate():

    connection = sqlite3.connect(os.path.join(os.path.dirname(__file__) , 'instance' , 'main.db'))
    cursor = connection.cursor()

    values = [('Frontend Development',), ('Backend Development',), 
        ('Software Development',), ('CI/CD',) , 
        ('Database/Data Science',),('Programing Languages',) ,
        ('UML',) , ('UI/UX',)
    ]

    cursor.executemany("INSERT INTO Category VALUES(NULL , ?)" , values)
    connection.commit()
    connection.close()

    Console.print('successfully populated category table')

cli()