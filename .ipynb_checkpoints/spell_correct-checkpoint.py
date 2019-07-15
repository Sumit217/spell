import re
from collections import Counter

# Candidate Model: c is a subset of possible spell correction candidates
# This tells us which candidate corrections, c, to consider.

# The subset of words that appear in the dictionary of ExampleCorpus
def wordExist(words): 

    wordsSubset = set(w for w in words if w in ExampleCorpus)
    
    return wordsSubset

# For editDistance 1, i.e. All edits that are one edit away from word in check
def editDistance1(word):
    
#     word = words(word)
    englishalphabets    = 'abcdefghijklmnopqrstuvwxyz'
    word_splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    word_deletes    = [left + right[1:] for left, right in word_splits if right]
    word_transposes = [left + right[1] + right[0] + right[2:] for left, right in word_splits if len(right)>1]
    word_replaces   = [left + eng + right[1:] for left, right in word_splits if right for eng in englishalphabets]
    word_inserts    = [left + eng + right for left, right in word_splits for eng in englishalphabets]
    word_possible1 = set(word_deletes + word_transposes + word_replaces + word_inserts)
    
    return word_possible1

# For editDistance 2, i.e. All edits that are two edits away from word in check
def editDistance2(word): 
    
    word_possible2 = (eDis2 for eDis1 in editDistance1(word) for eDis2 in editDistance1(eDis1))
    
    return word_possible2

# Language Model: P(c) 
# The probability that c appears as a word of English text. 
# For example,if occurrences of "here" make up about 20% of English text, so we should have P(here) = 0.2.

#Clean string
def words(text): 

    text= re.sub(r"\'s", " \'s",text)
    text= re.sub(r"\'ve", " \'ve",text)
    text= re.sub(r"n\'t", " n\'t",text)
    text= re.sub(r"\'re", " \'re",text)
    text= re.sub(r"\'d", " \'d",text)
    text= re.sub(r"\'ll", " \'ll",text)
    text= re.sub(r",", " , ",text)
    text= re.sub(r"!", " ! ",text)
    text= re.sub(r"\(", " \( ",text)
    text= re.sub(r"\)", " \) ",text)
    text= re.sub(r"\?", " \? ",text)
    text= re.sub(r"\s{2,}", " ",text)
    text= re.sub(r'\S*(x{2,}|X{2,})\S*',"xxx",text)
    text= re.sub(r'[^\x00-\x7F]+', "",text)
    text= re.sub(" \d+", "",text)   #added
    text= re.sub("^\d+\s|\s\d+\s|\s\d+$", " ",text)  
    text= re.sub(r"-","",text)
    
    emoticons_happy = set([':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])
    emoticons_sad = set([':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c', ':c', ':{', '>:\\', ';('])
    
    emoticons = emoticons_happy.union(emoticons_sad)
    
    #Emoji patterns
    emoji_pattern = re.compile(
        "["u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)
    
    
    text = emoji_pattern.sub(r'', text)

    # check tokens against stop words , emoticons and punctuations
    textfinal = ''
    
    for i in text:
        if i not in emoticons:
                textfinal+=i
                
    textfinal= re.findall(r'\w+', textfinal.lower())
    return textfinal


ExampleCorpus = Counter(words(open('example_corpus.txt').read()))


# Probability of word
def wordProb(word, N=sum(ExampleCorpus.values())): 
    
    wordProbability = ExampleCorpus[word] / N
    
    return wordProbability

# Error Model: P(w|c)
# The probability that w would be typed in a text when the author meant c. 
# For example, P(hear|here) is relatively high, but P(heeyer|here) would be low.

# Most probable spelling correction for word in check
def probableCorrection(word): 
    
    Correction = max(getPossibleWords(word), key=wordProb)
    
    return Correction


# Generate possible spelling corrections for word in check
def getPossibleWords(word): 
    
    possibleWords = (wordExist([word]) or wordExist(editDistance1(word)) or wordExist(editDistance2(word)) or [word])
    
    return possibleWords

# Evaluating spell corrector

# Run correction(wrong) on all (right, wrong) pairs; report results

def resultspelltest(tests, verbose=False):
    import time
    start = time.clock()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = probableCorrection(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in ExampleCorpus)
            if verbose:
                print('probable correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, ExampleCorpus[w], right, ExampleCorpus[right]))
    dt = time.clock() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
# Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs

def inputTestSetData(lines):
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]



if __name__ == '__main__':
    

    print(len(editDistance1('ambigious')))
    print(wordExist(editDistance1('ambigious')))
    print(wordExist(editDistance2('ambigious')))
    print(wordProb('ambigious',N=sum(ExampleCorpus.values())))
    print(getPossibleWords('ambigious'))
    print(probableCorrection('ambigious'))
    #testwords--
    l1=["poetry: poartry poertry poetre poety powetry","ecstasy: exstacy ecstacy","voluntary: volantry"]

    inputTestSetData(l1)
    resultspelltest(inputTestSetData(l1))