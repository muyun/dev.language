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

import base

def traverse(t):
    try:
        t.labels()
    except AttributeError:
        print t,
    else:
        # Now we know that t.node is defined

        #import pdb; pdb.set_trace()
        print "(", t.label(),
        for child in t:
            traverse(child)
        print ")",

def simp_conj_sent(sent):
    tokens = StanfordTokenizer().tokenize(sent)

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']
    #print "root: ", root

    """
    words = []
    #import pdb; pdb.set_trace()
    for node in result.nodes.items():
        #print(node)
        #print(node[1]['word'])
        words.append(node[1]['word'])
    """

    #w = result.tree()
    #print "parse_tree:", w

    #TODO: use the tree, check again
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

    node_list = [] #(4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        #print(node)
        node_list.append(base.get_triples(node))

    # construct the tree
    #partial = Tree(w[parent].label(), )
    """
    _subtree = {}
    for subtree in w.subtrees():

        #import pdb; pdb.set_trace()
        traverse(subtree)
        _subtree[subtree.label()] = subtree

    """
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

    # Universal dependencies -- And relations
    """ depes format, based on dependency graph in NLTK
    ((head word, head tag), rel, (dep word, dep tag))
    e.g.  ((u'ate', u'VBD'), u'nsubj', (u'I', u'PRP'))
    """

    strs = ""
    """
    for nd in node_list:
        if 'root' in nd[4]:
            rind = nd[4]['root'] # the index of root
    """
    for nd in node_list:
        #import pdb; pdb.set_trace()
        #print(nd)
        if (root in nd) and ('conj' in nd[4].keys()):
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']
            pass

        if (root in nd) and ('cc' in nd[4].keys()):
            #print "cc: ", nd
            ind = nd[4]['cc'][0]
            #print "cc_node: ", ind

            # if the last one in the _str is ',', replace ',' with '.'

            #import pdb; pdb.set_trace()
            # some trick for the dataset
            if tokens[ind-2] == ',':
                tokens[ind-2] = ''
            if (ind-1) == 0:
                pass
            else:
                _str = tokens[:(ind-1)]

                strs = ' '.join(_str)
                strs = strs + " . "
            #print(strs)

            #import pdb; pdb.set_trace()
            # upper the first char in tokens[ind]
            _str1 = tokens[ind][0].upper() + tokens[ind][1:] + ' '
            _str2 = _str1 + ' '.join(tokens[(ind+1):])
            #print(_str2)

            strs = strs + _str2

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
    # based on the splitting alg

    #import pdb; pdb.set_trace()
    #print

    #import pdb; pdb.set_trace()
    """
    strs =""
    for str in ret:
        _strs = ' '.join(str)
        _strs = _strs + ' . '
        strs = strs + _strs
    """
    return strs

