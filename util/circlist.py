class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class CircularLinkedList:
    def __init__(self):
        self.current = None
        self.first = None
        self.count = 0

    def clear(self):
        self.current = None
        self.count = 0

    def is_empty(self):
        return self.current is None

    def add_element(self, data):
        new_node = Node(data)

        # If the list is empty, make the new node the head and point to itself
        if self.is_empty():
            new_node.next = new_node
            new_node.prev = new_node
            self.first = new_node
        # elif self.count == 1:
            # # 
            # scurr = self.current
            
            # new_node.next = scurr
            # new_node.prev = scurr
            
        else:
            # Traverse to the last node and update its 'next' to the new node
            scurr = self.current
            snext = self.current.next
            
            new_node.next = snext
            new_node.prev = scurr
            
            snext.prev = new_node
            scurr.next = new_node

        self.count += 1
        self.current = new_node

    #
    # removes the element at 'inc' steps away from the 
    # current pointer, then points to the 'next' element
    # after this element is removed, and returns the value
    # of the removed element
    #
    def remove_from_current(self, inc):
        # If the list is empty, make the new node the head and point to itself
        # print("inc: ", inc, " c->data: ", self.current.data)
        if inc > 0:
            for i in range(inc):
                self.current = self.current.next
            # Traverse to the last node and update its 'next' to the new node
        elif inc < 0:
            for i in range(-inc):
                self.current = self.current.prev
                #print("i: ", i, " c->data: ", self.current.data)
        value = self.current.data
        N = self.current.next
        P = self.current.prev
        N.prev = P
        P.next = N
        self.current = N
        # print("inc: ", inc, " c->data: ", self.current.data)
        return value

    #
    # inserts element with value (value) inc steps to the 'right'
    # NOTE: self.current is pointing to the 'previous' element
    # NOTE: if inc < 0 traverse in opposite direction (.prev)
    def insert_element(self, value, inc):
            
        # new_node = Node(value)
        # If the list is empty, make the new node the head and point to itself
        if inc > 0:
            for i in range(inc):
                self.current = self.current.next
            # Traverse to the last node and update its 'next' to the new node
        elif inc < 0:
            for i in range(-inc):
                self.current = self.current.prev
        self.add_element(value)

    def remove_element(self, key):
        if self.is_empty():
            print("List is empty. Cannot remove element.")
            return

        current_node = self.current
        prev_node = None

        # Search for the key to remove
        while True:
            if current_node.data == key:
                if prev_node:
                    prev_node.next = current_node.next
                else:
                    # If the head is the key, update the head
                    last_node = self.current
                    while last_node.next != self.current:
                        last_node = last_node.next
                    last_node.next = current_node.next
                    self.current = current_node.next

                # If there's only one element, set head to None
                if self.current == current_node.next:
                    self.current = None

                #print(f"Element {key} removed from the list.")
                self.count -= 1
                break

            prev_node = current_node
            current_node = current_node.next

            # If we reach the head again, the key is not in the list
            if current_node == self.current:
                print(f"Element {key} not found in the list.")
                break


    def remove_next(self, this_node):
        if self.is_empty():
            print("List is empty. Cannot remove element.")
            return

        remove_node = this_node.next
        key = remove_node.data
        
        if remove_node == self.current:
            self.current = self.current.next

        # remove element (next_node)
        
        this_node.next = remove_node.next

        self.count -= 1
        #print(f"Element {key} removed from the list.")
        return this_node.next
        
    def remove_across(self, this_node):
        save_node = this_node
        #print(f"Current element {this_node.data}.")
        if self.is_empty():
            print("List is empty. Cannot remove element.")
            return
        remove_node = this_node
        #
        # we are going to seek for the self.count/2 th element
        for i in range(self.count//2 - 1):
            remove_node = remove_node.next
        this_node = remove_node
        remove_node = remove_node.next
        key = remove_node.data
        
        if remove_node == self.current:
            self.current = self.current.next

        # remove element (next_node)
        
        this_node.next = remove_node.next

        self.count -= 1
        #print(f"Element atfer {this_node.data},  {key} removed from the list.")
        return save_node.next

    def random(self):
        n = random.randint(1, self.count)
        el = self.current
        for i in range(n):
            el = el.next
        return el

    def display_list(self, Arrows = True):
        if self.is_empty():
            print("List is empty.")
            return
        start = self.first
        current_node = start
        n = 0
        while n < self.count:
            n += 1
            if Arrows:
                print(current_node.data, end=" -> ")
            else:
                if current_node == self.current:
                    print("(", current_node.data, end=") ")
                else:
                    print(current_node.data, end=" ")
            current_node = current_node.next
            #current_node = current_node.prev

            # If we reach the where we started, break the loop
            if current_node == start:
                break
        if Arrows: print(" (head)")
        else: print()
