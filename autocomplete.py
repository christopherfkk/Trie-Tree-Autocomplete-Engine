class Node:
    """This class represents one node of a trie tree
    
    Parameters
    ----------
    self.char --> str
        the character it stores, i.e. one character per node
    self.valid --> bool
        True if the character is the end of a valid word
    self.parent --> Node
        the parent node, i.e. each node only has one parent, None if root node
    self.children --> list of Node
        a list of children nodes, i.e. each node can have multiple children, empty if leaf node
        
    Methods
    -------
    get_child(self, char)
        returns the child corresponding to the input char if present, otherwise return False.
    sorted_children(self)
        Returns the children of a node but sorted by in alphabetical order
    """

    def __init__(self, char):
        """Creates the Node instance.
        
        Parameters
        ----------
        char : str
            The character the node represents
        """
        self.char = char 
        self.valid = False
        self.parent = None
        self.children = []
        self.occurrence = 0 # new attribute to store occurrence when building the trie
        
    def __repr__(self):
        """Overrides the defauly print implementation."""
        return f"\n\t Node {self.char}"
    
    def __eq__(self, other):
        """Overrides the default equality implementation."""
        if isinstance(other, Node):
            return self.char == other.char
        if isinstance(other, str):
            return self.char == other
        return False
    
    def get_child(self, char):
        """Returns the child corresponding to the input char if present in 
        the node's list of children. Otherwise returns False.
        
        Parameters
        ----------
        char : str
            The character to be checked in the node's children
        """        
        for child in self.children:
            if child == char: # this is made possible by __eq__()
                return child
        return False
    
    # new method
    def sorted_children(self):
        """Returns the children of a node but sorted by in alphabetical order.
        
        Returns
        ----------
        sorted_children : list of Nodes
            the sorted children of a node
        """   
        # if a node doesn't have children, return empty list
        if not self.children:
            return []
        
        # else sort the children with key as node.char
        sorted_children = sorted(self.children, key=lambda x: x.char)
        
        return sorted_children
        
