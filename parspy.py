import requests, bs4


s=requests.get('https://mybook.ru/author/stanislav-logunov/put-samuraya-vnedrenie-yaponskih-biznes-principov/citations/')
b=bs4.BeautifulSoup(s.text, "html.parser")
#p3=b.select('.temperature .p3')
#pogoda1=p3[0].getText()
#p4=b.select('.temperature .p4')
#pogoda2=p4[0].getText()
#p5=b.select('.temperature .p5')
#pogoda3=p5[0].getText()
#p6=b.select('.temperature .p6')
#pogoda4=p6[0].getText()
#print('Yt :' + pogoda1 + ' ' + pogoda2)
#print('Dn :' + pogoda3 + ' ' + pogoda4)
p=b.select('.TextTruncate__wrap .TextTruncate__text')
for i in range(len(p)):
    print
    print(p[i].getText().strip())


https://gist.github.com/eff9bfc3be3ebcf69403bbda265c8705