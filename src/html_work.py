import glob, os
from bs4 import BeautifulSoup
from user import User
from datetime import datetime

def get_html_files(dir):
    html_file_paths = []
    os.chdir(dir)
    for file in glob.glob('*.html'):
        html_file_paths.append(dir + '/' + file)
    return html_file_paths

def file_to_html(file_name):
    f = open(file_name, encoding="utf8")
    return BeautifulSoup(f.read(), 'html.parser')

def files_to_html(files, update_callback):
    html_objects = []
    for file in files:
        html_objects.append(file_to_html(file))
        update_callback()
    return html_objects

def analyze_htmls(objs, update_callback):
    
    users = {}
    for obj in objs:
        update_callback()
        messages = obj.html.body.div.find('div', class_='page_body').find('div', class_='history').find_all('div', class_='message')
        last_name = ''
        for msg in messages:
            body = msg.find('div', class_='body')
            name = body.find('div', class_='from_name')
            message = body.find('div', class_='text')
            
            if message:
                if name:
                    last_name = name.text.strip()
                if last_name not in users:
                    users[last_name] = User(last_name)
                if not last_name:
                    continue
                
                date_div = body.find('div', class_='date')
                date = ''
                if date_div:
                    date_str = date_div['title']
                    date_format = "%d.%m.%Y %H:%M:%S UTC%z"
                    date = datetime.strptime(date_str, date_format)
                    date = date.date()
                else:
                    continue
                
                message = str.lower(message.text).strip()
                message = ''.join(char for char in message if char.isalpha() or char == ' ')
            
                user = users[last_name]
                user.add_message(date, message)
    
    usr_keys = list(users.keys()) 
    users_arr = []
    for usr_key in usr_keys:
        users_arr.append(users[usr_key])
        
    return users_arr#[0:2]