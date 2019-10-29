import smtplib, ssl 
import pandas as pd
import argparse
import json
import os 

def change_recursive(my_dict):
    for key in my_dict:
        if isinstance(my_dict[key], dict):
            change_recursive(my_dict[key])
        else: 
            if os.path.exists(my_dict[key]):
                with open(my_dict[key], 'r') as file:
                    my_dict[key]=file.read()        

def return_text(key, my_dict, row, keys, level=0):
    if not isinstance(my_dict[key], dict):
        return str(my_dict[key])
    else:
        return return_text(row[keys[level]], my_dict[key], row, keys, level+1)

if __name__ == '__main__': 
    
    # parser for command-line arguments
    parser=argparse.ArgumentParser("Script to efficiencly send emails to guests.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-j', '--json', dest='json', type=str, default = 'json/website.json',  
                        help='JSON file containing which file to use for each language. Must contain the following keys: "message", "salutation", "subject"')
    parser.add_argument('-s', '--sender', dest='sender', type=str, default = 'chiaraegiuseppe.matrimonio@gmail.com',  help='Sender email')
    parser.add_argument('-g', '--guests', dest='guests', type=str, default = 'csv/invitati.csv',  help='CSV file with guests information')
    parser.add_argument('-d', '--dryrun', dest='dryrun', action='store_true', help='Make a dry run, print the messages but do not seend')
    parser.add_argument('--column-email', dest='columnemail', type=str, default = 'email',  help='Name of the email column in the CSV')
    parser.add_argument('--column-language', dest='columnlanguage', type=str, default = 'Lingua',  help='Name of the language column in the CSV')
    parser.add_argument('--column-SP', dest='columnSP', type=str, default = 'S/P',  help='Name of the S/P column in the CSV. Values in the  column must be in [S,P]')
    parser.add_argument('--column-MF', dest='columnMF', type=str, default = 'M/F',  help='Name of the M/F column in the CSV. Values in the colums must be in [M,F]')
    parser.add_argument('--column-names', dest='columnnames', type=str, default = 'Inizio',  help='Name of the column in the CSV with the names of the guests')
    args=parser.parse_args()

    # load json file with messages
    with open(args.json, 'r') as j:
        messages = json.load(j)

    # if the CSV points to files, replace with file content                        
    change_recursive(messages)
    # order of keys in json
    keys = [args.columnlanguage, args.columnSP, args.columnMF]

    # read guest list
    df = pd.read_csv(args.guests, sep=',')

    # SSL  
    port = 465  # port for SSL 
    password = input('Type your password and press enter: ')
    # SSL context
    context = ssl.create_default_context()

    # extra check: ask ifsure to send
    if not args.dryrun:
        send = input('Do you really want to send? Type [yes/no] and press enter: ')
        if send=='yes':
            print('You are really sending the emails!')

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login('chiaraegiuseppe.matrimonio@gmail.com', password)
        for index, row in df.iterrows():
            # check we are reading a row with a real email
            if type(row[args.columnemail]) is str and '@' in row[args.columnemail]:
                message = 'Subject: ' + return_text('subject', messages, row, keys) + '\n\n'
                message += return_text('salutation', messages, row, keys) 
                message += ' ' + row[args.columnnames] + ',\n\n'
                message += return_text('message', messages, row, keys)
                if  args.dryrun:
                    print('To:', row[args.columnnames], row[args.columnemail])
                    print(message)
                    print('\n')
                else:
                    # THIS IS SENDING THE EMAIL!
                    if send=='yes':
                        server.sendmail(args.sender, row[args.columnemail], message)
                        print('Sent to',row[args.columnemail])

