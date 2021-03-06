# -*- coding: utf-8 -*-
"""
  utils.alg
  ~~~~~~~~~~~
  syntacitc algs

@author wenlong
"""
import inspect

from nltk import Tree

from nltk.tokenize import StanfordTokenizer

# use the wrapper or use the standard lib?
from nltk.parse.stanford import StanfordDependencyParser
eng_parser = StanfordDependencyParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

#from  nltk.parse.stanford import StanfordParser
#eng_parser = StanfordParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

import base

PUNCTUATION = (';', ':', ',', '.', '!', '?')
COMMA = ','

def traverse(t):
    try:
        t.label()
    except AttributeError:
        print(t + " ")
    else:
        # Now we know that t.node is defined

        #import pdb; pdb.set_trace()
        print('(', t.label())
        for child in t:
            traverse(child)
        print(')')

"""
def upper_first_char(w):
    return w[0].upper() + w[1:]
"""

def simp_coordi_sent(tokens, node_list):
    """
    tokens = StanfordTokenizer().tokenize(sent)
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']


    node_list = [] #(4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        #print(node)
        node_list.append(base.get_triples(node))

    # construct the tree
    #w = result.tree()
    #partial = Tree(w[parent].label(), )
    _subtree = {}
    for subtree in w.subtrees():
        #import pdb; pdb.set_trace()
        #traverse(subtree)
        _subtree[subtree.label()] = subtree

    """

    # Universal dependencies -- And relations
    """ depes format, based on dependency graph in NLTK
    ((head word, head tag), rel, (dep word, dep tag))
    e.g.  ((u'ate', u'VBD'), u'nsubj', (u'I', u'PRP'))
    ##### node_list
    e.g. #(4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    """
    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    #import pdb; pdb.set_trace()

    strs = ""
    for nd in node_list[1:]:
        #print(nd)
        #depes.append(row)

        #import pdb; pdb.set_trace()
        # look for the root word, and check the root word has a modifier
        """
        #if (root in nd) and ('conj' in nd[4].keys()):
            # if "conj" relation, it is modified by row[2]
            #import pdb; pdb.set_trace()
            #print "conj_node: ", nd[4]['conj']
        #    pass
            #

            lst = []
            lst.append(row[2][0])
            if row[2][0] in _subtree:
                #print "conj_node: ", _subtree[row[2][0]]
                for k in _subtree[row[2][0]]:
                    lst.append(k)
            #lst.append(row[2][0])

            lst_ = sorted(lst, key=lambda x: tokens.index(x))
            #print "conj_lst_: ", lst_
            ret.append(lst_)
        """
        if (root in nd) and ('conj' in nd[4].keys()) and ('cc' in nd[4].keys()):
              # coordination
            # Note: remove the conjunction word, and
            #       if there is words before the conjunction, we consider it as a sent,
            #       or,
            #import pdb; pdb.set_trace()

            nsubj = " "
            nsubj_ind = 0
            FLAG = 0
            #Assume the nsubj is the before word of the conj_ind
            conj_ind = nd[4]['conj'][0]
            for _nd in node_list[1:]:
                if conj_ind == _nd[0]:
                    if ('nsubj' in _nd[4].keys()) or ('nsubjpass' in _nd[4].keys()):
                        # another subj :THE ASSUME
                        nsubj_ind = conj_ind - 1
                        conj_nsubj = base.upper_first_char(tokens[nsubj_ind]) + nsubj
                        FLAG = 1 # use the subj

            # get nsubj
            #nsubj = " "
            if ('nsubj' in nd[4].keys()):
                nsubj_ind = nd[4]['nsubj'][0]
                nsubj =  base.upper_first_char(tokens[nsubj_ind]) + nsubj


            if ('nsubjpass' in nd[4].keys()):
                nsubj_ind = nd[4]['nsubjpass'][0]
                nsubj = base.upper_first_char(tokens[nsubj_ind]) + nsubj

            #print "cc_node: ", nd[4]['cc']
            cc_ind = nd[4]['cc'][0]

            # 1st str1
            # remove the conjunction word

            #import pdb; pdb.set_trace()
            tokens[cc_ind] = ''
            if tokens[cc_ind - 1] == '':# no word before the conjunction word
                pass
            elif tokens[cc_ind - 1] in PUNCTUATION:
                tokens[cc_ind - 1] = ''
                tokens[cc_ind] = '.'
            elif tokens[cc_ind + 1] in PUNCTUATION:
                tokens[cc_ind + 1] = ''
            else:# we can add ' . ' as the end of the 1st sentence
                tokens[cc_ind] = '.'

            str1 = nsubj + " ".join(tokens[(nsubj_ind+1):(cc_ind+1)])

            #NOTE: We can consider the next word after the conjunction as the first word of 2nd sentence
            # str2
            if not FLAG:
                str2 = nsubj + " ".join(tokens[(cc_ind + 1):])
            else:
                str2 = conj_nsubj + " ".join(tokens[conj_ind:])


            """
            lst = []
            lst.append(row[0][0])
            if row[0][0] in _subtree:
                #print "cc_node: ", _subtree[row[0][0]]
                for k in _subtree[row[0][0]]:
                    # remove the 'cc' modifier
                    if k == row[2][0]:
                        pass
                    else:
                        lst.append(k)
            #lst.append(row[0][0])

            lst_ = sorted(lst, key=lambda x: tokens.index(x))
            print "cc_lst_: ", lst_
            #ret.append(lst_)
            """
            strs = str1 + " " + str2
            return strs
        else:
            #print "Hello, World"
            pass

    """
    ret = []

    depes = []
    for row in result.triples():
        #print(row)
        depes.append(row)

        #import pdb; pdb.set_trace()
        # look for the root word, and check the root word has a modifier
        if (root in row[0]) and (len(row[2]) != 0) and (row[1] == 'conj'):
            # if "conj" relation, it is modified by row[2]
            #import pdb; pdb.set_trace()
            #print "conj_node: ", _subtree[row[2][0]]
            #
            lst = []
            lst.append(row[2][0])
            if row[2][0] in _subtree:
                #print "conj_node: ", _subtree[row[2][0]]
                for k in _subtree[row[2][0]]:
                    lst.append(k)
            #lst.append(row[2][0])

            lst_ = sorted(lst, key=lambda x: words.index(x))
            #print "conj_lst_: ", lst_
            ret.append(lst_)

        elif (root in row[0]) and (len(row[2] != 0)) and (row[1] == 'cc'):

            #import pdb; pdb.set_trace()
            #print "cc_node: ", _subtree[row[0][0]]
            lst = []
            lst.append(row[0][0])
            if row[0][0] in _subtree:
                #print "cc_node: ", _subtree[row[0][0]]
                for k in _subtree[row[0][0]]:
                    # remove the 'cc' modifier
                    if k == row[2][0]:
                        pass
                    else:
                        lst.append(k)
            #lst.append(row[0][0])

            lst_ = sorted(lst, key=lambda x: words.index(x))
            #print "cc_lst_: ", lst_
            ret.append(lst_)
        else:
            #print "Hello, World"
            pass

    """

    #import pdb; pdb.set_trace()

    return strs


