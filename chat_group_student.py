S_ALONE = 0
S_TALKING = 1

#==============================================================================
# Group class:
# member fields: 
#   - An array of items, each a Member class
#   - A dictionary that keeps who is a chat group
# member functions:
#    - join: first time in
#    - leave: leave the system, and the group
#    - list_my_peers: who is in chatting with me?
#    - list_all: who is in the system, and the chat groups
#    - connect: connect to a peer in a chat group, and become part of the group
#    - disconnect: leave the chat group but stay in the system
#==============================================================================

class Group:
    
    def __init__(self):
        self.members = {}
        self.chat_grps = {}
        self.grp_ever = 0
        
    def join(self, name):
        self.members[name] = S_ALONE       
        
    #implement        
    def is_member(self, name):
        if name in self.members.keys():
            return True
        return False
            
    #implement
    def leave(self, name):
        in_group, group_key = self.find_group(name)
        if in_group:
            self.disconnect(name)
        del self.members[name]
        
    #implement                
    def find_group(self, name):
        found = False
        group_key = 0
        if self.is_member(name):
            for i in self.chat_grps.keys():
                if name in self.chat_grps[i]:
                    found = True
                    group_key = i
        return found, group_key
        
    #implement                
    def connect(self, me, peer):
        #if peer is in a group, join it
        peer_in_group, group_key = self.find_group(peer)
        if peer_in_group:
            self.chat_grps[group_key].append(me)
        # otherwise, create a new group with you and your peer
        else:
            index = len(self.chat_grps)
            for i in range(len(self.chat_grps)):
                if i not in self.chat_grps.keys():
                    index = i
                    break
            self.chat_grps[index] = [me, peer]
            self.members[peer] = S_TALKING
            self.grp_ever += 1
        self.members[me] = S_TALKING

    #implement                
    def disconnect(self, me):
        # find myself in the group, quit
        in_group, group_key = self.find_group(me)
        if len(self.chat_grps[group_key]) > 2:
            self.members[me] = S_ALONE
            self.chat_grps[group_key].remove(me)
        else:
            for people in self.chat_grps[group_key]:
                self.members[people] = S_ALONE
            self.grp_ever -= 1
            del self.chat_grps[group_key]

        
    def list_all(self):
        # a simple minded implementation
        full_list = "Users: ------------" + "\n"
        full_list += str(self.members) + "\n"
        full_list += "Groups: -----------" + "\n"
        full_list += str(self.chat_grps) + "\n"
        return full_list

    #implement
    def list_me(self, me):
        # return a list, "me" followed by other peers in my group
        my_list = [me]
        in_group, group_key = self.find_group(me)
        for people in self.chat_grps[group_key]:
            if people != me:
                my_list.append(people)
        return my_list

if __name__ == "__main__":
    g = Group()
    g.join('a')
    g.join('b')
    g.join('c')
    g.join('d')
    g.join('e')
    print(g.list_all())
        
    g.connect('a', 'b')
    g.connect('c', 'd')
    print(g.list_all())
    
    print(g.list_me('d'))
    print(g.list_all())
    
    g.leave('a')
    print(g.list_all())

    g.connect('b', 'e')
    print(g.list_all())