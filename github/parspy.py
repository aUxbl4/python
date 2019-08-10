import requests, bs4, random, time, psycopg2, re, uuid, urllib, os, urlparse
from psycopg2 import sql

#global
s='https://mybook.ru'
k='/catalog/biznes-knigi/books'
file_dir='/home/artem/tmpjpg/'


def get_dml_db( values, insert_id, select_id, obj): # values=[('','', n)] insert_id= 1 or 2 select_id= 3 or 4, obj=path or url
    x=''
    case_sql = {
        1: 'INSERT INTO CORE_TABLE (AVTOR, BOOK_NAME, PATH, COUNT_CITAT, URL) VALUES {}',
        2: 'INSERT INTO CITATIONS (CITATION, ID_BOOKS) VALUES {}',
        3: 'SELECT ID FROM CORE_TABLE WHERE PATH = %s',
        4: 'SELECT ID FROM CORE_TABLE WHERE URL = %s'
    }
    print('call get_dml_db')
    print('get_dml_db', insert_id, select_id, obj)
    conn = psycopg2.connect(dbname='test_db', user='tpython',                   # connect db
                            password='12345678', host='localhost', port='5432')
    with conn.cursor() as cursor:
        if insert_id > 0:
            conn.autocommit = True
            insert = sql.SQL(case_sql[insert_id]).format(
                sql.SQL(',').join(map(sql.Literal, values))
            )
            cursor.execute(insert)
            print('ok')
        if select_id > 0:
            cursor.execute(case_sql[select_id], (obj, ) )
            for row in cursor:
                x=row[0]
    return x



def get_call_web(s,k): # create html text url
    print('call get_call_web')
    print('get_call_web',s,k)
    time.sleep(random.uniform(0.5,1.5))
    s=requests.get(s+k)
    return bs4.BeautifulSoup(s.text, 'html.parser')


def get_search_max_page(b): # search max page
    print('call get_search_max_page')
    l=[]
    p=b.select('.ContextPagination__pagesButtons .PageButton__pageButton') # html current range page
    if len(p) > 0: # page > 0
        x=int(p[len(p)-1].getText().strip()) # end page
        for i in range(1,x+1):
            l.append(i)
    else:
        l.append(1)
    return l # [1, 2, 3, 4, ..., n] or []


def get_select(y):
    global s, file_dir
    #y='/author/l-e-kalinina/kommentarij-k-federalnomu-zakonu-o-privatizacii-go/' #test
    a=[]
    p=[]
    # select avtor and name book and name foto
    b=get_call_web(s,y) # call html pars

    print('!!!!!!!!!!!!!!!!!!!!!!!! ')
    print(b.findAll('h1', attrs={'class' : 'BookPageHeaderContent__coverTitle'})[0].text)
    for k in (b.findAll('a', attrs={'class' : 'BreadCrumbs__link'})): # avtor and book_name
        print(k.text)
        a.append(k.text)
    if len(a)==3: # check avtor, if NOT then a[3] = '-'
        a.insert(3,a[2])
        a.insert(2,'-')

    b=get_call_web(s,y+'citations/') # call html pars
    max=get_search_max_page(b)


    d=b.select('.section .BookCitationListView__count')
    print('count= ',b.findAll('div', attrs={'class' : 'BookCitationListView__count'}))

    for j in enumerate(b.findAll('link')): # select and save foto (jpg)
        if re.search(r'c/200x300',j[1]['href']):
            filename = str(uuid.uuid4()) # create random name file
            file_path = urlparse.urlparse(j[1]['href']).path
            ext = os.path.splitext(file_path)[1]
            if ext == '.jpe': ext = '.jpg' # remove format
            urllib.urlretrieve(re.sub(r'c/200x300','p/600x',j[1]['href']), file_dir+filename+ext)
            print('filename', file_dir+filename+ext)
            break

    print('a= ',a)
    print(a[2])
    print(a[3])
    print('filename= ',filename)
    print('re.match(r,d[0].text).group()= ',re.match(r'\d*',d[0].text).group())
    print('y= ',y)
    p.append((a[2],a[3],filename,re.match(r'\d*',d[0].text).group(),y)) # finish avtor and book name, count citats

    id=get_dml_db(p,1,3,filename) # insert avtor and name book, select id book
    for i in max:
        n=[]
        print('i=',i)
        if i > 1:
            b=get_call_web(s,y+'citations/'+'?page='+str(i))
            print('next page')
        for text in b.select('.TextTruncate__wrap .TextTruncate__text'):  # select citation
            n.append((text.getText().strip(),id))
        if len(n)>0:
            cou_c += len(n)
            get_dml_db(n,2,0,0)
    print(cou_c)

def get_random_page(x): # random page
    print('call get_random_page')
    global s, k

    if len(x) > 0:
        y=random.choice(x) # generate random page
        x.pop(x.index(y)) # remove index in list x
        n=[div.a for div in get_call_web(s,k+'/?page='+str(y)).findAll('div', attrs={'class' : 'ContextBookCard__bookTitle'})] # create list books
        print('get_random_page page=',y)
        for i in range(len(n)): # check random books
            y=random.choice(n)
            n.pop(n.index(y))
            print('get_random_page books=',y['href'])
            if get_dml_db('',0,4,y['href']) == '':
                get_select(y['href'])
            else:
                print('lose')
            #break #test
        get_random_page(x)  # if test then insert #
        print('next page books')


get_random_page(get_search_max_page(get_call_web(s,k)))