def simp_subordi_sent(tokens, node_list):
    # C1 and C2  must have the own subject
    #PUNCT = ','
    # the subordinating conjunction
    dict1 = {   'after': 'Then',
                'although': 'But',
                'though': 'But',
                'since': 'Therefore',
                'because': 'Therefore',
                'as': 'Therefore'
            }

    dict2 = {'so': 'So',
             'before': 'Then'
            }

    """
    # the original tokens in the sent
    tokens = StanfordTokenizer().tokenize(sent)
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']
    """
    #w = result.tree()
    #print "parse_tree:", w

    #TODO: use the tree structure, check again
    """
    _tree = {} # store the _tree-> {node: children}
    #import pdb; pdb.set_trace()
    for postn in w.treepositions():
        if w.label() and len(postn) > 0:
            parent = postn[:-1]

            nd = w[parent].label() #node
            if nd in _tree:
                _tree[nd].append(w[postn])
            else:
                _tree[nd] = []
                _tree[nd].append(w[postn])

    """

    # Universal dependencies --
    """ depes format, based on dependency graph in NLTK
    ((head word, head tag), rel, (dep word, dep tag))
    e.g.  ((u'ate', u'VBD'), u'nsubj', (u'I', u'PRP'))
    """

    """
    node_list = [] # dict (4 -> 4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        #print(node)
        node_list.append(base.get_triples(node))
        #node_list[base.get_triples[0]] = base.get_triples(node)
    """

    # construct the tree
    #partial = Tree(w[parent].label(), )
    """
     # store the subtree in the
    for nd in _subtree:
        childs = []
        for v in _subtree[nd]:
            if not isinstance(v, Tree):
                childs.append(v)
            #else:
            #    childs.append(v.label())
        _subtree[nd] = childs
    """

    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    strs = ""
    #split_ind = 0
    mark_ind = 0
    for nd in node_list[1:]:
        #import pdb; pdb.set_trace()
        #print(nd)
        if (root in nd) and ('advcl' in nd[4].keys()):
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']
            pass

        if (root in nd) and ('advcl' in nd[4].keys()):
            advcl_ind = nd[4]['advcl'][0]


            #import pdb; pdb.set_trace()
            mark_list = []
            nsubj_ind = 0
            if ('nsubj' in nd[4].keys()):
                nsubj_ind = nd[4]['nsubj'][0]

            advcl_dict = {}
            for _nd in node_list: #BUG
                if advcl_ind == _nd[0]:
                     advcl_dict = _nd[4]
                     mark_list = _nd
                     break


            #import pdb; pdb.set_trace()
            if ('mark' in advcl_dict.keys()):
                #import pdb; pdb.set_trace()
                mark_ind = mark_list[4]['mark'][0]
                marker = tokens[mark_ind].lower()

                # get the marker,  delete the conjunction
                #tokens[mark_ind] = ''
                #tokens[mark_ind+1] = upper_first_char(tokens[mark_ind+1])
                # if the marker is in the dict1
                # [NOTICE]: we use the punctuation to check the sentence
                if (marker in dict1.keys()): # if dict1, subordinated clause goes first
                    # delete the conjunction,
                    _w = dict1[marker]
                    tokens[mark_ind] = ''
                    tokens[mark_ind+1] = base.upper_first_char(tokens[mark_ind+1])

                    #[NOTICE]: we consider 1st ',' to split the sentence, and get the 2nd sentence

                    #import pdb; pdb.set_trace()
                    """
                    if  COMMA in tokens: #
                        split_ind = tokens.index(COMMA)
                        tokens[split_ind] = ''
                         #import pdb; pdb.set_trace()
                        #print "tokens: ", tokens[split_ind+1]
                        #= tokens[split_ind+1][0].upper() + tokens[split_ind+1][1:]
                        _str1 = tokens[:(split_ind)]
                        str1 = ' '.join(_str1)
                        #print "1st sent: ", str1

                        _str2 = tokens[(split_ind+1):]
                        #w = _w + ' '
                        str2 = _w + ' ' + ' '.join(_str2)
                        #print "2nd sent: ", str2

                        strs = str1 + ' . ' + str2

                        return strs
                    """

                    if nsubj_ind != 0:
                        _str1 = tokens[:(nsubj_ind)]
                        if _str1[-1] in PUNCTUATION:
                            _str1[-1] = ''
                        str1 = ' '.join(_str1)
                    #print "1st sent: ", str1

                        _str2 = tokens[nsubj_ind:]
                    #w = _w + ' '
                        str2 = _w + ' ' + ' '.join(_str2)
                    #print "2nd sent: ", str2

                        strs = str1 + ' . ' + str2

                    else:
                        pass

                    return strs


                # if dict2, the subordinated clause goes second
                if (marker in dict2.keys()):
                    _w = dict2[marker]
                    tokens[mark_ind] = ''
                    tokens[mark_ind+1] = base.upper_first_char(tokens[mark_ind+1])


                    #import pdb; pdb.set_trace()
                    """
                    if COMMA in tokens:
                        split_ind = tokens.index(COMMA)
                        _str1 = tokens[:(split_ind)]
                        str1 = ' '.join(_str1)
                        #print "1st sent: ", str1

                        _str2 = tokens[(split_ind+1):]
                        #w = _w + ' '
                        str2 = _w + ' ' + ' '.join(_str2)
                        #print "2nd sent: ", str2

                        strs = str1 + ' . ' + str2
                        return strs
                    """
                    #TODO add it before the nsubj
                    if nsubj_ind != 0:
                        _str1 = tokens[:(nsubj_ind)]
                        if _str1[-1] in PUNCTUATION:
                            _str1[-1] = ''

                        str1 = ' '.join(_str1)
                    #print "1st sent: ", str1

                        _str2 = tokens[nsubj_ind:]
                    #w = _w + ' '
                        str2 = _w + ' ' + ' '.join(_str2)
                    #print "2nd sent: ", str2

                        strs = str1 + ' . ' + str2
                    else:
                        pass

                    return strs


        #if mark_ind == 0:  # if no mark word
        # adverbial clauses [NOTICE]: consider ',' to split the sentence

    return strs

