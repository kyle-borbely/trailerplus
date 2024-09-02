# TrailersPlus Documentation


*** Documentation for manOS BigSur Version 11.1. The documentation is also 
    suitable for Linux systems.

## Clone the project, create .env files and include a blank certificate

Clone project:
```bash
git clone https://github.com/upqode/trailersplus-backend.git
```

**Create file in the directory** - `../docker/` \
Create a new file - `.env` in the directory -`docker`. Fill in the file 
using the example - `compose.env.example`. 
\
\
**Create file in the directory** - `../trailersplus/trailersplus/` \
In the project configs, we also create - `.env` near `settings.py`. 
In order to populate this file, you need to access the GitLab repository. 
Project - `Trailersplus Backend`.
\
\
As soon as we got access, go to the GitLab project, go to Settings 
(left menu), go to `CI / CD`, then to Variables where the file will 
be -`ENV_FILE`, copy the contents and paste it into our `.env`, 
the settings must be changed for local use.
\
\
**Certificate** \
It is necessary to create a storage location for the certificate, 
in the `trailersplus` directory, create a `certs` directory in it, 
create a `redis` in it, create a file -` aiven_ca.pem`. The path should 
look like this - `... /trailersplus-backend/trailersplus/trailersplus/certs/redis/aiven_ca.pem`

```bash
chmod -R 0600 certs/
```

## Docker-compose

**Up containers** \
Go to the directory - `docker`. In it we run the command:
```bash
docker-compose up --build 
```
If all done correctly, 4 containers should up. The `web` part run separately.

## Virtualenv

**Create and run virtual environment** \
Сreate near the project or where it will be convenient. For example:
```bash
virtualenv venv_trailersplus --python=python3.8
```
Activate virtual environment:
```bash
source venv_trailersplus/bin/activate
```

## Install requirements

**Pipfile**
Need to install `pipenv`:
```bash
pip install pipenv
```
Install `Pipfile`:
```bash
pipenv install
```

Install `git-lfs`:
```bash
brew install git-lfs
git lfs install
git lfs pull
```

## Install static

Required to display styles
```bash
python manage.py collectstatic 
```

## Now you can start the project. 
In order to start the project, the containers must be running, 
if they are running, then we start the project:
```bash
python manage.py runserver
```

## Dump

**From the GitLab repository to CI / CD, you need to take 3 files**:
- PSQL_CLIENT_CERT 
- PSQL_CLIENT_KEY 
- PSQL_SERVER_CA 

These files are needed to dump.

You need to change the rights
```bash
chmod 0600 file
or
chmod -R 0600 your_dir
```

If the ip is added to the server, then using the command you can make a dump.

```bash
pg_dump "user=postgres dbname=factory port=5432 host=104.197.74.105 sslcert=…/PSQL_CLIENT_CERT sslkey=…/PSQL_CLIENT_KEY sslrootcert=…/PSQL_SERVER_CA sslmode=verify-ca" --inserts —file=…/damp_db.sql
```
