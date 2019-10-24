# TODO req4u: test non-unique keys

from btree import *

'''
description : 
- creates a tree 

args : 
- n : int, size of tree to be created
- d : int, degree of tree to be created 

return : 
- BTree
- list, values inserts into BTree
'''
def set_up(n, d, uniqueKeys = True): 

    assert d <= n, "degree of tree cannot be more than size!"

    X = [random.randrange(10000) for i in range(n)]

    if uniqueKeys: 
        X = list(set(X))

    print("tree of {} elements, degree {}".format(len(X), d)) 

    bt = BTree(d)

    for x in X: 
        bt.insert_one(x)

    random.shuffle(X)

    return bt, X 


## some basic tests : no deletion or insertion 
#--------------------------------------------------------

def test_is_leaf(): 

    B = BTree(4)

    r = BNode(4)
    r.data.append(566)
    r.data.append(899) 
    B.root = r

    assert B.is_leaf(B.root) is True, "Root is leaf!" 


'''
description : 
- method `check_height` is correct, checks leaves for satisfaction of height prop.
'''
def test_leaf_height(): 

    bt, X = set_up(random.randrange(500, 1500),\
        random.randrange(5, 20)) 

    assert bt.check_height() is True, "Leaves are not of same height!" 

'''
description : 
- method `check_tree_flow` is correct, checks that nodes satisfy flow property 
'''
def test_node_flow(): 

    bt, X = set_up(random.randrange(500, 1500),\
        random.randrange(5, 20)) 

    assert bt.check_tree_flow() is True, "There is an underflow or overflow!"


'''
description : 
- 
'''
def test_find_key(): 


    bt, X = set_up(random.randrange(500, 1500),\
        random.randrange(5, 20)) 

    # @<-->
    not0 = None 
    not1 = None 
    not3 = None 

    while not0 is None:
        not0 = random.randrange(0, 10000) 

        if not0 not in X:
            break 
        else: 
            not0 = None 

    while not1 is None:
        not1 = random.randrange(0, 10000) 

        if not1 not in X:
            break 
        else: 
            not1 = None 

    while not3 is None:
        not3 = random.randrange(0, 10000) 

        if not3 not in X:
            break 
        else: 
            not3 = None 
  
    toFind = [not0, not1, random.choice(X), not3, random.choice(X), random.choice(X)] 

    assert bt.find_key(toFind[0]) is False, "key {} does not exist!".format(toFind[0])
    assert bt.find_key(toFind[1]) is False, "key {} does not exist!".format(toFind[1])
    assert bt.find_key(toFind[2]) is not False, "key {} exists!".format(toFind[2])
    assert bt.find_key(toFind[3]) is False, "key {} does not exist!".format(toFind[3])
    assert bt.find_key(toFind[4]) is not False, "key {} exists!".format(toFind[2])
    assert bt.find_key(toFind[5]) is not False, "key {} exists!".format(toFind[2])


## testing insertion, deletion
#-------------------------------------------------------------------------

'''
description : 
- given some arbitrary tree, deletes arbitrary and checks it for 
  correct size and key content
'''
def test_deletion(): 

    bt, X = set_up(random.randrange(500, 1500),\
        random.randrange(5, 20)) 

    for x in X: 

        n = bt.find_key(x) 

        if n: 
            q0 = bt.linearize()
            sz0 = bt.get_size()
            bt.delete_it(x, log = True)            
            sz1 = bt.get_size()
            q1 = bt.linearize()
            """
            print("--------------------------------")
            print("\nsize before :\t", bt.get_size())
            bt.delete_it(x)            
            print("size after :\t", bt.get_size())
            print("--------------------------------")
            """

            # check size
            if abs(sz1 - sz0) != 1: 
                print("ERROR AT :\t", x) 
                print("PUBLISHING REPORT") 

                fp = os.getcwd() + "/reports/error_{}".format(str(x))
                f = open(fp, 'w') 

                BTree.report_deletion_error(fp, bt)
                raise ValueError("Deletion does not produce tree with correct size!")

            # check contents 
            q0.pop(q0.index(x)) 
            assert q0 == q1, "Deletion does not produce correct contents!"

'''
description : 
- given some arbitrary tree, checks it for correct size and key content 
'''
def test_insertion(): 

    bt, X = set_up(random.randrange(500, 1500),\
        random.randrange(5, 20)) 

    X = sorted(X) 

    # check for sorted and of equal to original 
    assert X == bt.linearize(), "inserted elements not equal to actual sorted!"

'''
description : 
- runs 20000 random insertion and deletion operations and checks for size and contents 
- deletion to insertion ratio is set at some P < 0.5 
''' 
def test_deletion_insertion():

    bt = BTree(random.randrange(5, 20)) 
    P = random.randrange(0, 500) / 1000 
    # 20000 random operations

 

    for _ in range(20000): 

        # deletion 
        if random.random() < P:  

            if bt.get_size() == 0: 
                print("passing deletion : 0-tree") 
                continue

            q0 = bt.linearize() 
            c = random.choice(q0) 

            bt.delete_it(c, log = False)

            q1 = bt.linearize() 

            q0.pop(q0.index(c)) 

            assert q0 == q1, "Deletion does not produce correct contents!"

        else: 

            q0 = bt.linearize()
            c = random.randrange(0, 10000)  
 
            bt.insert_one(c) 

            q1 = bt.linearize() 

            q0.append(c) 
            q0 = sorted(q0) 

            assert q0 == q1, "Insertion does not produce correct contents!"
