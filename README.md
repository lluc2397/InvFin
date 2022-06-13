# InvFin
The main purpose of the webapp is to centralise information about investing, in spanish.

# CURRENT PARTS
The webapp is composed (by the moment) of 3 majors parts.

## Q&A
One part is the written content where users can vote, read definitions, share content, ask and answer questions (like SO), improve some definitions or create their own newsletter.
This part is very basic, users can CRUD answers, comments, etc... if they are log in, nothing really fancy.

## Screener
The second part is the screener. For now it's just companies (ETFs and Superinvestors are still in developpements, I have to recreate the database schema, and set up templates, views, etc...) 
In this part, users can look for over 30000 companies around the globe. They can see their financial statements and metrics with nice charts and tables.

## Public Blog
The third part is the "management". Users can create their own newsletter, have a subdomain and create a fan base to send them their newsletters (like substack).
In this part they can see all related to their content, views, times shared, interactions, emails opening rate, etc...

## Roboadvisor
Users will have a investor profile and based on that they can ask to analyse some company and see if it would match their profile and investement approach.

## Portfolio
Users can keep track of their finance and investments and share it with the world, set up goals and reminders.


# SIDE NOTES
## Creation
I used cookiecutter to start the project to see how to structure it "correctly".
The website is deployed on a single core CPU so multithreading is limited. For everything related to sending emails or scraping for information Celery with Redis handle that. Why Redis? Well, Django Cookiecutter came with that so I wanted to give it a try. Before I used RabbitMQ as it is focused on being a message broker I thought that it was more appropriate. Now I'm using Redis to test it and because I can use it to cache.

## TemplateTags
### UTM
A tag to create utm parameters for the urls. source and campaign are at the end as usually medium, content and term are usually changed accross the web.

- {% utm content='', term='', medium='webapp', source='invfin', campaign='website-links' %}


# TODO
- Create recommendation sys for dashboard companies, terms, writters, etc...
- Improve roboadvisor brain
- Add ETFs


# How to start locally

Make sure that you have make installed.

Run the following command to build the images
- make build

Then run this to have the containers running.
- make up

Run the different tests.
- make test

Make sure that the styles is correct.
- make isort_pep