def simp_advcl_sent(tokens, node_list):
    strs = ""

    """
    # the original tokens in the sent
    tokens = StanfordTokenizer().tokenize(sent)
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']

    #w = result.tree()
    #print "parse_tree:", w

    #TODO: use the tree structure, check again
    node_list = [] # dict (4 -> 4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        node_list.append(base.get_triples(node))
        #node_list[base.get_triples[0]] = base.get_triples(node)
    """
    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    #split_ind = 0
    for nd in node_list[1:]:
        #import pdb; pdb.set_trace()
        #print(nd)
        if (root in nd) and ('advcl' in nd[4].keys()):
            pass

        if (root in nd) and ('advcl' in nd[4].keys()):
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']

            #import pdb; pdb.set_trace()
            advcl_ind = nd[4]['advcl'][0]

            nsubj_ind = 0
            if ('nsubj' in nd[4].keys()):
                nsubj_ind = nd[4]['nsubj'][0]

            advcl_dict = {}
            for _nd in node_list: #BUG
                if advcl_ind == _nd[0]:
                     advcl_dict = _nd[4]
                     break


            #import pdb; pdb.set_trace()
            if ('mark' in advcl_dict.keys()):
                pass
            else:
                #[NOTICE]: just deal with advcl case
                # the subject of the main clause is used as the subject of the new sentence
                if ('nsubj' in nd[4].keys()): #and (COMMA in tokens):

                    #import pdb; pdb.set_trace()

                    #split_ind = tokens.index(COMMA)
                    nsubj_ind = nd[4]['nsubj'][0]
                    #if (advcl_ind < split_ind):
                    subj = tokens[nsubj_ind]
                    tokens.insert(1, base.upper_first_char(subj))

                    _str1 = tokens[:(nsubj_ind)]
                    if _str1[-1] in PUNCTUATION:
                        _str1[-1] = ''
                    str1 = ' '.join(_str1)
                        #print "1st sent: ", str1

                        # upper the 1st char in 2nd sent
                    tokens[nsubj_ind] = base.upper_first_char(tokens[nsubj_ind])
                    _str2 = tokens[nsubj_ind:]
                        #w = _w + ' '
                    str2 =  ' '.join(_str2)
                        #print "2nd sent: ", str2

                    strs = str1 + ' . ' + str2

                    return strs

    return strs

