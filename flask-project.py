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
@click.option("--count")
def populate(count):

    console.log('[yellow]Prepering to populate database[/]')
    connection = sqlite3.connect(os.path.join(os.path.dirname(__file__) , 'instance' , 'main.db'))

    cursor = connection.cursor()

    faker = Faker()

    for i in range(int(count)):
        cursor.execute("INSERT INTO Category VALUES (NULL , ?)" , (faker.company(),))
    
    connection.commit()
    connection.close()

    console.log('[green]Successfully populated database[/]')
    

cli()