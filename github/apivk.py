# -*- coding: utf-8 -*-
import requests, vk, time, psycopg2, random,sys, glob, os #Image
from datetime import date
from psycopg2 import sql

reload(sys)
sys.setdefaultencoding('utf-8')

data_result = []
path_photo = '/home/artem/tmpjpg/'
TOKEN = '07de2b623eed2486f93ab755b3a8327f767a758f4012052793bc517195aeec40c8906339a726a06c0c8f9'
APIV = '5.101'
PUB_ID = 182371107


def get_dml_db( select_id):
    x=[]
    case_sql = {
        1: 'SELECT ID FROM CORE_TABLE WHERE COUNT_CITAT >= 6 AND ( DATE (CURRENT_DATE) - DATE (DATE_PUBLIC) > 14 OR DATE_PUBLIC ISNULL );',
        2: 'SELECT AVTOR, BOOK_NAME, PATH FROM CORE_TABLE WHERE ID IN %s'
    }
    conn = psycopg2.connect(dbname='test_db', user='tpython',                   # connect db
                            password='12345678', host='localhost', port='5432')
    with conn.cursor() as cursor:
        if select_id == 1:
            #cursor.execute(case_sql[select_id], (obj, ) )
            cursor.execute(case_sql[select_id])
            for row in cursor:
                x.append(row[0])
            y = tuple(random.sample(x,9))
            print('get_dml_db ID =',y)
            cursor.execute(case_sql[2], (y, ) )
            x = []
            for row in cursor:
                x.append(row)  # x[0]=avtor,book,path x[0][0]=avtor x[0][1]=book
    return x


def get_saveWallPhoto(vk_api,upload_url, id_photo):
    global data_result, PUB_ID

    file = {'photo': open(id_photo, 'rb') }
    upload_response = requests.post(upload_url, files=file).json()
    # insert  | caption='Test_ '+path_photo |
    save_result=vk_api.photos.saveWallPhoto( group_id=PUB_ID, photo=upload_response['photo'],server=upload_response['server'],
                                             hash=upload_response['hash'] )
    print(str(save_result[0]['owner_id']))
    data_result.append(('photo'+str(save_result[0]['owner_id'])+'_'+str(save_result[0]['id'])+
                  '&access_key='+str(save_result[0]['access_key'])))


def get_polls_create(vk_api,y):
    global data_result,PUB_ID

    d = date(2019, 8, 23)
    data_parsing = int(time.mktime(d.timetuple()))
    print(data_parsing)
    polls=vk_api.polls.create(question="test", end_date=data_parsing , owner_id=-PUB_ID,add_answers="["+','.join(y)+"]")
    data_result.append(('poll'+str(polls['owner_id'])+'_'+str(polls['id'])))



def main():
    global data_result, TOKEN, APIV, PUB_ID, path_photo
    y = []

    # Create session in VK
    session=vk.Session(access_token=TOKEN)
    vk_api = vk.API(session, v=APIV)

    upload_url=vk_api.photos.getWallUploadServer(group_id=182371107)['upload_url']
    #get_saveWallPhoto(vk_api, upload_url, '0ac97a36-2c93-4f04-a118-d7c731413f39.jpg')
    #get_saveWallPhoto(vk_api, upload_url, 'f9a674c3-f77c-495e-874d-e0ab33b43f2a.jpg')

    # Start Create poll in wall public vk
    # connect database, select data ( avtor, books and path foto )
    x=get_dml_db(1)
    print(len(x))
    # check count books ( if == 10 )
    if len(x) == 9:
        for i in range(len(x)):
            filename = os.path.splitext(glob.glob(path_photo+x[i][2]+'*')[0])
            print('Path '+x[i][2])
            if filename[1] == '.jpe':
                print('Rename '+path_photo+x[i][2])
                os.rename(filename[0]+filename[1], filename[0]+'.jpg')
                get_saveWallPhoto(vk_api, upload_url, filename[0]+'.jpg')
            else:
                get_saveWallPhoto(vk_api, upload_url, filename[0]+filename[1])
            y.append("\""+x[i][0]+" | "+x[i][1]+"\"")
        get_polls_create(vk_api,y)

    # posting VK wall public
    result2=vk_api.wall.post(attachments=data_result,owner_id=-PUB_ID,from_group=1,message='TEST')


main()
#filename = os.path.splitext(glob.glob('/home/artem/tmpjpg/fd300ab3-f429-488e-a0d8-05e049b9b4be*')[0])
#print(filename[1])
#if os.path.splitext(glob.glob('/home/artem/tmpjpg/fd300ab3-f429-488e-a0d8-05e049b9b4be*')[0])[1] ==  '.jpe':
#   print('!!!')
#   print(filename)
#   c=os.rename(filename[0]+filename[1], filename[0]+'.jpg')
#   print(c)


#im = Image.open('Foto.jpg')
#im.save('Foto.png')