def simp_parti_sent(tokens, node_list):

    """
    # the original tokens in the sent
    tokens = StanfordTokenizer().tokenize(sent)
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']

    #w = result.tree()
    #print "parse_tree:", w

    #TODO: use the tree structure, check again
    node_list = [] # dict (4 -> 4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        node_list.append(base.get_triples(node))
        #node_list[base.get_triples[0]] = base.get_triples(node)

    """

    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    strs = ""
    #split_ind = 0
    for nd in node_list[1:]:
        #import pdb; pdb.set_trace()
        #print(nd)
        if (root in nd) and ('nsubj' in nd[4].keys()):
            pass

        if (root in nd) and ('nsubj' in nd[4].keys()):
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']

            #import pdb; pdb.set_trace()
            nsubj_ind = nd[4]['nsubj'][0]
            nsubj_dict = {}
            for _nd in node_list: #BUG
                if nsubj_ind == _nd[0]:
                     nsubj_dict = _nd[4]
                     break


            #import pdb; pdb.set_trace()
            if ('acl' in nsubj_dict.keys()):
                #[NOTICE]: connect the nsubj + acl as 1st
                # And the 1st end in the PUNC
                #import pdb; pdb.set_trace()
                acl_ind = nsubj_dict['acl'][0]

                #[NOTICE]: end the 1st sentence at the 'punc' place after acl_ind
                for punc in PUNCTUATION:
                    if punc in tokens[acl_ind:]:
                        split_ind = tokens[acl_ind:].index(punc)
                        break

                subj = tokens[nsubj_ind]
                #tokens.insert(1, upper_first_char(subj))

                #import pdb; pdb.set_trace()
                root_ind = tokens.index(root)
                _str1 = tokens[acl_ind:(split_ind+acl_ind)]
                if _str1[-1] in PUNCTUATION:
                    _str1[-1] = ''
                str1 = base.upper_first_char(subj) + " " + ' '.join(_str1)
                #print "1st sent: ", str1

                # upper the 1st char in 2nd sent
                _str2 = tokens[root_ind:]
                #w = _w + ' '
                str2 = base.upper_first_char(subj) + " " + ' '.join(_str2)
                #print "2nd sent: ", str2

                strs = str1 + ' . ' + str2
                return strs

    return strs

