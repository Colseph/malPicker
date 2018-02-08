#~File:malPicker.py
#~picks random show in chosen mal list can be filtered by type number of episodes

#~~~~~~~~~~Config~~~~~~~~~~#
logPath = '.\\' #~location to save log file (use double \\ because its the escape character
logNameInfo = 'malPicker' #~name for info log file (you dont need ext just name)
#~~~~~~~~End-Config~~~~~~~~#


#~import god files
import requests
from bs4 import BeautifulSoup
import logging
from random import randint

#~logging config
logging.basicConfig(filename=str(logPath) + str(logNameInfo) + '.log', filemode='w', level=logging.DEBUG) #~config for info logging


logging.info('Starging program')
#~start of prog(ive realized i tend to write my programs like i write batch files.. easier to read for novices i guess...
#~input - eventually will be GUI
#~for gui have check next to optional entries num eps etc
#~num of eps checkbox then entry then drop down < > = <= >=
#~type checkbox then
usrName = input("Enter Username: ")
print("lists:\nall anime\ncurrently watching\ncompleted\non hold\ndropped\nplan to watch")
listType = input("Enter the list you want(case sensitive): ")
#~epsCheckBox = input('would you like to filter by episodes(yes/no)?: ')
#~if epsCheckBox == yes:

#~little dictionary of what pages/statuses are what in MAL
listDict = {'all anime': 7, 'currently watching': 1, 'completed': 2, 'on hold': 3, 'dropped': 4, 'plan to watch': 6}

#~gets html from site(using list and username)
url = 'https://myanimelist.net/animelist/' + str(usrName) + '?status=' + str(listDict[listType])

logging.info('accessing: ' + str(url))
response = requests.get(url)
html = response.content

#~BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

#~graps the nicely premade dictionary already in the html(thanks MAL)
#null = "null"#~stops null no value error..
#true = "true"#~stops true no value error... shouldnt cause problems cuase not True keyword(case sensitive)
#false = "false"#~stops false no value error.. shouldnt cause problems bacuase not False keyword(case sensitive)
listTable = soup.find('table', attrs={'class': 'list-table'})

#~converts string to list. if i did listComplete = list(listTable.get('data-items')) then it would treat each character as a diff list item..
listCompleteString = listTable.get('data-items')#~retrieves string from html

#~converts string to list (VERY messy) because for some reason python treats it as a 1 item string instead of the list it is..
logging.info('creating list from html')
listComplete = []
entry1 = ''
entry2 = ''
listEntry = {}
whichEntry = 'entry1'
for char in listCompleteString:
    if char == '[':
        #~do nothing(leave the bracket out of the list)
        logging.info("skipping bracket: [")
        charOld = char
        continue
    elif char == ']':
        #~do nothing(leave brackets out of list
        logging.info("skipping bracket: ]")
        charOld = char
        continue
    elif char == '{':
        #~do nothint skips {
        logging.info("skipping bracket:{")
        charOld = char
        continue
    elif char == '}':
        #~adds entry to the list and resets listEntry, sets charOld as } to skip comma
        if charOld == '"':#~last entry in dict dont have comma, so this makes sure theyre not merged into next dict
            logging.info("adding last entry to dictionary")
            listEntry[entry1] = entry2
            logging.debug("'" + str(entry1) + "'" + ":" + "'" + str(entry2) + "'")
            entry1 = ''
            entry2 = ''
            whichEntry = 'entry1'
        logging.info("adding dictionary to list")
        listComplete.append(listEntry)
        logging.debug(listEntry)
        listEntry = {}
        charOld = char
        continue
    elif char == ',':
        if charOld == '}':
            logging.info("skipping comma: ,")
            #~skips comma
            charOld = char
            continue
        else:
            #~adds new dictionary entry
            logging.info("adding new entry to dictionary")
            listEntry[entry1] = entry2
            logging.debug("'" + str(entry1) + "'" + ":" + "'" + str(entry2) + "'")
            entry1 = ''
            entry2 = ''
            whichEntry = 'entry1'
            charOld = char
            continue
    elif char == ':':
        whichEntry = 'entry2'
        charOld = char
        continue
    elif char == '"':
        #~skipps double quoees- theyre replaced with single when added to dictionary
        logging.info('skipped double quotes: "')
        charOld = char
        continue
    else:
        if whichEntry == 'entry1':
            entry1 += char
            charOld = char
        else:
            entry2 += char
            charOld = char
logging.info('finished parsing html into list')
logging.info('Total Entries: ' + str(len(listComplete[0]) * len(listComplete)) + ' - ' + str(len(listComplete[0])) + ' Entries in ' + str(len(listComplete)) + ' Dictionaries')

#print(len(listComplete))
#itemFind = len(listComplete)
#for item in range(itemFind):
#    print(listComplete[item]['anime_title'])

#~picks a random anime in the list
randomAnime = randint(0,(len(listComplete) - 1))
logging.info('Picked Dictionary ' + str(randomAnime) + ': ' + str(listComplete[randomAnime]))
print("Anime in List: " + str(len(listComplete)) + '\nRandomly Picked Anime: ' + str(listComplete[randomAnime]['anime_title']) + '\nType: ' + str(listComplete[randomAnime]['anime_media_type_string']) + '\nEpisodes: ' + str(listComplete[randomAnime]['anime_num_episodes']) + '\nRating: ' + str(listComplete[randomAnime]['anime_mpaa_rating_string']))
logging.info('Program Complete')
#~mal uses jscript for values so if i did this id just get stuff like ${ item.animetitle } etc..
#listComplete = [] #~list to store all MAL list data to pick from
##~grabs each item in table
#for listTableData in soup.findAll('tbody', attrs={'class': 'list-table-data'}):
#    print(listTableData)
#
#    #~grabs title
#    dataTitle = listTableData.find('td', attrs={'class': 'data title clearfix'})
#    title = dataTitle.find('a', attrs={'class': 'link sort'})
#    print(title)
#
#    #~grabs type(TV OVA ETC)
#    dataType = listTableData.find('td', attrs={'class': 'data type'})
#    print(dataType)
#
#    #~graps number of episodes
#    dataProgress = listTableData.find('td', attrs={'class': 'data progress'})
#    #~only assigns span with total number of episodes(irrelevant if using completed list etc)
#    for span in listTableData.findAll('span'):
#        if '/' not in span:
#            episodes = span
#    print(episodes)
#
#
#    #~appends to list
#    listComplete.append([title.text, dataType.text, episodes.text])
#
#print(listComplete)









