import requests, bs4, random, time

s='https://mybook.ru'
k='/catalog/biznes-knigi/books'


def call_web(s,k): # create html text url
    print('call start')
    time.sleep(0.5)
    s=requests.get(s+k)
    return bs4.BeautifulSoup(s.text, 'html.parser')

def search_max_page(b): # search max page
    l=[]
    p=b.select('.ContextPagination__pagesButtons .PageButton__pageButton') # html current range page
    if len(p) > 0: # page > 0
        x=int(p[len(p)-1].getText().strip()) # end page
        for i in range(1,x+1):
            l.append(i)
    return l # [1, 2, 3, 4, ..., n] or []

def random_page(x,f): # random page
    global s, k
    p=[]
    if len(x) > 0:
        y=random.choice(x) # generate random page
        x.pop(x.index(y)) # remove index in list x
        n=[div.a for div in call_web(s,k+'?page='+str(y)).findAll('div', attrs={'class' : 'ContextBookCard__bookTitle'})] # create list books
        print('page',y,'im',len(x))
        for i in range(len(n)): # check random books
            y=random.choice(n)
            n.pop(n.index(y))
            print('books',y['href'],'book',i,'in',len(n))
            p=call_web(s,y['href']+'citations/').select('.TextTruncate__wrap .TextTruncate__text')
            if len(p) >= 6: # if citations >= 6
                f.append(y['href'])
                print('f',len(f),'/3')
                break
    if len(f) == 3 and len(x) > 0:
        return f
    else:
        return random_page(x,f)



#print(search_max_page(call_web(s,'/author/evgenij-shepin/vkusvill-kak-sovershit-revolyuciyu-v-ritejle-del-2/citations/')))

print(random_page(search_max_page(call_web(s,k)),[]))

#print(call_web(s,k).findAll('a', {'class': 'PageButton__pageButton'})['href'])