def simp_adjec_sent(tokens, node_list):
    """
    strs = ""
    # the original tokens in the sent
    tokens = StanfordTokenizer().tokenize(sent)
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']

    #w = result.tree()
    #print "parse_tree:", w

    #TODO: use the tree structure, check again
    node_list = [] # dict (4 -> 4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        node_list.append(base.get_triples(node))
        #node_list[base.get_triples[0]] = base.get_triples(node)

    """
    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    strs = ""
    #split_ind = 0
    for nd in node_list[1:]:
        #import pdb; pdb.set_trace()
        #print(nd)
        if (root in nd) and ('nsubj' in nd[4].keys()):
            pass

        if (root in nd) and ('nsubj' in nd[4].keys()):
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']

            #import pdb; pdb.set_trace()
            nsubj_ind = nd[4]['nsubj'][0]
            nsubj_dict = {}
            for _nd in node_list: #BUG
                if nsubj_ind == _nd[0]:
                     nsubj_dict = _nd[4]
                     break


            #import pdb; pdb.set_trace()
            if ('acl:relcl' in nsubj_dict.keys()):
                #[NOTICE]: connect the nsubj + acl as 1st
                #import pdb; pdb.set_trace()
                relcl_ind = nsubj_dict['acl:relcl'][0]

                subj = tokens[nsubj_ind]
                #tokens.insert(1, upper_first_char(subj))

                root_ind = tokens.index(root)
                _str1 = tokens[relcl_ind:root_ind]
                if _str1[-1] in PUNCTUATION:
                    _str1[-1] = ''
                str1 = base.upper_first_char(subj) + " " + ' '.join(_str1)
                #print "1st sent: ", str1

                # upper the 1st char in 2nd sent
                _str2 = tokens[root_ind:]
                #w = _w + ' '
                str2 = base.upper_first_char(subj) + " " + ' '.join(_str2)
                #print "2nd sent: ", str2

                strs = str1 + ' . ' + str2
                return strs

    return strs


