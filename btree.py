import random
import copy 

import os 
import pickle

random.seed(195) 


class BNode:

    def __init__(self, degree): 

        self.data, self.next = [], []

        self.parent = None 

        # for b+ tree
        self.sibNext = None 
        self.sibPrev = None


from collections import OrderedDict

class BTree: 

    def __init__(self, degree): 

        self.root = None 
        self.degree = degree 

        self.size = 0 

        self.deletionLog = [] # used in the case of errors 

    '''
    description: 
    - determines if node is leaf 
    
    return : 
    - bool 
    '''
    def is_leaf(self, node):

        if len(node.next) == 0: 
            return True 
        return False

    '''

    description : 
    - determines if node with data size `nodeDataLen` is underflow 

    return : 
    - bool 
    '''
    def is_underflow(self, nodeDataLen:int):
        
        if nodeDataLen < (self.degree) // 2: 
            return True 
        return False   

    '''
    description : 
    - determines if `node` has underflow

    return : 
    - bool  
    '''
    def is_overflow(self, node:BNode):
        if len(node.data) >= self.degree:
            return True
        return False

    '''
    description : 
    - inserts one `value` into the proper position in leaf `n`'s data 

    return :
    - int, index where value was inserted into leaf's data 
    '''
    def ordered_insert(self, n, value): 

        for i, x in enumerate(n.data): 
            if x >= value:
                n.data.insert(i, value) 
                return i 

        n.data.append(value)
        return len(n.data) - 1

    '''
    description : 
    - helper for method `insert_one` 

    
    '''
    def insert_one_(self, value): 

        n = self.root

        while not self.is_leaf(n): 

            moved = False 
            for i, x in enumerate(n.data): 
                if x >= value: 
                
                    moved = True 
                    n = n.next[i] 
                    break

            if not moved: 
                n = n.next[i + 1]
 
        self.ordered_insert(n, value)
        return n   
    
    '''
    description : 
    - inserts one `value` into tree 

    args : 
    - value : int or float 

    return : 
    - 
    '''
    def insert_one(self, value): 
        if self.root is None: 

            self.root = BNode(self.degree) 
            self.root.data.append(value) 
        else: 
            node= self.insert_one_(value)

            self.check_overflow(node) 


    '''
    description : 
    - checks for overflow at some node `n`, will rebalance and recurse if needed 

    return : 
    - 
    '''
    def check_overflow(self, n):

        if not self.is_overflow(n):  
            return 

        median = len(n.data) // 2
        medianVal = n.data[median]                    

        left = BNode(self.degree)     
        right = BNode(self.degree)

        # add data to left and right 
        for i, x in enumerate(n.data[:median]): 
            left.data.append(x)     

        for i, x in enumerate(n.data[median + 1:]): 
            right.data.append(x)

        # add children to left and right if n is not a leaf 
        if not self.is_leaf(n):
            for i, x in enumerate(n.next[:median + 1]):
                left.next.append(x) 
                x.parent = left 

            for i, x in enumerate(n.next[median + 1:]):
                right.next.append(x) 
                x.parent = right

        # push median up 
            # find position of median
        p = n.parent 

        # parent is None --> root 
        if p is None:
            self.root = BNode(self.degree) 
            self.root.data.append(medianVal) 

            self.root.next.append(left)
            self.root.next.append(right) 

            left.parent, right.parent = self.root, self.root
        else: 
            index = self.ordered_insert(p, medianVal) 
            
            # add left and right as children
            p.next[index] = left             
            p.next.insert(index + 1, right)
            left.parent, right.parent = p, p
            self.check_overflow(p) 
    
    '''
    description : 
    - displays node keys at n and recurses downward 

    return : 
    - 
    '''
    def display_data_(self, n): 
        
        if n is not None: 

            if not self.is_leaf(n): 
                for i in range(len(n.data)): 
                    self.display_data_(n.next[i])
                    print("value :\t", n.data[i])
                self.display_data_(n.next[i + 1])
            
            else: 
                for i in range(len(n.data)): 
                    print("value :\t", n.data[i])

    '''
    description : 
    - see method `display_data_` 
    '''
    def display_data(self): 
        self.display_data_(self.root)

    '''
    description : 
    - adds node `n`'s keys to cache and recurses downward

    return :
    - 
    '''
    def linearize_(self, n, cache):

        if n is None: return [] 

        if self.is_leaf(n):
            cache.extend(n.data)
        else: 
            for i, x in enumerate(n.data): 
                self.linearize_(n.next[i], cache)
                cache.append(x) 
            self.linearize_(n.next[i + 1], cache)

    '''
    description : 
    - see above 

    return : 
    - list, all values from BTree 
    '''
    def linearize(self): 
        cache = [] 
        self.linearize_(self.root, cache) 
        return cache


    '''
    description : 
    - determines if key `x` is duplicate in BTree `bt` 
    
    return : 
    - bool 
    '''
    # TODO 
    @staticmethod
    def is_duplicate(bt, x): 

        l = bt.linearize() 
        c = 0 

        for i in l: 
            if i == x:
                c += 1 

        if c > 1: return True 
        return False 

    '''
    description : 
    - adds size of node `n`'s data and recurses downward

    return : 
    - 
    '''
    def get_size_(self, n):

        if n == None: return  

        if self.is_leaf(n):
            self.size += len(n.data)

        else:
            for i, x in enumerate(n.data): 
                self.get_size_(n.next[i])
                self.size += 1
                ##cache.append(x) 
            self.get_size_(n.next[-1])
            ##self.linearize_(n.next[i + 1], cache)

    
    '''
    description : 
    - ~

    return : 
    - int, the size 
    '''
    def get_size(self): 
        self.size = 0 
        self.get_size_(self.root)
        return self.size 

    '''
    description : 
    - returns the first occurrence of key `value` 

    return : 
    - BNode, node containing value 
    '''     
    def find_key(self, value): 

        n = self.root 
        found = False 
        while not self.is_leaf(n): 

            moved = False
             
            for i, x in enumerate(n.data):

                if x > value: 
                
                    moved = True 
                    n = n.next[i] 
                    break
                elif x == value: 
                    moved = True ##
                    found = True ##
                    return n 

            if not moved:
                n = n.next[i + 1]
               

        if value in n.data: 
            return n 
        return False

    '''
    description : 
    - for non-root node `n`, determines its position as child to parent 

    return : 
    - int
    '''
    def get_child_index(self, n): 

        if not n.parent: return False 

        p = n.parent 

        for i, x in enumerate(p.next):
            if x == n: 
                return i 

        return False 


    ## used for checking node properties 
    #--------------------------------------------------------

    '''
    description : 
    - determines if node satisfies child-size prop. and data size prop 

    return : 
    - bool 
    '''
    def check_flow_(self, n): 

        if n != self.root and self.is_underflow(len(n.data)): 
            return False 

        if self.is_overflow(n): 
            return False

        if len(n.next) != len(n.data) + 1: 
            return False 

        return True  

    '''
    description : 
    - determines if node satisfies BTree properties and recurses downward

    return : 
    - True if good 
    - else `BNode` of issue 
    '''
    def check_tree_flow_(self, n):

        if n is not None:
            if not self.check_flow_(n): 
                return n 

            if not self.is_leaf(n): 
                for i in range(len(n.data)): 
                    self.check_tree_flow_(n.next[i])

                self.check_tree_flow_(n.next[i + 1])
        return True

    '''
    description : 
    - see above 

    return : 
    - see above 
    '''
    def check_tree_flow(self):
        return self.check_tree_flow_(self.root)


    '''
    description : 
    - returns height from node `root` to some value `v`

    return : 
    - int 
    '''
    def get_height(self, v): 

        n = self.root

        h = 0 

        while not self.is_leaf(n): 

            found = False 
            for i, x in enumerate(n.data): 
                if v < x: 
                    n = n.next[i]
                    found = True 
                    break 

            if not found: 
                n = n.next[i +  1] 
            h += 1

        if v not in n.data: 
            return False 
        return h  

    '''
    description : 
    - determines if all leaves are of same height 

    return : 
    - bool, if all leaves of same height 
    '''
    # TODO 
    def check_height(self): 

        q = self.linearize()

        H = [] 

        for q_ in q: 

            if self.is_leaf(self.find_key(q_)): 

                H.append(self.get_height(q_)) 
                
                if len(list(set(H))) != 1:
                    return False 

        return True 

    ## methods used for deletion 
    #----------------------------------------------
    '''
    description : 
    - solves underflow node `n` by borrowing from rich sibling 

    return :
    boolean, if rich sibling exists 
    '''
    def solve_by_rich_sibling(self, n): 

        # can't be root 
        if not n.parent: 
            return False

        ci = self.get_child_index(n)

        # look at left 
        if ci > 0: 
            left = n.parent.next[ci - 1]

            # rich 
            if not self.is_underflow(len(left.data) - 1):

                # add parent key 
                pk = n.parent.data[ci - 1]
                n.data.insert(0, pk)

                # replace parent key 
                n.parent.data[ci - 1] = left.data.pop(-1)

                # insert sibling children if exists
                if not self.is_leaf(left):
                    cc = left.next.pop(-1) 
                    cc.parent = n 

                    n.next.insert(0, cc) 
                return True

        # look at right 
        if ci < len(n.parent.next)  - 1:

            right = n.parent.next[ci + 1]

            # rich 
            if not self.is_underflow(len(right.data) - 1):

                # add parent key 
                pk = n.parent.data[ci]
                n.data.append(pk)

                # replace parent key 
                n.parent.data[ci] = right.data.pop(0)
            
                # insert sibling children if exists
                if not self.is_leaf(right):
                    cc = right.next.pop(0) 
                    cc.parent = n 
                    n.next.append(cc) 

                return True 
        return False 


    '''
    description : 
    - merges a poor sibling with underflow node n 

    return : 
    - 
    '''
    def solve_by_poor_sibling(self, n): 

        """
        description : 
        - merges either poor left sibling or right sibling depending on direction
          `d`

        args : 
        - ci : int, child index of underflow node
        - d : str, direction of poor sibling

        return : 
        -   
        """
        def helper(ci, d:str):

            # obsolete 
            """
            if  len(n.parent.next) != len(n.parent.data) + 1: 
                print('WARNING : parent does not have enough children') 

            if len(n.parent.data) == 0: 
                print("WARNING : parent has 0 children")
            """ 

 
            if d == 'right': 
                # remove sibling

                # TODO delete 
                ## used for checking
                try:  
                    s = n.parent.next.pop(ci + 1) #
                except: 
                    print("NODE :\t", n.data) 
                    print("PARENT NODE :\t", n.parent.data) 
                    print("PARENT NEXT :\t") 
                    for x in n.parent.next: 
                        print("*\t", x.data) 

                    n.parent = n 
                    return 1

                # remove parent key 
                pk = n.parent.data.pop(ci) #

                # add parent key and sibling data 
                n.data.append(pk) #
                n.data.extend(s.data) #
     
                # add sibling children 
                for d in s.next:
                    d.parent = n 
                    n.next.append(d) #

            else: 
                # remove sibling 
                s = n.parent.next.pop(ci - 1) #

                # remove parent key 
                pk = n.parent.data.pop(ci - 1) #

                # add parent key and sibling data 
                n.data.insert(0, pk) #
                for d in s.data[::-1]: n.data.insert(0, d) #
     
                # add sibling children 
                for d in s.next[::-1]: 
                    d.parent = n 
                    n.next.insert(0, d) #
    
        # cases : n is leftmost, n is rightmost, n is in the middle 
        if not n.parent: 
            return False

        ci = self.get_child_index(n)

        # right sibling 
        if ci == 0: 
            helper(ci, 'right') 

        # left sibling 
        elif ci == len(n.parent.next) - 1: 
            helper(ci, 'left') 
 
        # random 
        else: 
            d = 'left' if random.random() > 0.5 else 'right' 
            helper(ci, d) 

    '''
    description : 
    - rebalances node `n` if underflow

    return : 
    - 
    '''
    def rebalance(self, n, log):  

        # used for debugging
        if log:  
            self.deletionLog.append((copy.deepcopy(self), copy.deepcopy(n)))

        # if root and empty, make child the root
        if n == self.root: 
            if n.data == []: 
                self.root = self.root.next[0] 
                self.root.parent = None

        # if underflow, rebalance and recurse 
        elif self.is_underflow(len(n.data)):

            if not self.solve_by_rich_sibling(n): 
                self.solve_by_poor_sibling(n)
 
            self.rebalance(n.parent, log) 

    '''
    description : 
    - helper method for deletion, used for leaves 

    args : 
    - n : BNode, contains value v 
    - v : int or float
    '''
    def delete_at_leaf(self, n, v, log): 
        i = n.data.index(v) 
        
        # case : n is root, just delete 
        if n == self.root:
            self.root.data.pop(i) 
            return 

        # n is not root
        # if underflow, have to rebalance
        n.data.pop(i)
        self.rebalance(n, log)

    '''
    description : 
    - helper method for deletion, used for non-leaves.
    - finds replacement in leaf for `v` in `n` 

    args : 
    - n : BNode, contains value v 
    - v : int or float
    '''
    def get_replacement(self, n, v): 

        if self.is_leaf(n): 
            return False, False 

        index = n.data.index(v)

        d = 'left' if random.random() > 0.5 else 'right' 

        if d == 'right': 
            right = n.next[index + 1]

            while not self.is_leaf(right):
                right = right.next[0]

            x = right.data.pop(0) 
            return right, x 

        else: 

            left = n.next[index]

            while not self.is_leaf(left):
                left = left.next[-1]

            x = left.data.pop(-1) 
            return left, x   

    '''
    description : 
    - deletes value `v` from tree and rebalances if needed 

    return : 
    None 
    '''
    def delete_it(self, v, log = False): 

        fp = os.getcwd() + "/reports/error_{}".format(str(v)) 

        n = self.find_key(v)

        if log: 
            self.deletionLog = [] 
 
        if n:

            if self.is_leaf(n): 
                self.delete_at_leaf(n, v, log)
            else: 
                rep, x = self.get_replacement(n, v)

                # TODO : delete cond. 
                if rep is not False: 
                    n.data[n.data.index(v)] = x 
                    self.rebalance(rep, log) 
                else: 
                    print("ERROR : could not find replacement for leaf!") 


        else: 
            print("value {} could not be found".format(v))

    '''
    description : 
    - misnomer, `next` is a list of nodes 
    - stringizes data of the list of nodes 

    return : 
    - str
    '''
    @staticmethod
    def str_next(next):  
        l = "" 

        for x in next: 
            l += str(x.data) 
            l += "  ,"

        return l 
        

    ## used fo
    #------------------------------------------------------------
    '''
    description : 
    - logs relevant information of BTree `b` at node `n` 

    args : 
    - fp : str, filepath to log info,
               file must exist and be able to be used in `a` mode 
    - b : BTree 
    - n : node 
    '''
    @staticmethod
    def report_node(fp, b, n): 

        with open(fp, 'a') as f: 


            # get node data 
            f.write("total size :\t" + str(b.get_size())) 
            f.write("\nnode data :\t" + str(n.data) + "\n")  
            f.write("\nnode next :\n\t" + BTree.str_next(n.next) + "\n")  


            q = [] 
            if n.parent: 
                f.write("\nparent data :\t" + str(n.parent.data) + "\n")  
                f.write("\nparent next :\t" + BTree.str_next(n.parent.next) + "\n")

                # TODO (maybe) 
                # write sibling next here  

                if n.parent.parent: 
                    f.write("\ngrandparent data :\t" + str(n.parent.parent.data) + "\n")  
                    f.write("\ngrandparent next :\t" + BTree.str_next(n.parent.parent.next) + "\n")

                # add parent next 
                for x in n.parent.next:
                    q.extend(x.data)

                    # add next next 
                    if x.next != []: 
                        for x_ in x.next: 
                            q.extend(x_.data)  

                # add parent data 
                q.extend(n.parent.data) 


            # TODO : note that below makes sense only if BTree has unique values
            #        purpose is to check for reference, deref. pointer errors 

            # add pertinent node data for checking 
            q.extend(n.data) 
            for x in n.next:
                q.extend(x.data)


            q = list(set(q)) 
            f.write("\npossible duplicates :\n\n") 
            for q_ in q: 
                q__ = BTree.is_duplicate(b, q_)

                if q__ > 1: 
                    f.write("*\t" + str(q_) + "\t" + str(q__) + "\n") 
            f.write("---------------------------------------------\n\n") 


    @staticmethod
    def report_deletion_error(fp, bt): 

        for (b, n) in bt.deletionLog: 
            BTree.report_node(fp, b, n) 


