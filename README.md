# Emails to many people

![Emails](images/emails.png)

While organising my wedding, 
I’ve often needed to send an email to all the guests, 
e.g. to share with them the location of the wedding website, 
or the link to the pictures stored on Google Photos. 

I wanted to communicate the same information to everybody, but 
part of the guests were English-speaking and part Italian-speaking. 
Furthermore, in Italian you need to use different adjectives, 
pronouns and verbs for singular and plural, masculine and feminine. 

To avoid embarrassing mistakes, I’ve decided to seek the help of a simple python script. 

## Organise the information

I already had all my guest and their emails listed in a spreadsheet, 
to which I added the columns “Language”, “M/F”, “Number of guests”. 
I then saved the spreadsheet as a csv file for an easier handling in python. 
An example of the resulting file is  in [csv/invitati.csv](csv/invitati.csv)

## Modules to import

### Email-related 
* The [ssl module](https://docs.python.org/3/library/ssl.html) is used for the Secure Sockets Layer, to establish 
an encrypted connection.
* For the SMTP protocol client, I used the [smtplib module](https://docs.python.org/3/library/smtplib.html). 

### Other modules
* As in most of my scripts, I use [argparse](https://docs.python.org/3/library/argparse.html) for command-line options. 
* [json](https://docs.python.org/2/library/json.html) is used to read the JSON file containing the information on which 
text we want to use for each type of guest. 
* [pandas](https://pandas.pydata.org/) is used to read the csv file into a DataFrame. 


## How to run the script 

The text of the message for the different options has to be stored in a JSON file, like [this one](json/website.json). 
The final leaf can be either the text itself or the name of a text file containing it. 

To run the script:
```
python emails.py --json json/website.json --guests csv/invitati.csv 
```

Running:
```
python emails.py --help 
```
will show all the arguments avaiable and their meaning




