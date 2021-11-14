from autocomplete import Node
from autocomplete import Trie
from requests import get


## 1. TEST lookup()

# This is Namárië, JRRT's elvish poem written in Quenya
wordbank = "Ai! laurië lantar lassi súrinen, yéni unótimë ve rámar aldaron! Yéni ve lintë yuldar avánier mi oromardi lisse-miruvóreva Andúnë pella, Vardo tellumar nu luini yassen tintilar i eleni ómaryo airetári-lírinen. Sí man i yulma nin enquantuva? An sí Tintallë Varda Oiolossëo ve fanyar máryat Elentári ortanë, ar ilyë tier undulávë lumbulë; ar sindanóriello caita mornië i falmalinnar imbë met, ar hísië untúpa Calaciryo míri oialë. Sí vanwa ná, Rómello vanwa, Valimar! Namárië! Nai hiruvalyë Valimar. Nai elyë hiruva. Namárië!".replace("!", "").replace("?", "").replace(".", "").replace(",", "").replace(";", "").split()
trie = Trie(wordbank)

# given tests
assert trie.lookup('oiolossëo') == True # capital letters
assert trie.lookup('an') == True # a prefix, but also a word
assert trie.lookup('ele') == False # a prefix, but not a word
assert trie.lookup('Mithrandir') == False # not in the wordbank

# extra tests
assert trie.lookup('OROMARDI') == True # lower-case letters
assert trie.lookup('lisse miruvóreva') == True # missing hyphen but still valid
assert trie.lookup(' lantar ') == True # extra white space
assert trie.lookup('lanta') == False # near-valid word with missing last letter

print("Passed all tests!")


## 2. TEST alphabetical_list()

# given test
wordbank = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Duis pulvinar. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos hymenaeos. Nunc dapibus tortor vel mi dapibus sollicitudin. Etiam quis quam. Curabitur ligula sapien, pulvinar a vestibulum quis, facilisis vel sapien.".replace(",", "").replace(".", "").split()
trie = Trie(wordbank)

assert trie.alphabetical_list() == ['a','ad','adipiscing','amet','aptent',
                                    'class','consectetuer','conubia',
                                    'curabitur','dapibus','dolor','duis',
                                    'elit','etiam','facilisis','hymenaeos',
                                    'inceptos','ipsum','ligula','litora',
                                    'lorem','mi','nostra','nunc','per',
                                    'pulvinar','quam','quis','sapien',
                                    'sit','sociosqu','sollicitudin','taciti',
                                    'torquent','tortor','vel','vestibulum']


# extra test 1: previous wordbank
wordbank = "Ai! laurië lantar lassi súrinen, yéni unótimë ve rámar aldaron! Yéni ve lintë yuldar avánier mi oromardi lisse-miruvóreva Andúnë pella, Vardo tellumar nu luini yassen tintilar i eleni ómaryo airetári-lírinen. Sí man i yulma nin enquantuva? An sí Tintallë Varda Oiolossëo ve fanyar máryat Elentári ortanë, ar ilyë tier undulávë lumbulë; ar sindanóriello caita mornië i falmalinnar imbë met, ar hísië untúpa Calaciryo míri oialë. Sí vanwa ná, Rómello vanwa, Valimar! Namárië! Nai hiruvalyë Valimar. Nai elyë hiruva. Namárië!".replace("!", "").replace("?", "").replace(".", "").replace(",", "").replace(";", "").split()
trie = Trie(wordbank)

assert trie.alphabetical_list() == ['ai', 'airetári-lírinen', 'aldaron', 'an', 'andúnë', 
                             'ar', 'avánier','caita', 'calaciryo','eleni', 'elentári',
                             'elyë','enquantuva','falmalinnar','fanyar','hiruva',
                             'hiruvalyë', 'hísië', 'i', 'ilyë', 'imbë', 'lantar',
                             'lassi', 'laurië', 'lintë','lisse-miruvóreva', 'luini',
                             'lumbulë','man','met','mi','mornië','máryat','míri','nai',
                             'namárië','nin','nu','ná','oialë','oiolossëo','oromardi',
                             'ortanë','pella','rámar','rómello','sindanóriello','sí',
                             'súrinen','tellumar','tier','tintallë','tintilar','undulávë',
                             'untúpa','unótimë','valimar','vanwa','varda','vardo','ve',
                             'yassen','yuldar','yulma','yéni','ómaryo']