def simp_appos_sent(tokens, node_list):
    """
    strs = ""
    # the original tokens in the sent
    tokens = StanfordTokenizer().tokenize(sent)
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']

    #w = result.tree()
    #print "parse_tree:", w

    #TODO: use the tree structure, check again
    node_list = [] # dict (4 -> 4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        node_list.append(base.get_triples(node))
        #node_list[base.get_triples[0]] = base.get_triples(node)

    """
    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    strs = ""

    #split_ind = 0
    for nd in node_list[1:]:
        #import pdb; pdb.set_trace()
        #print(nd)
        if (root in nd) and ('nsubj' in nd[4].keys()):
            pass

        if (root in nd) and ('nsubj' in nd[4].keys()):
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']

            #import pdb; pdb.set_trace()
            nsubj_ind = nd[4]['nsubj'][0]
            nsubj_dict = {}
            for _nd in node_list: #BUG
                if nsubj_ind == _nd[0]:
                     nsubj_dict = _nd[4]
                     break


            #import pdb; pdb.set_trace()
            if ('appos' in nsubj_dict.keys()):
                #[NOTICE]: connect the nsubj + acl as 1st
                #import pdb; pdb.set_trace()
                appos_ind = nsubj_dict['appos'][0]

                verb = "be"

                subj = base.upper_first_char(tokens[nsubj_ind])

                #[NOTICE]: remove the ',' after the nsubj
                if tokens[nsubj_ind + 1] in PUNCTUATION:
                    tokens[nsubj_ind + 1] = ''

                tokens.insert(nsubj_ind + 1, verb)

                root_ind = tokens.index(root)
                _str1 = tokens[nsubj_ind:root_ind]

                if _str1[-1] in PUNCTUATION:
                    _str1[-1] = ''
                str1 =  ' '.join(_str1)
                #print "1st sent: ", str1

                # upper the 1st char in 2nd sent
                _str2 = tokens[root_ind:]
                #w = _w + ' '
                str2 = upper_first_char(subj) + " " + ' '.join(_str2)
                #print "2nd sent: ", str2

                strs = str1 + ' . ' + str2
                return strs

    return strs

def simp_passive_sent(tokens, node_list):
    """
    strs = ""
    # the original tokens in the sent


    #import pdb; pdb.set_trace()
    print(sent)
    #import pdb; pdb.set_trace()
    tokens = StanfordTokenizer().tokenize(str(sent))
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']

    #w = result.tree()
    #print "parse_tree:", w

    #TODO: use the tree structure, check again
    node_list = [] # dict (4 -> 4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        node_list.append(base.get_triples(node))
        #node_list[base.get_triples[0]] = base.get_triples(node)
    """
    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    strs = ""
    #split_ind = 0
    for nd in node_list[1:]:
        #import pdb; pdb.set_trace()
        #print(nd)
        # A passive nominal subjec
        if (root in nd) and ('nsubjpass' in nd[4].keys()):
            pass

        if (root in nd) and ('nsubjpass' in nd[4].keys()):
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']

            #import pdb; pdb.set_trace()
            nsubjpass_ind = nd[4]['nsubjpass'][0]

            det_ind = 0
            subj = ""
            if ('nmod' in nd[4].keys()):
                nmod_ind = nd[4]['nmod'][0]

                nmod_dict = {}
                for _nd in node_list: #BUG
                    if nmod_ind == _nd[0]:
                         nmod_dict = _nd[4]
                         break


                #import pdb; pdb.set_trace()
            #if ('case' in nmod_dict.keys()): # 'by'
                #[NOTICE]: connect the nsubj + acl as 1st
                #import pdb; pdb.set_trace()
                if ('det' in nmod_dict):
                    det_ind = nmod_dict['det'][0]

                if det_ind:
                    subj = base.upper_first_char(tokens[det_ind]) + " " + tokens[nmod_ind]
                else:
                    subj = tokens[nmod_ind]

            strs = subj + " " + root + " " + tokens[nsubjpass_ind]
            """
                #[NOTICE]: remove the ',' after the nsubj
                if tokens[nsubj_ind + 1] in PUNCTUATION:
                    tokens[nsubj_ind + 1] = ''

                tokens.insert(nsubj_ind + 1, verb)

                #root_ind = tokens.index(root)
                #_str1 = tokens[nsubj_ind:root_ind]

                if _str1[-1] in PUNCTUATION:
                    _str1[-1] = ''
                str1 =  ' '.join(_str1)
                #print "1st sent: ", str1

                # upper the 1st char in 2nd sent
                _str2 = tokens[root_ind:]
                #w = _w + ' '
                str2 = upper_first_char(subj) + " " + ' '.join(_str2)
                #print "2nd sent: ", str2
            """
                #strs = str1 + ' . ' + str2
            return strs


    return strs

