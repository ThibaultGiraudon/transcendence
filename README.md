<div align="center">
  <a href="https://github.com/LeonPupier/Mensible">
    <img src="django/static/main/img/favicon.ico" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">Transcendence</h3>
  
  Final common core project of 42 school
  
  [![HitCount](https://img.shields.io/endpoint?url=https%3A%2F%2Fhits.dwyl.com%2FThib1708%2Ftranscendence.json%3Fcolor%3Dgreen)](https://github.com/Thib1708/transcendence/)
  ![](https://sloc.xyz/github/Thib1708/transcendence)
  [![Last commit](https://img.shields.io/github/last-commit/Thib1708/transcendence)](https://github.com/Thib1708/transcendence/)
</div>

> [!WARNING]
> This project is still under development.

## Summary

- [Description](#description)
- [Installation](#installation)
- [Pong game](#pong-game)
	- [Practice modes](#practice-modes)
 	- [Ranked modes](#ranked-modes)
- [Chat](#chat)
- [Ranking](#ranking)
- [Friends](#friends)
- [Profile](#profile)
- [Notifications](#notifications)
- [Email support](#email-support)
- [How to create the env file](#how-to-create-the-env-file)
- [Technical details](#technical-details)
- [Credits](#credits)


## Description

This project is a website that lets you play the famous game of [Pong](https://en.wikipedia.org/wiki/Pong), with several game modes available.
To do this, you'll need to create an account using your own credentials or by linking your **42 account** to the website.
All data is persistent and securely stored. It is not possible for developers to recover a user's password in clear text.


## Installation

### Clone the repository
Use the following command to clone the repository to your local machine:
```shell
git clone https://github.com/tgiraudo/transcendence.git
```

### Create the env file
See [How to create the env file](#how-to-create-the-env-file) to create this important file and to be abble to continue the installation.

### Launch the server
Use the following commands to launch the docker-compose file to up the website:
```shell
cd transcendence
docker-compose up --build
```

> [!NOTE]
> *See [this page](https://docs.docker.com/desktop/) to understand how to install Docker.*

### Open the website
Open your favorite internet browser and go to http://localhost:8000 to visit the website in the insecure way. To have an HTTPS connexion, go to https://localhost:8443.


## Pong game

### Practice modes

You can train your skills in a practice mode with 3 games among:

- **Local** game with a friend on the same computer.
- **1 vs AI** where you are against an artificial intelligence.
- **Wall game** where you have to throw as many balls as possible against the wall.

### Ranked modes

If you're looking for a competitive edge, there are 3 game modes to choose from:

- **1 vs 1** against an opponent from all over the world.
- **4-way deathmatch** where all players play at the same time on the same grid, with a paddle on each side.
- **Tournament** mode, where 2 groups of 2 play simultaneously on their own grid, followed by a final between the 2 winners.


## Chat

In addition to the game, you'll find an advanced chat feature.
</br>
This allows you to have **private conversations** with another user. You can also take part in **group conversations**, with no user limit. If you feel like it, feel free to **create your own chat group** and invite your friends!


## Ranking

By playing competitive game modes, you **earn points** that help you climb the world rankings. A tab is dedicated to this ranking, where you can see other players' statistics and more by visiting their profiles.


## Friends

You can send a **friend request** to any user of your choice. If they accept, you'll be officially linked. Friends are private and visible only to those concerned. This allows you to see their **live status** to see if they're online, offline or in a game. You can find them more easily in a dedicated tab.


## Profile

Each user has a profile. Public information includes your **profile photo** (*a photo is assigned to you by default when your account is created*), your **nickname**, your **statistics** and your **game history**. On your own account, you'll be able to access more options, such as customizing your profile. This includes changing your profile photo and display name. Not forgetting your email address and password (*not accessible to users logged in with 42*).


## Notifications

An advanced notification system is available on the website to keep you up to date. A **live animation** will alert you to incoming news, along with a **pending message counter**. Once on the notifications page, you'll be able to see **unread messages**, **new ones received**... All notifications are **clickable** and will redirect you to the desired location, and some contain **action buttons** to facilitate your reaction.


## Email support

The project includes an **email support** to inform registered users of actions taken on their accounts and securely track their modifications. This can be disabled if required on the user's profile page.


## How to create the env file

To set up the server and website, you'll need a file containing environment variables. This file should be named `.env` and located at the root of the main folder. Here's an implementation model of this famous file:

```python
# Django
HOST=# Put your local IP here
SECRET_KEY= # Django secret key
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 ${HOST} [::1]
OFFICIAL_EMAILS=lpupier@student.42lyon.fr,tgiraudo@student.42lyon.fr,ezanotti@student.42lyon.fr

# DataBase identification
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=postgres
DATABASE_USER= # Database username
DATABASE_PASSWORD= # Database password
DATABASE_HOST=postgres
DATABASE_PORT=5432

# API identification
CLIENT_ID= # 42 client API ID
CLIENT_SECRET= # 42 client secret
OTHER_CLIENT_SECRET= # 42 next client secret - optionnal

# Email gestion
EMAIL_HOST_USER= # Email
EMAIL_HOST_PASSWORD= # API password
```

Modify the informations with your own credentials and then launch the `docker-compose` of your choice.


## Technical details

- **Front End**: HTML <img height=20 src="https://github.com/devicons/devicon/blob/master/icons/html5/html5-original.svg"> / CSS <img height=20 src="https://github.com/devicons/devicon/blob/master/icons/css3/css3-original.svg"> / JavaScript <img height=20 src="https://github.com/devicons/devicon/blob/master/icons/javascript/javascript-original.svg">

- **Back End**: Python <img height=20 src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg"> / Django <img height=20 src="https://github.com/devicons/devicon/blob/master/icons/django/django-plain.svg">

- **Database**: PostgreSQL <img height=20 src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-original.svg">


The entire website has been developed in compliance with the single page application ([SPA](https://en.wikipedia.org/wiki/Single-page_application)) for increased user comfort and speed of use.


## Credits

This project was entirely developed by *Leon Pupier*, *Elias Zanotti* and *Thibault Giraudon* for the final comon core project of 42 called **ft_transcendence**.
