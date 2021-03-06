# -*- coding: utf-8 -*-
"""
   utils.base
   ~~~~~~~~~~
   base common function
"""
#from itertools import chain
from collections import defaultdict

from nltk.tokenize import StanfordTokenizer
#from nltk.tokenize import wordpunct_tokenize

from nltk.parse.stanford import StanfordDependencyParser
eng_parser = StanfordDependencyParser(model_path=u'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')

from nltk.tag import StanfordNERTagger
eng_tagger = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')

from pattern.en import tenses, conjugate
#import inspect
#print 'inspect.getfile(pattern.en) is:', inspect.getfile(pattern)

import base
#from algs import base

PUNCTUATION = (';', ':', ',', '.', '!', '?')
COMMA = ','

def simp_adverb_sent(_tokens, node_list):
    tokens = list(_tokens)
    strs = ""

    #import pdb; pdb.set_trace()
    if COMMA not in tokens:
        return strs

    root = ""
    root_ind = node_list[0][4]['root'][0]
    for nd in node_list:
        if root_ind == nd[0]:
            root=nd[1]

    #split_ind = 0
    for nd in node_list[1:]:
        #import pdb; pdb.set_trace()
        #print(nd)
        if (root in nd) and ('advcl' in nd[4].keys() or 'xcomp' in nd[4].keys()):
            pass

        if (root in nd) and ('advcl' in nd[4].keys() or 'xcomp' in nd[4].keys() or 'advmod' in nd[4].keys()):
            #print "conj: ", nd
            #print "conj node: ", nd[4]['conj']

            #import pdb; pdb.set_trace()
            nsubj = ""
            nsubj_ind = 0
            det_ind = 0
            if ('nsubj' in nd[4].keys()):
                nsubj_ind = nd[4]['nsubj'][0]

                nsubj_dict = {}
                nsubj_compound_list = []
                amod_list = []
                det_ind = 0
                #import pdb; pdb.set_trace()
                for _nd in node_list:
                    #import pdb; pdb.set_trace()
                    if (nsubj_ind == _nd[0]):
                        #import pdb; pdb.set_trace()
                        nsubj_dict = _nd[4]
                        if ('amod' in nsubj_dict.keys()):
                            amod_list = nsubj_dict['amod']
                        if ('compound' in nsubj_dict.keys()):
                            nsubj_compound_list = nsubj_dict['compound']
                        if ('det' in nsubj_dict.keys()):
                            det_ind = nsubj_dict['det'][0]
                    #break

                #nsubj = tokens[det_ind] + " " + tokens[nsubj_ind]
                for j in amod_list:
                    nsubj = nsubj + " " + tokens[j]
                for i in nsubj_compound_list:
                    nsubj = nsubj + " " + tokens[i]
                if det_ind > 0:
                    nsubj = tokens[det_ind] + " " + nsubj + " " + tokens[nsubj_ind]
                else:
                    nsubj = nsubj + " " + tokens[nsubj_ind]

                #import pdb; pdb.set_trace()
                nsubj = nsubj.strip()
                nsubj = nsubj[0].upper() + nsubj[1:] + " "
                
                #cop_ind = 0
                if ('cop' in nd[4].keys()):
                    cop_ind = nd[4]['cop'][0]
                #import pdb; pdb.set_trace()
                
            if ('nsubjpass' in nd[4].keys()):
                nsubj_ind = nd[4]['nsubjpass'][0]
                for _nd in node_list:
                    #import pdb; pdb.set_trace()
                    if (nsubj_ind == _nd[0]):
                        #import pdb; pdb.set_trace()
                        if ('det' in _nd[4].keys()):
                            det_ind = _nd[4]['det'][0]
                            
                nsubj = tokens[det_ind] + " " + tokens[nsubj_ind]
                nsubj = nsubj.strip()

            """
            person_taggers = []
            org_taggers = []
            #import pdb; pdb.set_trace()
            # replace the nsubj with "he/she"
            for token, title in eng_tagger.tag(tokens):
                if token.lower() in nsubj.lower().split():
                    if token == 'the' or token == 'The': 
                        continue
                    if title == 'PERSON':
                        person_taggers.append(token)
                    elif title == 'ORGANIZATION':
                        org_taggers.append(token)
                    else:
                        org_taggers.append(token)
            """
            #import pdb; pdb.set_trace()
            advcl_dict = {}
            advcl_tag = ""
            if ('advcl' in nd[4].keys()):
                advcl_ind = nd[4]['advcl'][0]

                #import pdb; pdb.set_trace()
                if len(tenses(root))>0:
                    if tenses(root)[0][0] == 'infinitive':
                        tokens[advcl_ind] = conjugate(tokens[advcl_ind], tenses(root)[1][0], 3)
                    else:
                        tokens[advcl_ind] = conjugate(tokens[advcl_ind], tenses(root)[0][0], 3)

                #TODO: update the tense of the advcl_ind
                
                #import pdb; pdb.set_trace()
                #advcl_dict = {}
                for _nd in node_list[1:]: #BUG
                    if advcl_ind == _nd[0]:
                         advcl_dict = _nd[4]
                         advcl_tag = _nd[2]
                         break

                # check the nsubj of the advcl, if they are the same subj, it is adverb
                advcl_dobj_ind = 0
                for _nd in node_list[1:]:
                    if advcl_ind == _nd[0]:
                        if 'nsubj' in _nd[4].keys():
                            #import pdb; pdb.set_trace()
                            advcl_nsubj_ind = _nd[4]['nsubj'][0]
                            if tokens[advcl_nsubj_ind].lower() not in nsubj:
                                return strs
                        if 'dobj' in _nd[4].keys():
                            advcl_dobj_ind = _nd[4]['dobj'][0]

                #import pdb; pdb.set_trace()
                verb = 'was'
                #import pdb; pdb.set_trace()
                if len(tenses(root)) > 0:
                    if nsubj.strip().lower() == 'they':
                        if tenses(root)[0][0] == 'infinitive':
                            verb = conjugate(verb, tenses(root)[1][0], 2)
                        else:
                            verb = conjugate(verb, tenses(root)[0][0], 2)
                    else:
                        if tenses(root)[0][0] == 'infinitive':
                            verb = conjugate(verb, tenses(root)[1][0], 3)
                        else:
                            verb = conjugate(verb, tenses(root)[0][0], 3)

                # TODO, the tense
                if advcl_tag == 'VBN':
                    if len(nsubj)>0:
                        nsubj = nsubj[0].upper() + nsubj[1:] + " "
                if advcl_tag == 'VBG':
                    if len(nsubj)>0:
                        nsubj = nsubj[0].upper() + nsubj[1:] + " "

                #ASSUME ',' is the splitting tag
                # This assumation isnot right
                split_ind = tokens.index(COMMA)
                    #nsubj_ind = nd[4]['nsubj'][0]
                    #if (advcl_ind < split_ind):
                    #subj = tokens[nsubj_ind]
                   # tokens.insert(1, base.upper_first_char(subj))

                #if len(tenses(root))>0:
                #    tokens[advcl_ind]=conjugate(tokens[advcl_ind], tenses(root)[0][0])
                #

                #import pdb; pdb.set_trace()
                if advcl_dobj_ind > split_ind:
                    tokens[split_ind] = ""
                    _str1 = tokens[split_ind:advcl_dobj_ind+1]
                else:
                    #_str1 = ""
                    _str1 = tokens[:(split_ind)]
                    if _str1[-1] in PUNCTUATION:
                        _str1[-1] = ''
                """
                str1 = ""
                if advcl_tag == 'VBN':
                    str1 = nsubj + ' '.join(_str1)
                if advcl_tag == 'VBG':
                    str1 = ' '.join(_str1)
                """
                #import pdb; pdb.set_trace()
                _str1_ = ' '.join(_str1)
                nsubj = ' '.join(nsubj.split())
                str1 = ""
                if nsubj.lower() + ' ' in _str1_.lower().split():
                    str1 = _str1_
                else:
                    if advcl_tag == 'VBN':
                        str1 = nsubj + " " +  verb + " " + _str1_
                    else:
                        str1 = nsubj + " " + _str1_
                #print "1st sent: ", str1

                        # upper the 1st char in 2nd sent
                    #tokens[nsubj_ind] = base.upper_first_char(tokens[nsubj_ind])

                #import pdb; pdb.set_trace()
                _str2 = ""
                str2 = ""
                if split_ind < nsubj_ind:
                    #_str2 = tokens[split_ind+1:] 
                    _strs = tokens[root_ind:]
                    if ('which' == _strs[0].lower()) or ('who' == _strs[0].lower()):
                        _strs = tokens[split_ind+2:]

                    _str2 = " ".join(_strs)
                #_str2 = tokens[root_ind:]
                        #w = _w + ' '
                    """
                    if len(nsubj)>0:
                        if (('it' not in nsubj.lower()) or ('They' not in nsubj.lower())):
                            str2 = nsubj + " " + ' '.join(_str2)
                        else:
                        #str2 = nsubj[0].upper() + nsubj[1:] + " " + ' '.join(_str2)
                            if len(person_taggers) > 0:
                                str2 = "He" + " " + ' '.join(_str2)  # 'he' will be replaced with 'he/she'
                            elif len(org_taggers) > 0:
                                if base.isplural(org_taggers[-1]) or (org_taggers[-1].lower() == 'they'):
                                    str2 = "They" + " " + ' '.join(_str2)
                                else:
                                    str2 = "It" + " " + ' '.join(_str2)
                    else:
                        str2 = ' '.join(_str2)
                    """
                    nsubj = nsubj.strip()
                    _nsubj = nsubj[0].upper() + nsubj[1:]

                    if _nsubj == 'I' or _nsubj == 'She' or _nsubj == 'He':
                        str2 = _nsubj + " " + _str2
                    else:
                        #sent2 = _nsubj + " " + _str2
                    
                        #nsubj = base.replace_nsubj(sent2, nsubj)
                        #str2 = nsubj + _str2
                        str2 = _nsubj + " " + _str2
                else:
                    if advcl_dobj_ind > split_ind:
                        _strs = tokens[advcl_dobj_ind+1:]
                        if _strs[0] in PUNCTUATION:
                            _strs[0] = ''
                    else:
                        _strs = tokens[split_ind+1:]
                        
                    if len(_str2)>0 and (('which' == _str2[0].lower()) or ('who' == _str2[0].lower())):
                        _strs = tokens[split_ind+2:]

                    _str2 = " ".join(_strs)

                    nsubj = nsubj.strip()
                    _nsubj = nsubj[0].upper() + nsubj[1:]
                    
                    if _nsubj == 'I' or _nsubj == 'She' or _nsubj == 'He':
                        str2 = _nsubj + " " + _str2
                    else:
                        #sent2 = _nsubj + " " + _str2
                    
                        #nsubj = base.replace_nsubj(sent2, nsubj)
                        #str2 = nsubj + " " + _str2
                        str2 = _nsubj + " " + _str2
                    
                #print "2nd sent: ", str2

                if str1:
                    strs = str1 + ' . ' + str2
                else:
                    strs = str2

                return strs    

            #import pdb; pdb.set_trace()
            xcomp_ind = 0 
            if ('xcomp' in nd[4].keys()):
                xcomp_ind = nd[4]['xcomp'][0]
                if len(tenses(root))>0:
                    tokens[xcomp_ind] = conjugate(tokens[xcomp_ind], tenses(root)[0][0], 3)

                #import pdb; pdb.set_trace()
                #advcl_dict = {}
                for _nd in node_list: #BUG
                    if xcomp_ind == _nd[0]:
                         xcomp_dict = _nd[4]
                         xcomp_tag = _nd[2]
                         break

                #if len(tenses(root)) > 0:
                #    tokens[xcomp_ind]=conjugate(tokens[xcomp_ind], tenses(root)[0][0])

                #import pdb; pdb.set_trace()
                verb = 'was'
                #import pdb; pdb.set_trace()
                if len(tenses(root)) > 0:
                    if nsubj.strip().lower() == 'they':
                        verb = conjugate(verb, tenses(root)[0][0], 2)
                    else:
                        verb = conjugate(verb, tenses(root)[0][0], 3)
                # TODO
                if xcomp_tag == 'VBN':
                    nsubj = nsubj[0].upper() + nsubj[1:] + " "
                if xcomp_tag == 'VBG':
                    nsubj = nsubj[0].upper() + nsubj[1:] + " "

                split_ind = tokens.index(COMMA)
                    #nsubj_ind = nd[4]['nsubj'][0]
                    #if (advcl_ind < split_ind):
                    #subj = tokens[nsubj_ind]
                   # tokens.insert(1, base.upper_first_char(subj)) 

                _str1 = tokens[:(split_ind)]
                if _str1[-1] in PUNCTUATION:
                    _str1[-1] = ''

                str1 = ""

                #import pdb; pdb.set_trace()
                nsubj = ' '.join(nsubj.split())
                _str1_ = ' '.join(_str1)
                #if xcomp_tag == 'VBN':
                if nsubj.lower() + ' ' in _str1_.lower():
                    str1 = _str1_
                else:
                    if advcl_tag == 'VBN':
                        str1 = nsubj + " " +  verb + " " + _str1_
                    else:
                        str1 = nsubj + " " +  _str1_
                """
                #elif xcomp_tag == 'VBG':
                    if nsubj.lower() in _str1_.lower():
                        str1 = _str1_
                    else:
                        str1 = nsubj + _str1_
                """
                #print "1st sent: ", str1

                        # upper the 1st char in 2nd sent
                    #tokens[nsubj_ind] = base.upper_first_char(tokens[nsubj_ind])

                #import pdb; pdb.set_trace()
                _str2 = ""
                str2 = ""
                if nsubj_ind < split_ind:
                    _strs = tokens[split_ind+1:]
                    if ('which' == _strs[0].lower()) or ('who' == _strs[0].lower()):
                        _strs = tokens[split_ind+2:]
                    _str2 = " ".join(_strs)
                    #TODO: update the tense
                    #_str2 = tokens[root_ind:]
                #_str2 = tokens[split_ind+1:]
                        #w = _w + ' '
                    """
                    if len(nsubj)>0:
                        if (('it' not in nsubj.lower()) or ('they' not in nsubj.lower())):
                            str2 = nsubj + " " + ' '.join(_str2)
                        else:
                        #str2 = nsubj[0].upper() + nsubj[1:] + " " + ' '.join(_str2)
                            if len(person_taggers) > 0:
                                str2 = "He" + " " + ' '.join(_str2)  # 'he' will be replaced with 'he/she'
                            elif len(org_taggers) > 0:
                                if base.isplural(org_taggers[-1]) or (org_taggers[-1].lower() == 'they'):
                                    str2 = "They" + " " + ' '.join(_str2)
                                else:
                                    str2 = "It" + " " + ' '.join(_str2)

                    else:
                        str2 = ' '.join(_str2)
                    """
                     #str2 = nsubj[0].upper() + nsubj[1:] + " " + ' '.join(_str2)
                    nsubj = nsubj.strip()
                    _nsubj = nsubj[0].upper() + nsubj[1:]

                    if _nsubj == 'I' or _nsubj == 'He' or _nsubj == 'She':
                        str2 = _nsubj + " " + _str2
                    else:
                        #sent2 = _nsubj + " " + _str2
                        #nsubj2 = base.replace_nsubj(sent2, nsubj)
                        #str2 = nsubj2 + _str2
                        str2 = _nsubj + " " + _str2
                   
                else:
                    str2 = base.upper_first_char(nsubj) + " " + ' '.join(tokens[split_ind+2:])
                #str2 = "That" + " " + ' '.join(_str2)
                #print "2nd sent: ", str2

                if str1:
                    if str2:
                        strs = str1 + ' . ' + str2 
                    else:
                        strs = str1 + ' . '
                else:
                    strs = str2 + ' . '

                return strs

            #import pdb; pdb.set_trace()
            advmod_ind = 0 
            if ('advmod' in nd[4].keys()):
                advmod_ind = nd[4]['advmod'][0]
                #if len(tenses(root))>0:
                #    tokens[advmod_ind] = conjugate(tokens[advmod_ind], tenses(root)[0][0], 3)

                #import pdb; pdb.set_trace()
                #advcl_dict = {}
                for _nd in node_list: #BUG
                    if advmod_ind == _nd[0]:
                         advmod_dict = _nd[4]
                         advmod_tag = _nd[2]
                         break

                #if len(tenses(root)) > 0:
                #    tokens[xcomp_ind]=conjugate(tokens[xcomp_ind], tenses(root)[0][0])

                #import pdb; pdb.set_trace()
                verb = 'was'
                #import pdb; pdb.set_trace()
                if len(tenses(root)) > 0:
                    if nsubj.strip().lower() == 'they':
                        verb = conjugate(verb, tenses(root)[0][0], 2)
                    else:
                        verb = conjugate(verb, tenses(root)[0][0], 3)
                # TODO
                if nsubj:
                    nsubj = nsubj.strip()
                    nsubj = nsubj[0].upper() + nsubj[1:]

                split_ind = tokens.index(COMMA)
                    #nsubj_ind = nd[4]['nsubj'][0]
                    #if (advcl_ind < split_ind):
                    #subj = tokens[nsubj_ind]
                   # tokens.insert(1, base.upper_first_char(subj)) 

                _str1 = tokens[:(split_ind)]
                if _str1[-1] in PUNCTUATION:
                    _str1[-1] = ''

                str1 = ""

                #import pdb; pdb.set_trace()
                nsubj = ' '.join(nsubj.split())
                _str1_ = ' '.join(_str1)
                #if xcomp_tag == 'VBN':
                if nsubj.lower() + ' ' in _str1_.lower():
                    str1 = _str1_
                else:
                    str1 = nsubj + " " + verb + " " + _str1_.lower()
                """
                #elif xcomp_tag == 'VBG':
                    if nsubj.lower() in _str1_.lower():
                        str1 = _str1_
                    else:
                        str1 = nsubj + _str1_
                """
                #print "1st sent: ", str1

                        # upper the 1st char in 2nd sent
                    #tokens[nsubj_ind] = base.upper_first_char(tokens[nsubj_ind])

                #import pdb; pdb.set_trace()
                _str2 = ""
                str2 = ""
                if nsubj_ind < split_ind:
                    _strs = tokens[split_ind+1:]
                    if ('which' == _strs[0].lower()) or ('who' == _strs[0].lower()):
                        _strs = tokens[split_ind+2:]
                    _str2 = " ".join(_strs)
                    #TODO: update the tense
                    #_str2 = tokens[root_ind:]
                #_str2 = tokens[split_ind+1:]
                        #w = _w + ' '
                     #str2 = nsubj[0].upper() + nsubj[1:] + " " + ' '.join(_str2)
                    
                    nsubj = nsubj.strip()
                    if nsubj:
                        _nsubj = nsubj[0].upper() + nsubj[1:]

                        if _nsubj == 'I' or _nsubj == 'He' or _nsubj == 'She':
                            str2 = _nsubj + " " + _str2
                        else:
                        #sent2 = _nsubj + " " + _str2
                        #nsubj2 = base.replace_nsubj(sent2, nsubj)
                        #str2 = nsubj2 + _str2
                            str2 = _nsubj + " " + _str2
                   
                else:
                    str2 = base.upper_first_char(nsubj) + " " + ' '.join(tokens[split_ind+2:])
                #str2 = "That" + " " + ' '.join(_str2)
                #print "2nd sent: ", str2

                #import pdb; pdb.set_trace()

                if str1:
                    if str2:
                        strs = str1 + ' . ' + str2 
                    else:
                        strs = str1 + ' . '
                else:
                    strs = str2 + ' . '

                return strs
            
 
    return strs


