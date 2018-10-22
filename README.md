#ODKewa

ODKewa is an application that allows us to generate a web app with a data-collection based on an excel spreadsheet (XLSForm) that complies with Open Data Kit (ODK) specifications.

#How to use.

To start clone this repository.

You'll also need an xls file that complies with XLSForm specifications.
Place that file in a git repository your server will have access to and commit the file.

Get the repository url by running:
"git config --get remote.origin.url"
Get the commit hash:
First use 
"git log"
to get a list of commits
then take one of the 6 character commits and use 
"git rev-parse [commit]"
to get the full 40 character hash

prepare a PostgreSQL database with 3 tables "xmeta" "xdata" and "xdatamedia"
you will be using that to collect user inputs from the web app
'odkewa.sql' has the scripts to help create the tables

go to 'populate_xmeta.py' and configure the settings for your database on lines 14, 31, 46, 63, and 78
now you can deploy your form by calling
"python deploy.py [git url] [commit hash] [path to the xls file in your repository]"
deploy.py will print a url to output 
something like: "form/[hash]/[hash]"
copy that and hold on to it

now you can start up the server 
(configure the settings for your machine on lines 21 (database) and 143 (server))

"python odkewa.py"

go to your url (flask should tell you it "Running on:  [your URL]")
and add on the path you got from deploy.py "form/[hash]/[hash]"
your form will display on the site.
you can now fill it out and it will save your input in the database.


#Restrictions 

* field names must comply with the following regular expression:  [a-zA-Z_][a-zA-Z0-9_]*