def simp_subordi_sent(sent):
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

    tokens = StanfordTokenizer().tokenize(sent)
    tokens.insert(0, '')

    result = list(eng_parser.raw_parse(sent))[0]
    root = result.root['word']
    #print "root: ", root

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

    node_list = [] #(4, u'said', u'VBD', u'root', [[18], [22], [16], [3]])
    for node in result.nodes.items():
        #print(node)
        node_list.append(base.get_triples(node))

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

    # Universal dependencies --
    """ depes format, based on dependency graph in NLTK
    ((head word, head tag), rel, (dep word, dep tag))
    e.g.  ((u'ate', u'VBD'), u'nsubj', (u'I', u'PRP'))
    """

    strs = ""
    split_ind = 0
    for nd in node_list:
        #import pdb; pdb.set_trace()
        #print(nd)
        if (root in nd) and ('advcl' in nd[4].keys()):
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']
            pass

        if (root in nd) and ('advcl' in nd[4].keys()):
            advcl_ind = nd[4]['advcl'][0]

            for _nd in node_list:
                if (advcl_ind == _nd[0]) and ('mark' in _nd[4].keys()):
                    mark_ind = _nd[4]['mark'][0]
                    # get the marker

                    #import pdb; pdb.set_trace()
                    for __nd in node_list[1:]: #skip the 1st one
                        if (__nd[1].lower() in dict1.keys()) or (__nd[1].lower() in dict2.keys()):
                            #import pdb; pdb.set_trace()
                            # mark word, so,
                            #how to know the 2rd sentence?, now we use he advcl_ind to check it
                            # Remove the 1st word like 'since/because'
                            tokens[mark_ind] = ''

                            tokens[mark_ind+1] = tokens[mark_ind+1][0].upper() + tokens[mark_ind+1][1:]

                             # add the test trick here

                             #import pdb; pdb.set_trace()
                            #[Notice]:NOW we use ',' to break the sentences
                            #the 2nd setence? now we use the advcl_ind to test
                            punct = ','
                            if punct in tokens:
                                split_ind = tokens.index(punct)
                                tokens[split_ind] = ''
                                #if mark_id > split_ind: #

                                #import pdb; pdb.set_trace()
                                #print "tokens: ", tokens[split_ind+1]
                                #= tokens[split_ind+1][0].upper() + tokens[split_ind+1][1:]

                                # if dict1, subordinated clause goes first
                                if (__nd[1].lower() in dict1.keys()):

                                    _str1 = tokens[:(split_ind)]
                                    str1 = ' '.join(_str1)
                                    print "1st sent: ", str1

                                    _str2 = tokens[(split_ind+1):]
                                    w = dict1[__nd[1].lower()] + ' '
                                    str2 = w  + ' '.join(_str2)
                                    print "2nd sent: ", str2

                                    if mark_ind < split_ind:
                                        strs = str1 + ' . ' + str2

                                # if dict2, the subordinated clause goes second
                                if (__nd[1].lower() in dict2.keys()):
                                    _str1 = tokens[:(split_ind)]
                                    str1 = ' '.join(_str1)
                                    print "1st sent: ", str1

                                    _str2 = tokens[(split_ind+1):]
                                    w = dict2[__nd[1].lower()] + ' '
                                    str2 = w  + ' '.join(_str2)
                                    print "2nd sent: ", str2

                                    if mark_ind < split_ind:
                                        strs = str1 + ' . ' + str2

                                #strs = str1 + ' . ' +  str2
                            #

                        else:
                            pass # the 3rd loop

                else:
                    pass# the 2nd loop

            #split_ind = advcl_ind # in the

    # Universal dependencies -- And relations
    """ depes format, based on dependency graph in NLTK
    ((head word, head tag), rel, (dep word, dep tag))
    e.g.  ((u'ate', u'VBD'), u'nsubj', (u'I', u'PRP'))
    """

    return strs


#main
def main():
    # coordinated clauses
    #sent = "I ate fish and he drank wine."
    sent = "He likes swimming and I like football."
    #sent = "I like swimming and he love running and she likes badminton"

    #sent = "Integra-A Hotel  Co. said its planned rights offering to raise about $9 million was declared effective and the company will begin mailing materials to shareholders at the end of this week."
    #sent = "We haven't totally forgotten about it, but we're looking forward to this upcoming season."
    sent = "He held it out, and with a delighted \"Oh!\""
    sent = "and this is factory is critical to meeting that growing demand."
    sent = "He looked me and at last said, \"Very well.\""
    sent = "For information on COPIA events open to the public, sign on to www.copia.org"
    #res = simp_coordi_sent(sent)
    #print(res)


    # Subordinated Clauses and Adverbial Clauses
    sent= "Since he came, I left."
    #sent = " Since he took the head coaching job at bottom-dwelling Vanderbilt, the question Bobby Johnson is asked most often is not, &quot;Why will things be different under you?"
    #sent = "Because he took the head, the question is asked?"
    #sent = "A mission to end a war"
    sent = "Before he came, I left."
    print(simp_subordi_sent(sent))


    # Adverbial Clauses

    # Appositive phrase

    # Adjectival Clauses and Appositive phrases


if __name__ == '__main__':
    main()