def simp_syn_sent_(sent):
    strs = ""
    # the original tokens in the sent


    #import pdb; pdb.set_trace()
    #print(sent)
    #import pdb; pdb.set_trace()
    tokens = StanfordTokenizer().tokenize(str(sent))
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']

    #w = result.tree()
    #print "parse_tree:", w
    #for row in result.triples():
    #    print(row)


    #import pdb; pdb.set_trace()
    #TODO: use the tree structure, check again
    node_list = [] # dict (4 -> 4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        node_list.append(base.get_triples(node))
        #node_list[base.get_triples[0]] = base.get_triples(node)


    #import pdb; pdb.set_trace()
    strs = simp_coordi_sent(tokens, node_list)
    #strs = simp_subordi_sent(tokens, node_list)
    #strs = simp_advcl_sent(tokens, node_list)
    #strs = simp_parti_sent(tokens, node_list)
    #strs = simp_adjec_sent(tokens, node_list)
    #strs = simp_appos_sent(tokens, node_list)
    #strs = simp_passive_sent(tokens, node_list)

    return strs

def simp_syn_sent(sent):
    strs = ""
    # the original tokens in the sent


    #import pdb; pdb.set_trace()
    #print "syn sent: ", sent
    #import pdb; pdb.set_trace()
    tokens = StanfordTokenizer().tokenize(sent)
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']

    #w = result.tree()
    #print "parse_tree:", w

    #TODO: use the tree structure, check again
    node_list = [] # dict (4 -> 4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        node_list.append(base.get_triples(node))
        #node_list[base.get_triples[0]] = base.get_triples(node)


    #import pdb; pdb.set_trace()
    if len(sent) > 0:
        strs = simp_coordi_sent(tokens, node_list)
        if len(strs) > 0:
            return strs
        else:
            strs = simp_subordi_sent(tokens, node_list)
            if len(strs) > 0:
                return strs
            else:
                strs = simp_advcl_sent(tokens, node_list)
                if len(strs) > 0:
                    return strs
                else:
                    strs = simp_parti_sent(tokens, node_list)
                    if len(strs) > 0:
                        return strs
                    else:
                        strs = simp_adjec_sent(tokens, node_list)
                        if len(strs) > 0:
                            return strs
                        else:
                            strs = simp_appos_sent(tokens, node_list)
                            if len(strs) > 0:
                                return strs
                            else:
                                strs = simp_passive_sent(tokens, node_list)
                                if len(strs) > 0:
                                    return strs


    return strs

#main
def main():
    # coordinated clauses
    sent = "He held it out, and with a delighted \"Oh!\""
    #sent = "I ate fish and he drank wine."
    sent = "We haven't totally forgotten about it, but we're looking forward to this upcoming season."
    sent = "I ate fish or he drank wine."

    sent = "I ate an apple and an orange."
    #print(simp_coordi_sent(sent))
    print(simp_syn_sent_(sent))

    # Subordinated Clauses and Adverbial Clauses
    sent= "Since he came, I left."
    sent = "Before he came, I left."
    #print(simp_subordi_sent(sent))
    #print(simp_syn_sent_(sent))

    # Adverbial Clauses
    sent = "Needing money, I begged my parents."
    #sent = "Ochoa's new teammates were generally pleased with the move, even if it wasn't a blockbuster."
    #sent = "I blinked when I opened the door."
    #print(simp_advcl_sent(sent))
    #print(simp_syn_sent(sent))

    # participial phrases
    sent = "Alicia, running down the street, tripped."
    #sent = "The MTR was immediately popular with residents of Hong Kong ; as a result , subsequent lines have been built to cover more territory . There are continual debates regarding how and where to expand the MTR network ."
    #print(simp_parti_sent(sent))
    #print(simp_syn_sent(sent))

    #Adjectival Clauses and Appositive phrases
    sent = "Peter, who liked fruits, ate an apple."
    #print(simp_adjec_sent(sent))
    #print(simp_syn_sent(sent))

    sent = "Peter, my son, ate an apple."
    #print(simp_appos_sent(sent))
    #print(simp_syn_sent(sent))

    sent = "Peter was hit by a bus."
    #print(simp_passive_sent(sent))
    sent = "Food is procured with its suckers and then crushed using its tough `` beak '' of chitin ."
    #print(simp_syn_sent_(sent))


if __name__ == '__main__':
    main()
