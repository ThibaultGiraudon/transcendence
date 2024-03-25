# Transcendence

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

### Launch the server
Use the following commands to launch the docker-compose file to up the website:
```shell
cd transcendence
docker-compose up --build
```

> [!NOTE]
> *See [this page](https://docs.docker.com/desktop/) to understand how to install Docker.*


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


## Technical details

- **Front End**: HTML <img height=20 src="https://github.com/devicons/devicon/blob/master/icons/html5/html5-original.svg"> / CSS <img height=20 src="https://github.com/devicons/devicon/blob/master/icons/css3/css3-original.svg"> / JavaScript <img height=20 src="https://github.com/devicons/devicon/blob/master/icons/javascript/javascript-original.svg">

- **Back End**: Django <img height=20 src="https://github.com/devicons/devicon/blob/master/icons/django/django-plain.svg">

- **Database**: PostgreSQL <img height=20 src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-original.svg">


## Credits

This project was entirely developed by *Leon Pupier*, *Elias Zanotti* and *Thibault Giraudon* for the final comon core project called **ft_transcendence**.
