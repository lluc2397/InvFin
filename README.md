# InvFin
The main purpose of the webapp is to centralise information about investing, in spanish.

# CURRENT PARTS
The webapp is composed (by the moment) of 3 majors parts.

One part is the written content where users can vote, read definitions, share content, ask and answer questions (like SO), improve some definitions or create their own newsletter.
This part is very basic, users can CRUD answers, comments, etc... if they are log in, nothing really fancy.

The second part is the screener. For now it's just companies (ETFs and Superinvestors are still in developpements, I have to recreate the database schema, and set up templates, views, etc...) 
In this part, users can look for over 30000 companies around the globe. They can see their financial statements and metrics with nice charts and tables.

The third part is the "management". Users can create their own newsletter, have a subdomain and create a fan base to send them their newsletters (like substack).
In this part they can see all related to their content, views, times shared, interactions, emails opening rate, etc...

# PARTS COMMING
I'm still finishing the portfolio part. Where users can keep track of their finance and investments and share it with the world, set up goals and reminders.

The other part is a roboadvisor. Users will have a investor profile and based on that they can ask to analyse some company and see if it would match their profile and investement approach.

# SIDE NOTES
I used cookiecutter to start the project to see how to structure it "correctly".
The website is deployed on a single core CPU so multithreading is limited. For everything related to sending emails or scraping for information Celery with Redis handle that. Why Redis? Well, Django Cookiecutter came with that so I wanted to give it a try. Before I used RabbitMQ as it is focused on being a message broker I thought that it was more appropriate. Now I'm using Redis to test it and because I can use it to cache.

# TODO
- Add better ckeditor config
- Finish templates and views of roboadvisor
- Update README
- Improve roboadvisor brain
- Add ETFs
- Add superinvestors