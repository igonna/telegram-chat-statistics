from tkinter import Tk, Button, filedialog, Text, Scrollbar
from tkinter.ttk import Progressbar
from typing import List
from typing import Dict
import html_work
from time_period import TimePeriod
import numpy as np
import matplotlib.pyplot as plt

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

def print_users(users):
    periods: List[TimePeriod] = []
    
    user_names = []
    for user in users:
        periods.append(TimePeriod(user.days.values()))
        user_names.append(user.name)
    
    users_days = []
    
    
    for index, period in enumerate(periods):
        msg_count = period.get_msg_count()
        msg_count = msg_count if msg_count > 0 else 1
        avg_len_msg = round(period.get_msg_len() / msg_count, 2)
        user_name = user_names[index]
        
        output = f"[{user_name}] [words]: {period.get_words_count()} [messages]: {msg_count} [total length]: {period.get_msg_len()} [avg message length]: {avg_len_msg}"
        text_widget.insert('end', output)
        text_widget.insert('end', '\n')
        
        # top_words_count = 20
        # words = user.get_words()
        # all_words_sum = sum(words.values())
        # top_words = heapq.nlargest(top_words_count, words, key=words.get)
        # text_widget.insert('end', '\n')
        # for i, key in enumerate(top_words, start=1):
        #     percent = round(((words[key]/all_words_sum) * 100), 2)
        #     nice_view = f"{i}. {key}: {words[key]} {percent}%"
        #     text_widget.insert('end', nice_view + '\n')
        
        users_days.append(period.get_days_msg_count())
    
    draw_days_stacked_column_chart(users_days, user_names)
    #draw_days_percent_stacked_area_chart(users_days, user_names)
   
def draw_days_stacked_column_chart(periods, user_names):
    color_names = list(plt.cm.colors.CSS4_COLORS.keys())
    color_names = ["red", "blue", "green", "yellow", "orange", "purple"] + color_names

    max_days = max(periods, key=len)
    x_days = max_days.keys()    
    y_msg_counts = [[] for _ in range(len(periods))]
    
    for day in x_days:
        for index, days in enumerate(periods):
            day_count = days.get(day, 0)
            y_msg_counts[index].append(day_count)
            
    prev_index = 0
    for index, y_msg_count in enumerate(y_msg_counts):
        if not index:
            plt.bar(x_days, y_msg_count, label=user_names[index], color=color_names[index])
            prev_index = index
        else:    
            plt.bar(x_days, y_msg_count, bottom=y_msg_counts[prev_index], label=user_names[index], color=color_names[index])
    
    plt.xlabel('time')
    plt.ylabel('message count')
    plt.title('Message Count per Day')
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()
    #draw_days_percent_stacked_area_chart(x_days, y_msg_counts, user_names)


def draw_days_percent_stacked_area_chart(x_days, y_msg_counts, user_names):
    sum_msg_counts = np.array(y_msg_counts)
    
    percent = sum_msg_counts /  sum_msg_counts.sum(axis=0).astype(float) * 100

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.stackplot(x_days, percent, labels=user_names)
    ax.set_title('100 % stacked area chart')
    ax.set_ylabel('Percent (%)')
    ax.margins(0, 0)
    plt.xticks(rotation=45)
    plt.show()
        

def select_folder_action():
    text_widget.delete('1.0', 'end')
    dir = filedialog.askdirectory()
    files = html_work.get_html_files(dir)
    init_progress_loading(len(files))
    html_objects = html_work.files_to_html(files, increase_progress_loading)
    init_progress_processing(len(files))
    users = html_work.analyze_htmls(html_objects, increase_progress_processing)
    print_users(users)


root = Tk()
root.title('telegram chat statistics')

select_button = Button(root, text='Select Folder', command=select_folder_action)
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

#select_folder_action()

root.mainloop()