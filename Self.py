from bs4 import BeautifulSoup
import requests
from datetime import date,timedelta, datetime

date_test = []
today = datetime.today()
for i in range(10):
    date_test.append(today-timedelta(days=1))
# DATE = '2021-01-23'
# print(date_test)


def clean_1(l):
    # clean commas and brackets
    for i in range(1,len(l)):
        for j in range(len(l[i][1])):
            # print(l[i][1][j])
            if l[i][1][j] == '(':
                l[i][1] = l[i][1][:j].strip()
                break
    for i in range(1,len(l)):
        for j in range(len(l[i][1])):
            if l[i][1][j] == ',':
                l[i][1] = l[i][1][:j] + l[i][1][j+1:]
                break

        l[i][1] = int(l[i][1])
    return l
    # for i in l:
    #     print(i[1],type(i[1]))
# clean_1([['NEGERI', 'BILANGAN KES BAHARU *( )', 'BILANGAN KES KUMULATIF'], ['SABAH', '260 (1)', '34,083'], ['SELANGOR', '692 (2)', '23,623'], ['W.P. KUALA LUMPUR', '197 (3)', '9,623'], ['NEGERI SEMBILAN', '174', '6,858'], ['JOHOR', '77 (2)', '2,912'], ['PULAU PINANG', '37', '2,900'], ['KEDAH', '4', '2,869'], ['PERAK', '65', '2,775'], ['W.P. LABUAN', '19', '1,495'], ['SARAWAK', '1', '1,085'], ['PAHANG ', '6', '861'], ['MELAKA', '140', '691'], ['KELANTAN', '1', '483'], ['TERENGGANU', '4', '285'], ['W.P. PUTRAJAYA', '6', '228'], ['PERLIS', '0', '45'], ['JUMLAH KESELURUHAN', '1,683 (8)', '90,816']]
# )




def detail(link):
    import csv
    # url = "https://kpkesihatan.com/"
    # source = requests.get(url).text
    # soup = BeautifulSoup(source, 'lxml')
    # print(soup.prettify())
    url = link
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    # n = soup.find_all('figure',class_='wp-block-table')
    n = soup.findAll('figure',class_='wp-block-table')[1]
    # print(url)

    # for i in n:
    #     print(i)
    # print(n.table.tbody)
    # return

    temp = []
    # for j in n[1:]:
    for j in n.table.tbody:
        try:
            tr = j.find_all('td')
            # print(tr)
            # return
        except:
            pass
            print('j',tr)
        else:
            # for h in tr:
            #     tds = h.find_all('td')
            # temp.append([tds[0].text,tds[1].text,tds[2].text])
            temp.append([tr[0].text,tr[1].text,tr[2].text])
    try:
        l = len(temp[0][1])
    except:
        # print(temp)
        print('Sorry there was an error, please go to the link above.')
        return
    for i in range(l):
        if temp[0][1][i] == '*':
            temp[0][1] = temp[0][1][:i+1] + '( )'
            break
    # for i in temp:
    #     print(i)
    return temp