class Trie:
    """This class represents the entirety of a trie tree.
    
    Parameters
    ----------
    self.root --> Node
        the root node with an empty string
    self.word_list --> list
        the input list of words converted into lower-case
    self.tree --> None
        calls the create_trie() method so the trie is intialized upon instantiation
    
    Methods
    -------
    create_trie(self, word_list)
        Calls the insert() method for each word in word_list
    insert(self, word)
        Inserts a word into the trie, creating nodes as required.
    lookup(self, word)
        Determines whether a given word is present in the trie.
    peek_occurrence(self, word)
        Determines the occurrence of given word.
    k_most_common(self, k):
        Finds k words inserted into the trie most often.
    
    """
    
    def __init__(self, word_list = None):
        """Creates the Trie instance, inserts initial words if provided.
        
        Parameters
        ----------
        word_list : list
            List of strings to be inserted into the trie upon creation.
        """
        self.root = Node("")
        self.word_list = [word.lower() for word in word_list]
        self.tree = self.create_trie()
    
    def __repr__(self):
        """Overrides the defauly print implementation."""
        return f"This trie has root: \n{self.root}"
    
    def create_trie(self):
        """Inserts all words from the input wordbank into the trie by calling self.insert()"""
        for word in self.word_list:
            self.insert(word)
    
    def insert(self, word):
        """Inserts a word into the trie, creating missing nodes on the go.
        
        Parameters
        ----------
        word : str
            The word to be inserted into the trie.
        """

        # iterate through each character of the word
        current_node = self.root
        
        for i in range(len(word)): 
            
            # check if a child with the new character already exists
            new_char = word[i]
            child = current_node.get_child(new_char) 
            
            # if child doesn't exist, create new node instance
            if child == False:
                new_node = Node(new_char) 
                new_node.parent = current_node # update parent attribute
                current_node.children.append(new_node) # update children attribute
                current_node = new_node
            
            # if child exists, continue
            else:
                current_node = child
        
        # the last char of the word means it is a valid word
        current_node.valid = True
        # new line: records the occurrences of the word
        current_node.occurrence += 1
    
    def lookup(self, word):
        """Determines whether a given word is present in the trie.
        
        Parameters
        ----------
        word : str
            The word to be looked-up in the trie.
            
        Returns
        -------
        bool
            True if the word is present in trie; False otherwise.
            
        Notes
        -----
        Your trie should ignore whether a word is capitalized.
        E.g. trie.insert('Prague') should lead to trie.lookup('prague') = True
        """
        # convert to lower-case, remove white spaces, replace in-word white spaces with hyphens
        word = word.lower().strip().replace(" ", "-")
        
        current_node = self.root
        
        for i in range(len(word)):    
            
            # goes down the trie by iteratively checking if a child exist
            child = current_node.get_child(word[i])
            if child != False:
                current_node = child
                
            # if a child doesn't exist, immediately return False
            if child == False:
                return False
        
        # return if the last character of the word is a valid word
        return current_node.valid
    
    # new method
    def alphabetical_list(self):
        """Delivers the content of the trie in alphabetical order.
        
        Returns
        ----------
        list
            List of strings, all words from the trie in alphabetical order.
        """
        if not self.root:
            return []
        if not self.root.children:
            return []
        
        return self._alphabetical_list(self.root)
    
    # new inner method
    def _alphabetical_list(self, root):
        """Inner function to above. Recursively appends the child char to the parent.
        
        Parameters
        ----------
        root
            The root of a trie tree, possibly an internal node for a sub trie tree
            
        Note: having a root parameter is helpful for recursing through the trie by considering
        a child node has the root of a sub trie.
        """
        
        lst = [] # initialize empty list
        
        # if the root has children
        if root.children:
            children = root.sorted_children() # sort the children list
            
            for child in children:
                
                    # for each string accumulated from the bottom-up
                    for string in self._alphabetical_list(child):
                        
                        # this statement appends valid words that don't end at a leaf
                        if child.valid and child.children and child.char not in lst:
                            lst.append(child.char)
                            
                        # concatenate the child's character to the accumulated string 
                        lst.append(child.char + string)
                        
        
        # base case: if root (leaf) has no children
        else:
            lst.append('')
            
        return lst
    
    # new method
    def peek_occurrence(self, word):
        """Determines the occurrence of given word.
        
        Parameters
        ----------
        word : str
            The word to be peeked in the trie.
            
        Returns
        -------
        int / bool
            Returns the occurrence of the word. If word is not valid, return False
            
        Note: this is very similar to the lookup() method but instead of checking
        self.valid it checks self.occurrence.
    
        """
        current_node = self.root
        
        for i in range(len(word)):    
            
            child = current_node.get_child(word[i])
            if child != False:
                current_node = child
        
        if current_node.valid:
            return current_node.occurrence
        
        return False
    
    def k_most_common(self, k):
        """Finds k words inserted into the trie most often.

        Parameters
        ----------
        k : int
            Number of most common words to be returned.

        Returns
        ----------
        list
            List of tuples.
            
            Each tuple entry consists of the word and its frequency.
            The entries are sorted by frequency.

        Example
        -------
        >>> print(trie.k_most_common(3))
        [(‘the’, 154), (‘a’, 122), (‘i’, 122)]
        
        I.e. the word ‘the’ has appeared 154 times in the inserted text.
        The second and third most common words both appeared 122 times.
        """
        if k <= 0 or int(k) != k:
            return "ERROR: k must be a positive integer"
        
        common_words = [] # initialize empty list
        unique_words = self.alphabetical_list() # find all unique words
        
        if not unique_words:
            return "ERROR: no valid words to find the k most common words"
        
        # peek the occurrence of the word and stores in a tuple
        for word in unique_words:
            common_words.append((word, self.peek_occurrence(word)))
        
        # sort all words and their occurrences
        common_words.sort(key=lambda x: x[1], reverse = True)
        
        # if k is way too large
        if k > len(unique_words):
            print(f"NOTE: wordbank has {len(unique_words)} < {k} unique words!!")
            return common_words
        
        # returns the first k words with most occurrences
        return common_words[:k]
    
    # new method
    def most_common(self, node, prefix):
        """Finds the most common word with the given prefix.

        You might want to reuse some functionality or ideas from Q4.

        Parameters
        ----------
        node: Node
            the last node (char) of the prefix
        prefix : str
            The word part to be “autocompleted”.

        Returns
        ----------
        str
            The complete, most common word with the given prefix.

        """
        common_words = [] # initalize empty list
        unique_words = [prefix + word for word in self._alphabetical_list(node)] # find all unique words with the prefix
        
        if not node:
            return "ERROR: no valid words with this prefix"
        
        # if the prefix is a valid word itself
        if node.valid:
            unique_words.append(prefix)
        
        # if there are no unique words with this prefix
        if not unique_words:
            return "ERROR: no valid words with this prefix"
        
        # append the word and its occurrence for each unique word
        for word in unique_words:
            common_words.append((word, self.peek_occurrence(word)))
        
        # sort them by occurrences
        common_words.sort(key=lambda x: x[1], reverse = True)
        
        # return the first element of the first tuple, i.e. the string of the most common word
        return common_words[0][0]
     
     
    # new method
    def autocomplete(self, prefix):
        """Finds the most common word with the given prefix.

        You might want to reuse some functionality or ideas from Q4.

        Parameters
        ----------
        prefix : str
            The word part to be “autocompleted”.

        Returns
        ----------
        str
            The complete, most common word with the given prefix.
            
        Notes
        ----------
        The return value is equal to prefix if there is no valid word in the trie.
        The return value is also equal to prefix if prefix is the most common word.
        """
        # convert to lower-case
        prefix = prefix.lower()
        
        # traverse down the tree to the last char of the prefix
        current_node = self.root
        for i in range(len(prefix)):    
            current_node = current_node.get_child(prefix[i])
            if current_node == False:
                return "ERROR: prefix does not exist in trie"
        
        # find the most common words with the alphabetical list from this last char
        return self.most_common(current_node, prefix)
