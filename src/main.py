from bs4 import BeautifulSoup
from tkinter import Tk, Button, filedialog, Text, Scrollbar
from tkinter.ttk import Progressbar
import glob, os
from typing import List
import heapq

class User:
    def add_word(self, word):
        if word in self.__words:
            self.__words[word] += 1
        else:
            self.__words[word] = 1
    
    def inc_message_count(self):
        self.__messages_count += 1
    
    def __init__(self, name):
        # messages (content, date, length)
        self.__messages_count = 0
        self.__name = name
        self.__words = {}
        self.message_lenght = 0
    
    def get_words_count(self):
        return len(self.__words.values())
    
    def get_messages_count(self):
        return self.__messages_count
    
    def get_name(self):
        return self.__name
    
    def get_words(self):
        return self.__words

def get_html_files(dir):
    html_file_paths = []
    os.chdir(dir)
    for file in glob.glob('*.html'):
        html_file_paths.append(dir + '/' + file)
    return html_file_paths

def file_to_html(path):
    f = open(path, 'r')
    return BeautifulSoup(f.read(), 'html.parser')

def files_to_html(files, update_callback):
    html_objects = []
    for file in files:
        html_objects.append(file_to_html(file))
        update_callback()
    return html_objects

# progress bar

def init_progress_loading(count):
    progress_bar_loading['maximum'] = count
    progress_bar_loading['value'] = 0

def increase_progress_loading():
    progress_bar_loading['value'] += 1
    root.update()
    
def init_progress_processing(count):
    progress_bar_processing['maximum'] = count
    progress_bar_processing['value'] = 0

def increase_progress_processing():
    progress_bar_processing['value'] += 1
    root.update()


# analyze start
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
            
            try:
                last_name = name.text.strip()
            except:
                pass
            
            words = []
            try:
                message = str.lower(message.text).strip()
                message = ''.join(char for char in message if char.isalpha() or char == ' ') 
                
                if last_name not in users:
                    users[last_name] = User(last_name)
                
                user = users[last_name]
                user.inc_message_count()

                words = message.split()
                user.message_lenght += len(message)
                
                for w in words:
                    user.add_word(w)
            except:
                pass
    
    usr_keys = list(users.keys()) 
    users_arr = []
    for usr_key in usr_keys:
        users_arr.append(users[usr_key])
    return users_arr


def print_users(users: List[User]):
    users = users[0:2]
    top_words_count = 20
    for user in users:
        #print(user.get_name(), 'words: ', user.get_words_count(), 'messages: ', user.get_messages_count())
        avg_len_msg = round(user.message_lenght / user.get_messages_count(), 2)
        output = f"[{user.get_name()}] [words]: {user.get_words_count()} [messages]: {user.get_messages_count()} [total length]: {user.message_lenght} [avg lenght per message]: {avg_len_msg}"
        #text_widget.insert('end', str() + ' words: ' + str() + ' messages: ' + str(user.get_messages_count()))
        text_widget.insert('end', output)
        words = user.get_words()
        all_words_sum = sum(words.values())
        top_words = heapq.nlargest(top_words_count, words, key=words.get)
        text_widget.insert('end', '\n')
        for i, key in enumerate(top_words, start=1):
            percent = round(((words[key]/all_words_sum) * 100), 2)
            nice_view = f"{i}. {key}: {words[key]} {percent}%"
            text_widget.insert('end', nice_view + '\n')
        text_widget.insert('end', '\n')
    

def do_work():
    dir = filedialog.askdirectory()
    files = get_html_files(dir)
    #files = files[0:5]
    init_progress_loading(len(files))
    html_objects = files_to_html(files, increase_progress_loading)
    init_progress_processing(len(files))
    users = analyze_htmls(html_objects, increase_progress_processing)
    print_users(users)


root = Tk()
root.title('telegram chat statistics')

select_button = Button(root, text='Select Folder', command=do_work)
select_button.pack()

text_widget = Text(root, width=80, height=30)
text_widget.pack(side='left', fill='both', expand=True)

scrollbar = Scrollbar(root)
scrollbar.pack(side='right', fill='y')

text_widget.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_widget.yview)

progress_bar_loading = Progressbar(root, orient='horizontal', length=200, mode='determinate')
progress_bar_loading.pack()

progress_bar_processing = Progressbar(root, orient='horizontal', length=200, mode='determinate')
progress_bar_processing.pack()

root.mainloop()
