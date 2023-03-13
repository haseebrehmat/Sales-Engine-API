<p align="center">
    <img width="300" src="https://user-images.githubusercontent.com/85288256/220799197-734504e0-81b7-4b0c-bd49-2225161e0045.png" alt="https://octagonapp.io/">
    </p>

<h1 align="center">
Octagon - We do the hard work so you don't have to.
  </h1>

## Tracking Project Status - Octagon (BackEnd)

We use the [SCRUM](https://www.scrum.org/resources/what-is-scrum) framework for project management.
All active and closed issues can be viewed on the [Jira](https://www.atlassian.com/software/jira). Some useful links for reference:

| Resource                       | Link                                                                                                              |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| Jira - Project Board           | [Octagon - Jira Software Project](https://devsinc.atlassian.net/jira/software/projects/OC/boards/22)              |
| JSM - Help Desk                | [Octagon - Customer Support](https://devsinc.atlassian.net/servicedesk/customer/portal/8)                         |
| Atlas - Teamwork Directory     | [Octagon - Atlas - Release Notes](https://team.atlassian.com/project/DEVSI1-4)                                    |
| Compass - A developer Exp      | [Octagon - Compass](https://devsinc.atlassian.net/compass/component/b4c343cc-e008-4417-963d-a071155335cb)         |
| Confluence Documentation       | [Octagon - Confluence](https://devsinc.atlassian.net/wiki/spaces/OC/overview)                                     |
| Postman-API docs & Automation  | [Octagon - PostmanTeam](https://octagonapp.postman.co/)                                                           |
| Test Plan - Automation         | [Octagon - SQA Strategy](https://devsinc.atlassian.net/wiki/spaces/OC/pages/699367438/Octagon+-+Testing+Strategy) |
| Development - Coding Standards | [Octagon - Coding Standards](https://devsinc.atlassian.net/wiki/spaces/OC/pages/687276056/Standards)              |

## Getting Started

### Prerequisites:

Be sure, you have installed following dependenices installed on your development machine:

- python >= 3.7
- git
- pip
- postgresql

### Installation:

To install Octagon on your local machine, follow these steps:

#### 1. Clone the Octagon BE repository:

    git clone https://github.com/Devsinc-Org/Octagon-BE

#### 2. Familiarize yourself with the following files and directories:

- `requirements.txt`: contains all the dependencies required to run the Django project
- `.env.example`: contains all environment variables required to run the Django project

- `settings/` directory: contains all settings required to run the project on local, development, production, and staging environments

- `base.py`: contains the main settings for Django
- `local.py`: contains the settings for the local database
- `development.py`: contains the settings for the development database
- `production.py`: contains the settings for the production database
- `staging.py`: contains the settings for the staging database

### Usage

To use Octagon, follow these steps:

#### 1. Create and activate virtual environment

##### For linux or macOS

    python3 -m venv venv
    source venv/bin/activate

##### For Windows

    python -m venv venv
    venv/Scripts/activate

#### 2. Install dependencies for django using pip:

    pip install -r requirements.txt

#### 3. Configuration

Rename the `.env.example` file to .env and update the values with your own configuration.

#### 4. Set the environment variable in .env:

    ENVIRONMENT=development

- e.g: ('local', 'development', 'production', 'stagging')

#### 5. Run migrations

    python manage.py makemigrations

Above command will create database migrations

#### 6. Migrate DB Migrations

    python manage.py migrate

Above command will update db schema according to migrations.

#### 7. Running the application

    python manage.py runserver

The application will be available at http://127.0.0.1:8000/

#### Note:

- We need to use the PostgreSQL database because the project has dependencies on it.
