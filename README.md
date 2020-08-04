# Bank-Details-API
This repository is based on CRUD (Create, read, update, delete) operation on the bank details using Django Rest Framework ( RESTFUL API).

This application will help you to get through the Django rest framework and Heroku.

Heroku hosting files created in this repository is for windows but you can do it for linux and mac as well by following the simple steps from <a href="https://devcenter.heroku.com/articles/getting-started-with-python">here</a>

To run this, you need to have python3.6 and pip installed, then you're good to go.

Install require dependency -> pip install -r requirements.txt


then simply run   -> python3 manage.py collectstatic
                  -> python3 manage.py runserver 

if you want to host it on heroku --> I'm supposing youo've a free account on heroku.

$ heroku login

$ heroku create <REPO NAME (optional)>

if you don't specify REPO NAME it will create one automatically.

change the remote heroku url in .git\config file as per your url. Then,

$ git add .
$ git commit -m "Your Commit message here"
$ git push heroku master

Once successfully pushed to Heroku,

$ heroku open
$ heroku logs --tail  (optional, if you want to check logs.)

You can do more with heroku and that you'll get from <a href="https://devcenter.heroku.com/articles/getting-started-with-python#define-a-procfile">here</a>.
