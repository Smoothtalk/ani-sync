import os
import psycopg2
from django.core.management.base import BaseCommand
import environ

env = environ.Env()
environ.Env.read_env()

class Command(BaseCommand):
    help = 'Create a PostgreSQL database using settings from .env file'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, help='Name of the database to create', default=None)

    def handle(self, *args, **options):

        # Retrieve database connection info from environment variables
        db_name = env("DB_NAME")
        db_user = env("DB_USER")
        db_password = env("DB_PASSWORD")
        db_host = env("DB_HOST")
        db_port = env("DB_PORT")

        if not all([db_name, db_user, db_password, db_host, db_port]):
            self.stderr.write("Database connection info is missing in the .env file.")
            return

        # Connect to PostgreSQL
        conn = psycopg2.connect(dbname='postgres', user=db_user, password=db_password, host=db_host, port=db_port)
        conn.autocommit = True  # Required to create a database
        cursor = conn.cursor()

        try:
            # Create database
            cursor.execute(f"CREATE DATABASE {db_name};")
            self.stdout.write(f"Database '{db_name}' created successfully.")
        except psycopg2.errors.DuplicateDatabase:
            self.stdout.write(f"Database '{db_name}' already exists.")
        except Exception as e:
            self.stderr.write(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()
