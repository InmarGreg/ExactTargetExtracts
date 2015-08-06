import csv
import datetime
import json
import os
import urllib
import urllib.request
import zipfile

def ProcessCSV(name, log):
    processed = False

    # process member unsubscribes
    if name.lower().find('unsubs.csv') != -1:
        api_url = 'https://qacag.api.inmar.com/v1/member/optins/'

        input = open(name)
        reader = csv.reader(input)
        header = True

        for row in reader:

            if header != True:
                headers = {'Content-type':'application/json','X-Inmar-REST-API-Key':'d98e72d4-f30c-4eac-9205-18ec125b5ab4'}
                data = {'member':{'identity':{'user_id':row[3]},'optins':[{'optin_id':1040,'optin_value':0}]}}

                try:
                    request = urllib.request.Request(api_url, json.dumps(data).encode('utf8'), headers, method='PUT')
                    response = urllib.request.urlopen(request)
                except Exception as e:
                    log.write(str(e) + ',' + row[3] + '\n')
            else:
                header = False

        processed = True

    # process bounces (delete member)
    elif name.lower().find('bounces.csv') != -1:
        #api_url = 'https://qacag.api.inmar.com/v1/member/'

        input = open(name)
        reader = csv.reader(input)
        header = True

        for row in reader:

            if header_row != True:
                headers = {'Content-type':'application/json','X-Inmar-REST-API-Key':'d98e72d4-f30c-4eac-9205-18ec125b5ab4'}
                #data = {'member':{'active':True,'identity':{'user_id':row[2],'proxy_id':0},'pii':{'first_name':row[0],'last_name':row[1],'primary_address_postal_code':row[3]},'optins':[{'optin_id':1040,'optin_value':1}]}}

                #try:
                #    request = urllib.request.Request(api_url, json.dumps(data).encode('utf8'), headers, method='DEL')
                #    response = urllib.request.urlopen(request)
                #except Exception as e:
                #    writer.write(str(e) + ',' + row[0] + ',' + row[1] + ',' + row[2] + ',' + row[3] + '\n')
            else:
                header_row = False

        processed = True

    return processed

def ProcessZipFile(name, log):
    processed = False

    # open the zip file
    file = open(name, 'rb')
    list = zipfile.ZipFile(file)

    # iterate each item within the file
    for item in list.namelist():
    
        # extract, process and delete csv files
        if item.find('.csv') != -1:
            list.extract(item, '.')

            # processing any single csv marks the entire zip as processed
            if processed == True:
                ProcessCSV(item, log)
            else:
                processed = ProcessCSV(item, log)

            os.remove(item)

    return processed

# query path for a list of fies
files = [f for f in os.listdir('.') if os.path.isfile(f)]

# iterate each file
for file in files:

    # process zip files only
    if file.find('.zip') != -1:
        processed = False

        log = file[0:len(file) - len('.zip')] + '.log'
        writer = open(log, 'w')

        proccessed = ProcessZipFile(file, writer)
        writer.close()

        # if we process the file, delete it
        if processed == True:
            os.remove(file)
        else:
            os.remove(log)
