import pickle

class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = [];
        self.index = {}
        self.total_msgs = 0
        self.total_words = 0
        
    def get_total_words(self):
        return self.total_words
        
    def get_msg_size(self):
        return self.total_msgs
        
    def get_msg(self, n):
        return self.msgs[n]
        
    # implement
    def add_msg(self, m):
        self.msgs.append(m)
        self.total_msgs += 1
        
    def add_msg_and_index(self, m):
        self.add_msg(m)
        line_at = self.total_msgs - 1
        self.indexing(m, line_at)

    # implement
    def indexing(self, m, l):
        punc = "!?:;,."
        words = m.split(" ")
        for word in words:
            word = word.strip(punc)
            try:
                self.index[word.lower()].append(l)
            except:
                self.index[word.lower()] = [l]
        
    # implement: query interface
    '''
    return a list of tuples. If we index the first sonnet (p1.txt), then
    calling this function with term 'thy' will return the following:
    [(7, " Feed'st thy light's flame with self-substantial fuel,"),
     (9, ' Thy self thy foe, to thy sweet self too cruel:'),
     (9, ' Thy self thy foe, to thy sweet self too cruel:'),
     (12, ' Within thine own bud buriest thy content,')]          
    '''                      
    def search(self, term):
        msgs = []
        t_msgs = []
        indexes = []

        words = term.split()
        #phrase search
        if len(words) > 1:
            for word in words:
                t_msgs.append(self.search(word))
            for i in range(1, len(words)):
                for j in range(len(t_msgs[0])):
                    if t_msgs[0][j] in t_msgs[i]:
                        msgs.append(t_msgs[0][j])
            if msgs == []:
                return "No results found."
        #single word search
        else:
            if term in self.index.keys():
                indexes = self.index[term]
            else:
                return "No results found."
            for index in indexes:
                new_t = (index, self.get_msg(index))
                #remove dublicates
                if new_t not in msgs:
                    msgs.append(new_t)
                    
        return msgs
        
            
class PIndex(Index):
    def __init__(self, name):
        super().__init__(name)
        roman_int_f = open('roman.txt.pk', 'rb')
        self.int2roman = pickle.load(roman_int_f)
        roman_int_f.close()
        self.load_poems()
        
        # Implement: 1) open the file for reading, then call
        # the base class's add_msg_and_index
    def load_poems(self):
        lines = open(self.name, 'r').readlines()
        for l in lines:
            self.add_msg_and_index(l.strip())
    
        # Implement: p is an integer, get_poem(1) returns a list,
        # each item is one line of the 1st sonnet
    def get_poem(self, p):
        poem = []
        if p > 0 and p < 155:
            start = self.int2roman[p] + "."
            end = self.int2roman[p+1] + "."
            s_num = 0
            e_num = 0
            for i in range(self.get_msg_size()):
                if self.get_msg(i) == start:
                    s_num = i
                elif self.get_msg(i) == end:
                    e_num = i
                    break
                else:
                    e_num = i
            for j in range(s_num, e_num):
                poem.append(self.get_msg(j))
        else:
            return "Index out of range"
        return poem

if __name__ == "__main__":
    # The next three lines are just for testing
    # You are encouraged to add to this and create your own tests!
    # Call your functions as you implement them and see if they work
    sonnets = PIndex("AllSonnets.txt")
    p154 = sonnets.get_poem(154)
    print(p154)
    
    s_five = sonnets.search("five")
    print(s_five)
    
    p_fh = sonnets.search("five hundred")
    print(p_fh)
    
    p_ie = sonnets.search("i eat")
    print(p_ie)
    
    p1 = PIndex("p1.txt")
    s_thy = p1.search("thy")
    print(s_thy)