# extra test 2: all valid words but only one trie path
wordbank = "a ab abc abcd abcde abcdef abcdefg".replace("!", "").replace("?", "").replace(".", "").replace(",", "").replace(";", "").split()
trie = Trie(wordbank)

assert trie.alphabetical_list() == ['a', 'ab', 'abc', 'abcd', 'abcde', 'abcdef', 'abcdefg']

# extra test 3: empty word bank
wordbank = "".replace("!", "").replace("?", "").replace(".", "").replace(",", "").replace(";", "").split()
trie = Trie(wordbank)

assert trie.alphabetical_list() == []

print("Passed all tests!")


## 3. TEST k_most_common()

# might have to pip install requests
# Mehreen Faruqi - Black Lives Matter in Australia: https://bit.ly/CS110-Faruqi
# John F. Kennedy - The decision to go to the Moon: https://bit.ly/CS110-Kennedy
# Martin Luther King Jr. - I have a dream: https://bit.ly/CS110-King
# Greta Thunberg - UN Climate Summit message: https://bit.ly/CS110-Thunberg
# Vaclav Havel - Address to US Congress after the fall of Soviet Union: https://bit.ly/CS110-Havel

speakers = ['Faruqi', 'Kennedy', 'King', 'Thunberg', 'Havel']
bad_chars = [';', ',', '.', '?', '!', '_', '[', ']', ':', '“', '”', '"', '–', '-']

for speaker in speakers:
    
    # download and clean up the speech from extra characters
    speech_full = get(f'https://bit.ly/CS110-{speaker}').text
    just_text = ''.join(c for c in speech_full if c not in bad_chars)
    without_newlines = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in just_text)
    just_words = [word for word in without_newlines.split(" ") if word != ""]
    
    trie = Trie(just_words)
    
    if speaker == 'Faruqi':
        Faruqi = [('the', 60), ('and', 45), ('to', 39), ('in', 37), 
                  ('of', 34), ('is', 25), ('that', 22), ('this', 21), 
                  ('a', 20), ('people', 20), ('has', 14), ('are', 13), 
                  ('for', 13), ('we', 13), ('have', 12), ('racism', 12), 
                  ('black', 11), ('justice', 9), ('lives', 9), ('police', 9)]
        
        assert trie.k_most_common(20) == Faruqi
    
    elif speaker == 'Kennedy':
        Kennedy = [('the', 117), ('and', 109), ('of', 93), ('to', 63), 
                   ('this', 44), ('in', 43), ('we', 43), ('a', 39), 
                   ('be', 30), ('for', 27), ('that', 27), ('as', 26), 
                   ('it', 24), ('will', 24), ('new', 22), ('space', 22), 
                   ('is', 21), ('all', 15), ('are', 15), ('have', 15), ('our', 15)]
        assert trie.k_most_common(21) == Kennedy
    
    elif speaker == 'Havel':
        Havel = [('the', 34), ('of', 23), ('and', 20), ('to', 15), 
                 ('in', 13), ('a', 12), ('that', 12), ('are', 9), 
                 ('we', 9), ('have', 8), ('human', 8), ('is', 8), 
                 ('you', 8), ('as', 7), ('for', 7), ('has', 7), ('this', 7), 
                 ('be', 6), ('it', 6), ('my', 6), ('our', 6), ('world', 6)]
        assert trie.k_most_common(22) == Havel
    
    elif speaker == 'King':
        King = [('the', 103), ('of', 99), ('to', 59), ('and', 54), ('a', 37), 
                ('be', 33), ('we', 29), ('will', 27), ('that', 24), ('is', 23), 
                ('in', 22), ('as', 20), ('freedom', 20), ('this', 20), 
                ('from', 18), ('have', 17), ('our', 17), ('with', 16), 
                ('i', 15), ('let', 13), ('negro', 13), ('not', 13), ('one', 13)]
        assert trie.k_most_common(23) == King
    
    elif speaker == 'Thunberg':
        Thunberg = [('you', 22), ('the', 20), ('and', 16), ('of', 15), 
                    ('to', 14), ('are', 10), ('is', 9), ('that', 9), 
                    ('be', 8), ('not', 7), ('with', 7), ('i', 6), 
                    ('in', 6), ('us', 6), ('a', 5), ('how', 5), ('on', 5), 
                    ('we', 5), ('all', 4), ('dare', 4), ('here', 4), 
                    ('my', 4), ('people', 4), ('will', 4)]
        assert trie.k_most_common(24) == Thunberg
        
