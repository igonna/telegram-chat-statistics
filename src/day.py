class Day:
    def add_message(self, msg):
        self.total_msg_count += 1
        self.total_msg_len += len(msg)
        
        self.messages.append(msg)
        
        words = msg.split()
        self.total_words_count += len(words)
        
        for word in words:
            if word in self.words:
                self.words[word] += 1
            else:
                self.words[word] = 1

    def __init__(self, date):
        self.total_msg_len = 0
        self.total_msg_count = 0
        self.total_words_count = 0
        self.date = date
        self.words = {}
        self.messages = []