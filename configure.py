import shutil
import os.path
import secrets

env_file = 'project/.env'
env_example_file = 'project/.env_example'
env_file_exists = os.path.isfile(env_file)
if not env_file_exists:
    base_created = input("Did you create database in postgres (y/n)?\n")
    if base_created.lower() in ['yes', 'y']:
        db_name = str(input("Write db name: \n"))
        db_user = input("Write db username (default: postgres): \n").strip() or "postgres"
        db_pass = input("Write db password (default: postgres): \n").strip() or "postgres"
        db_host = input("Write db host (default: localhost): \n").strip() or "localhost"
        db_port = input("Write db port (default: 5432): \n").strip() or "5432"
        debug_str = input("Enable debug (y/n): \n").strip() or "True"
        if debug_str.lower() in ['yes', 'y']:
            debug_str = 'True'
        else:
            debug_str = ''
        secret_key = secrets.token_urlsafe(50)
        with open(env_file, "w") as text_file:
            text_file.write(f"DEBUG={debug_str}\n")
            text_file.write(f"DJANGO_SECRET_KEY={secret_key}\n")
            text_file.write(f"DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1\n\n")
            text_file.write(f"SQL_ENGINE=django.db.backends.postgresql_psycopg2\n")
            text_file.write(f"SQL_DATABASE={db_name}\n")
            text_file.write(f"SQL_USER={db_user}\n")
            text_file.write(f"SQL_PASSWORD={db_pass}\n")
            text_file.write(f"SQL_HOST={db_host}\n")
            text_file.write(f"SQL_PORT={db_port}\n")
    else:
        print("Please create database first")
else:
    print("You already have `.env` file in `project` folder")