print("Passed all tests!") 

# extra test
speaker = 'Faruqi'
speech_full = get(f'https://bit.ly/CS110-{speaker}').text
just_text = ''.join(c for c in speech_full if c not in bad_chars)
without_newlines = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in just_text)
just_words = [word for word in without_newlines.split(" ") if word != ""]

trie = Trie(just_words)    
    
Faruqi = [('the', 60), ('and', 45), ('to', 39), ('in', 37), 
          ('of', 34), ('is', 25), ('that', 22), ('this', 21), 
          ('a', 20), ('people', 20), ('has', 14), ('are', 13), 
          ('for', 13), ('we', 13), ('have', 12), ('racism', 12), 
          ('black', 11), ('justice', 9), ('lives', 9), ('police', 9)]

print("extra test 1")
print(trie.k_most_common(-1)) # negative number
print("\n extra test 2")
print(trie.k_most_common(0)) # zero
print("\n extra test 3")
print(trie.k_most_common(1000000)) # large number


## 4. TEST autcomplete()

bad_chars = [';', ',', '.', '?', '!', '1', '2', '3', '4',
             '5', '6', '7', '8', '9', '0', '_', '[', ']']

SH_full = get('http://bit.ly/CS110-Shakespeare').text
SH_just_text = ''.join(c for c in SH_full if c not in bad_chars)
SH_without_newlines = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in SH_just_text)
SH_just_words = [word for word in SH_without_newlines.split(" ") if word != ""]

SH_trie = Trie(SH_just_words)

assert SH_trie.autocomplete('hist') == 'history'
assert SH_trie.autocomplete('en') == 'enter'
assert SH_trie.autocomplete('cae') == 'caesar'
assert SH_trie.autocomplete('gen') == 'gentleman'
assert SH_trie.autocomplete('pen') == 'pen'
assert SH_trie.autocomplete('tho') == 'thou'
assert SH_trie.autocomplete('pent') == 'pentapolis'
assert SH_trie.autocomplete('petr') == 'petruchio'

print("Passed all tests")

# extra test
speaker = 'Faruqi':
bad_chars = [';', ',', '.', '?', '!', '_', '[', ']', ':', '“', '”', '"', '–', '-']
speech_full = get(f'https://bit.ly/CS110-{speaker}').text
just_text = ''.join(c for c in speech_full if c not in bad_chars)
without_newlines = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in just_text)
just_words = [word for word in without_newlines.split(" ") if word != ""]

trie = Trie(just_words)

Faruqi = [('the', 60), ('and', 45), ('to', 39), ('in', 37), 
          ('of', 34), ('is', 25), ('that', 22), ('this', 21), 
          ('a', 20), ('people', 20), ('has', 14), ('are', 13), 
          ('for', 13), ('we', 13), ('have', 12), ('racism', 12), 
          ('black', 11), ('justice', 9), ('lives', 9), ('police', 9)]

assert trie.autocomplete("") == "the" # empty prefix simple returns the most common word in trie
assert trie.autocomplete("andd") == "ERROR: prefix does not exist in trie" # prefix is longer that the actual word
assert trie.autocomplete("???") == "ERROR: prefix does not exist in trie" # bad characters that don't exist in trie
assert trie.autocomplete("JU") == "justice" # capital letters

print("Passed all tests")
