import os,io
import time,glob
import pandas as pd
import mimetypes,datetime
from shivam import Create_Service
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
z=str(datetime.datetime.now())

CLIENT_SECRETE_FILE='client_secret_185821502019-52o7bcj2m6vk35iia8q3q87aghvgqrvh.apps.googleusercontent.com.json'
API_NAME='drive'
API_VERSION='v3'
SCOPES=['https://www.googleapis.com/auth/drive']
service = Create_Service(CLIENT_SECRETE_FILE,API_NAME,API_VERSION,SCOPES)



def download():
    file_ids,file_drive_names = fileIdCapture()
    file_names=listtt()
    i=0
    while i<len(file_drive_names):
        if file_drive_names[i] in file_names:
            file_drive_names.pop(i)
            file_ids.pop(i)
        else:
            i+=1

    
    for file_id,file_name in zip(file_ids,file_drive_names):
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloder=MediaIoBaseDownload(fd=fh,request=request)

        done=False
        while not done:
            status, done =  downloder.next_chunk()
            print("Download progres {0}".format(status.progress()*100))
        fh.seek(0)
        with open(os.path.join('',file_name),"wb")as f:
            f.write(fh.read())
            f.close()



def fileIdCapture():
    folder_id = "1TRXEEZXSfeChVwg6_g2fl_aU5p8us9cH"
    query = f"parents = '{folder_id}'"
    response = service.files().list(q=query).execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = service.files().list(q=query,pagrToken=nextPageToken).execute()
        files.extend(response.get('files'))
        nextPageToken = response.get('nextPageToken')
    
    df = pd.DataFrame(files)
    files_ids = df['id'].tolist()
    file_names = df['name'].tolist()
    return (files_ids,file_names) 
    

def upload():
    folder_id = "1TRXEEZXSfeChVwg6_g2fl_aU5p8us9cH"
    file_names=listtt()
    file_ids,file_drive_names=fileIdCapture()
    mime_types=[]
    for i in file_names:
        if i in file_drive_names:
            file_names.remove(i)
        else:
            mime_types.append(str(mimetypes.MimeTypes().guess_type(i)[0]))

    
    for file_name,mime_type in zip(file_names,mime_types):
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]

            }
        media = MediaFileUpload(format(file_name),mimetype=mime_type)

        file=service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

def update():
    folder_id = "1TRXEEZXSfeChVwg6_g2fl_aU5p8us9cH"
    file_ids,file_names=modi()
    mime_types=[]
    for i in file_names:
        mime_types.append(str(mimetypes.MimeTypes().guess_type(i)[0]))


    for file_name,mime_type,file_id in zip(file_names,mime_types,file_ids):
        file_metadata = {
            'name': file_name,
            'addParents': [folder_id]

            }
        media = MediaFileUpload(format(file_name),mimetype=mime_type)
        updated_file = service.files().update(
                fileId=file_id,
                body=file_metadata,
                media_body=media
                ).execute()


def listtt():
    file_names=[]
    for i in glob.glob(r'*'):
        if (i == '__pycache__' or i=='token_drive_v3.pickle' or i == 'shivam.py' or i== 'pd project.py'  or i=='client_secret_185821502019-52o7bcj2m6vk35iia8q3q87aghvgqrvh.apps.googleusercontent.com.json'):
            pass
        else:
            file_names.append(i)
    return(file_names)
    

def modi():
    a=[]
    file_names=listtt()
    for i in file_names:
        x=time.ctime(os.path.getmtime(i))
        y=str(datetime.datetime.now())
        date=(int(y[8:10]))-(int(x[8:10]))
        hrs=(int(y[11:13]))-(int(x[11:13]))
        minu=(int(y[14:16]))-(int(x[14:16]))
        datexz=(int(x[8:10]))-(int(z[8:10]))
        hrsxz=(int(x[11:13]))-(int(z[11:13]))
        minuxz=(int(x[14:16]))-(int(z[14:16]))


        if(datexz>0 or hrsxz>0 or minuxz>=3):
            if(date>0 or hrs>0 or minu>=3):
                a.append(i)


    file_ids=[]
    file_drive_names=[]
    file_ids , file_drive_names = fileIdCapture()
    
    i=0
    while(i<len(file_drive_names)):
        if file_drive_names[i] not in a:
            file_ids.pop(i)
            file_drive_names.pop(i)
        else:
            i+=1
    return(file_ids,file_drive_names)


upload()
        