def simp_syn_sent_(sent):
    strs = ""
    # the original tokens in the sent

    #import pdb; pdb.set_trace()
    #print(sent)
    #import pdb; pdb.set_trace()
    _tokens = StanfordTokenizer().tokenize(str(sent))
    #tokens = wordpunct_tokenize(str(sent))
    _tokens.insert(0, '')

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
    #strs = simp_coordi_sent(tokens, node_list)
    #strs = simp_subordi_sent(tokens, node_list)
    strs = simp_adverb_sent(_tokens, node_list)
    #strs = simp_parti_sent(tokens, node_list)
    #strs = simp_adjec_sent(tokens, node_list)
    #strs = simp_appos_sent(tokens, node_list)
    #strs = simp_passive_sent(tokens, node_list)

    return strs

def main():
    #  clauses
    sent = "Needing money, I begged my parents."
    
    
    #sent = "Refreshed, Peter stood up."

    #sent = "The storm continued , crossing the Outer Banks of North Carolina , and retained its strength until June 20 when it became extratropical near Newfoundland ."
    #sent = "Despite almost daily reports of missing property , he was able to evade capture until 15 February , when a man named Wimbow , who had been pursuing him with a partner for days , found him in an area of thick brush called Liberty Plains and shot him ."
    #sent = "Published by Tor Books , it was released on August 15 , 1994 in hardcover , and in paperback on July 15 , 1997 ."
    sent = "Peter, who liked fruits, ate an apple."
    
    sent = "Published by Tor Books , it was released on August 15 , 1994 in hardcover , and in paperback on July 15 , 1997 ."
    sent = "The Pennines constitute the main watershed in northern England , dividing the eastern and western parts of the country ."
    sent = "They locate food by smell , using sensors in the tip of their snout , and regularly feast on ants and termites ."
    sent = "At present it is formed by the Aa , which descends from the Rigi and enters the southern extremity of the lake ."
    sent = "Realising that the gang could not elude the police forever , Moondyne Joe formulated a plan to escape the colony by traveling overland to the colony of South Australia ."
    sent = "Located on the River Pedieos and situated almost in the center of the island , it is the seat of government as well as the main business center ."
    sent = "The storm continued , crossing the Outer Banks of North Carolina , and retained its strength until June 20 when it became extratropical near Newfoundland ."
    sent = "Foods left unused too long will often acquire substantial amounts of bacterial colonies and become dangerous to eat , leading to food poisoning ."
    sent = "Published by Tor Books , it was released on August 15 , 1994 in hardcover , and in paperback on July 15 , 1997 ."
    #sent = "Refreshed, Peter stood up."
    sent = "They locate food by smell , using sensors in the tip of their snout , and regularly feast on ants and termites ."
    sent = "Notrium is played from a top-down perspective , giving an overhead view of proceedings ."
    sent = "The first amniotes , such as Casineria , resembled small lizards and evolved from amphibian reptiliomorphs about 340 million years ago ."
    sent = "They locate food by smell , using sensors in the tip of their snout , and regularly feast on ants and termites ."
    sent = "Peter came, suprising everyone ."
    #sent = "Needing money, I begged my parents."
    #sent = "Peter came, surprising everyone."
    #sent = "Refreshed, Peter stood up."
    #sent = "Impatient, he stood up."
    #sent = "Impatient, they stood up."
    #sent = "Refreshed, they stood up."
    sent = "Refreshed,  Alicia Smith stood up."
    sent = "Devastated, they left."
    
    #sent = "Since he was late, I left."
    #sent = "Since she was thirsty , he offered a drink."
    #sent = "Refreshed, Alicia stood up."
    #sent = "Peter, sweating hard, arrived."
    sent = "Alicia, running down the street, stumbled."
    #sent = "Needing money, I begged my parents."
    #sent = "Professor Cameron, carrying many books, came into the classroom."
    sent = "Frightened by the sound, he ran away."
    #print(simp_coordi_sent(sent))
    print(simp_syn_sent_(sent))    

        
if __name__ == '__main__':
    main()