### TODO 
### a little interface for viewing tree
### use at discretion 
def browse_tree_at_node(bt): 

    inp = '' 
    ci = None
    n = None


    print("--------------------------------")
    print("* f find node with value")

    print('* nd node data') 
    print('* nl node data length') 
    print('* nn node next') 
 
    print('* pd parent data') 
    print('* pl parent data length') 
    print('* pn parent next') 

    print('* ld left sibling data')
    print('* ll left sibling data len')
    print('* ln left next') 

    print('* rd right sibling data')
    print('* rl right sibling data len') 
    print('* rn right next') 
    print("--------------------------------")

    while inp.lower() != 'q': 

        print('\n')
        inp = input("Enter input :\t") 

        if inp.lower() == 'f': 

            nv = int(input("Enter value :\t"))
 
            n = bt.find_key(nv) 
            if not n: 
                print("node could not be found!") 
                n = None 

            else: 
                ci = bt.get_child_index(n)


        if n is None: 
            print("please specify a node!") 
            continue
 
        if inp.lower() == 'pd': 
            if n.parent: 
                print(n.parent.data) 
            else: 
                print("NONE") 

        elif inp.lower() == 'pl': 
            if n.parent: 
                print(len(n.parent.data))  
            else: 
                print("NONE") 

        elif inp.lower() == 'pn': 
            if n.parent:
                for x in n.parent.next: 
                    print(x.data)  

            else: 
                print("NONE")

        elif inp.lower() == 'nd': 
            print(n.data)  

        elif inp.lower() == 'nl': 
            print(len(n.data))

        elif inp.lower() == 'nn': 
            for x in n.next: 
                print(x.data)

        elif inp.lower() == 'ld':
            if ci is not False: 
                if ci > 0:
                    print(n.parent.next[ci - 1].data)  
                    continue

            print('NONE') 

           
        elif inp.lower() == 'll': 
            if ci is not False: 
                if ci > 0: 
                    print(len(n.parent.next[ci - 1].data))  
                    continue
            print('NONE')

        elif inp.lower() == 'ln':
            if ci is not False:  
                if ci > 0:              
                    for x in n.parent.next[ci - 1].next: 
                        print(x.data)  
                    continue

            print('NONE') 

        elif inp.lower() == 'rd': 
            if ci is not False:  
                if ci < len(n.parent.next) - 1: 
                    print(n.parent.next[ci + 1].data)  
                    continue
            print('NONE') 

        elif inp.lower() == 'rl': 
            if ci is not False:  
                if ci < len(n.parent.next) - 1: 
                    print(len(n.parent.next[ci + 1].data))  
                    continue
            print('NONE') 


        elif inp.lower() == 'rn': 
            if ci is not False:  
                if ci < len(n.parent.next) - 1: 
                    for x in n.parent.next[ci + 1].next: 
                        print(x.data)
                    continue
            print('NONE')

    

       
    