def Filter(INPUT,Sort=None):
    if date(int(INPUT[0:4]),int(INPUT[5:7]),int(INPUT[8:])) > date.today():
        print(f'This date is in the future! Please enter any date before {date.today()}')
        return
    url = "https://kpkesihatan.com/"
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    strings = soup.find_all('time',class_='entry-date')

    # target = f"Kenyataan Akhbar KPK {day_of_month} Disember 2020 – Situasi Semasa Jangkitan Penyakit Coronavirus 2019 (COVID-19) di Malaysia"
    state = 'all'

    ### duplicate times
    duplicates = []
    term = ''
    for i in range(0,len(strings)):
        if strings[i].text == term: # if date is equals to previous date
            duplicates.append([strings[i]['datetime'][:10],i]) # add duplicate dates with their order according to the website
        else:
            term = strings[i].text
        # print(strings[i]['datetime'][:10]) # list of dates
        # print(strings[i],i)
    # print(duplicates) # duplicate dates
    # print(INPUT)

    correct_link_id = ''
    for i in duplicates:
        if INPUT == i[0]:
            # print(INPUT,i[1])
            correct_link_id = i[1] # taking the latest date
    if correct_link_id == '': # input is not one of duplicates
        for i in range(len(strings)):
            # print(strings[i]['datetime'][:10],INPUT)
            if strings[i]['datetime'][:10] == INPUT:
                correct_link_id = i
    # print(correct_link_id)
    # return
    # print('correct_link_id',correct_link_id)
    # return
    # print()
    print('If there is an error, please go to the link: ',end='')
    print(url)
    print()
    if len(INPUT)==10:
        if correct_link_id == '' and date(int(INPUT[0:4]),int(INPUT[5:7]),int(INPUT[8:])) != date.today():# date is too long ago, information not in website
            # print(date(int(INPUT[0:4]),int(INPUT[5:7]),int(INPUT[8:])), date.today())
            print(INPUT,'might be too long ago and may not be available anymore. Please go to the link above for more information.')
            return
    ### end of duplicate times

    for i in range(0,len(strings)):
        # print(i)
        if strings[i].has_attr('datetime') and strings[i]['datetime'][:10].strip() == INPUT and i == correct_link_id:
            # print(INPUT)
            parent_link = strings[i].find_parent('a')['href'] # finding first parent
            # print(parent_link,'pl')
        # print(INPUT,i['datetime'][:10].strip())
        else:
            # print(strings[i])
            continue
        # continue
        # return
        if parent_link:
            if not Sort:
                t = detail(parent_link)
                # for i in t:
                #     if state.upper() == "ALL":
                #         print(i)
                #     if state.upper() == i[0]:
                #         print(i)
                #         break
                return t
            else:
                t = detail(parent_link)
                if t:
                # print(t)
                    t = clean_1(t)
                    if Sort.upper() == 'A':
                        for i in range(1,len(t)-2):
                            for j in range(1,len(t)-2):
                                if t[j][1] > t[j+1][1]:
                                    t[j+1],t[j] = t[j],t[j+1]
                    else:
                        for i in range(1,len(t)-2):
                            for j in range(1,len(t)-2):
                                if t[j][1] < t[j+1][1]:
                                    t[j+1],t[j] = t[j],t[j+1]
                # for i in t:
                #     if state.upper() == "ALL":
                #         print(i)
                #     if state.upper() == i[0]:
                #         print(i)
                #         break
                    return t
    foo = f'{date.today().year}-{date.today().month}-{date.today().day}'
    if len(foo) == 8:
        foo = f'{date.today().year}-0{date.today().month}-0{date.today().day}'
    if foo == INPUT:
        print('Unavailable, please try again at around 6:00 pm to 7:00 pm.')
        return 'Unavailable, please try again at around 6:00 pm to 7:00 pm.'
    else:
        return 'Sorry here was an error, plese go to the link above.'



def overview():
    source = requests.get('https://www.worldometers.info/coronavirus/country/malaysia/').text
    soup = BeautifulSoup(source, 'lxml')
    # print(soup.prettify())

    n = soup.find_all('li',class_='news_li')
    nn = soup.find_all('div',class_='news_date')
    nnn = soup.find_all('button',class_='btn btn-light date-btn')
    dates = []
    temp = ''
    for i in nn:
        temp += i.h4.text
    dates.append(temp)
    temp = ''
    for i in nnn:
        dates.append(i.text)
    # for i in dates:
    #     print(i)

    c = 0
    for i in n:
        print(dates[c],i.strong.text)
        c += 1


# overview()



print()
print('For results today, you do not need to enter the date. Simply skip by pressing enter. For results on other days, please specify the date in the form yyyy-mm-dd.')
print()
ans = input('Enter date: ')
# ans = DATE
# for i in date_test:
#     ans = f'{i.year}-{i.month}-{i.day}'
base = date.today()
date_list = [base - timedelta(days=x) for x in range(10)]


def check_input(d):
    if type(d) == date:
        if len(str(d)) == 8: # yyyy-m-d
            return str(f'{d.year}-0{d.month}-0{d.day}')
        else: # yyyy-mm-dd
            return str(f'{d.year}-{d.month}-{d.day}')
    if len(d) == 0:
        return str(f'{date.today()}')
    temp = d.split('-')
    return str(f'{temp[0]}-{temp[1]}-{temp[2]}')

print()
print('Date entered:',check_input(ans))
print()
t = Filter(check_input(ans),'d')
if t:
    for i in t[1:]:
        try:
            print(f'{i[0]} : {i[1]}')
        except:
            break
            print('Unavailable :(')
else:
    print()
    print('Unavailable')





def xxx():


    # yesterday = today - timedelta(days=1) # get yesterday
    target = INPUT.strftime("%Y-%m-%d") # yyyy-mm-dd


    # dd/mm/YY
    d1 = today.strftime("%d/%m/%Y")
    print("d1 =", d1)

    # Textual month, day and year
    d2 = today.strftime("%B %d, %Y")
    print("d2 =", d2)

    # mm/dd/y
    d3 = today.strftime("%m/%d/%y")
    print("d3 =", d3)

    # Month abbreviation, day and year
    d4 = today.strftime("%b-%d-%Y")
    print("d4 =", d4)

    # yesterday
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    print(yesterday)
# xxx()





def location():
    url = "https://kpkesihatan.com/"
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

# location()
