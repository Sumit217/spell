#
Following folder contains 3 components
1. spell_correct.py -- main algorithm code -- which contains the algorithm generated for spell correction, this was created more pythonically instead of existing libraries or algorithms.
2. flaskapi.py -- api (INPUT is a word- "ambigious", OUTPUT - list of possible corrects as ['ambitious','ambiguous'])
3. example_corpus.txt -- large corpus for dictionary creation -- The text file example_corpus.txt is taken as support to create a dictionaries of words.It is a concatenation of public domain book excerpts from Project Gutenberg and lists of most frequent words from Wiktionary and the British National Corpus, as mentioned in the heading.

##
Algorithmically,
There are three parts in the algorithm,

#Candidate Model: where a simple edit to a word is a deletion (remove one letter), a transposition (swap two adjacent letters), a replacement (change one letter to another) or an insertion (add a letter). The function editDistance1 returns a set of all the edited strings (whether words or not) that can be made with one simple edit. similarily for editDistance2 if 2 edits required in the word.
However, if we restrict ourselves to words that are known—that is, in the dictionary— then the set is much smaller:

#Language Model: We can estimate the probability of a word, P(word), by counting the number of times each word appears in a text file of about a million words(example_corpus.txt). The function words breaks text into words and preprocess it for emojis and hyphens, then the variable 'ExampleCorpus' holds a Counter of how often each word appears, and 'wordProb' estimates the probability of each word, based on this Counter.


#noisy/error model:

Without data it's difficult to build a good spelling error model, so I defined an error model that says all known words of edit distance 1 are infinitely more probable than known words of edit distance 2, and infinitely less probable than a known word of edit distance 0. So we can make candidates(word) produce the first non-empty list of candidates in order of priority:
The original word, if it is known; otherwise
The list of known words at edit distance one away, if there are any; otherwise
The list of known words at edit distance two away, if there are any; otherwise
The original word, even though it is not known.
Then we don't need to multiply by a P(w|c) factor, because every candidate at the chosen priority will have the same probability, according to the model.


###
Future Improvements:

1. P(w|c), the error model. So far, the error model has been trivial: the smaller the edit distance, the smaller the error. This causes some problems, as the examples below show. First, some cases where correction returns a word at edit distance 1 when it should return one at edit distance 2 Why should "adres" be corrected to "address" rather than "acres"? The intuition is that the two edits from "d" to "dd" and "s" to "ss" should both be fairly common, and have high probability, while the single edit from "d" to "c" should have low probability.Clearly we could use a better model of the cost of edits. We could use our intuition to assign lower costs for doubling letters and changing a vowel to another vowel (as compared to an arbitrary letter change), but it seems better to gather data: to get a corpus of spelling errors, and count how likely it is to make each insertion, deletion, or alteration, given the surrounding characters. We need a lot of data to do this well. If we want to look at the change of one character for another, given a window of two characters on each side, that's 266, which is over 300 million characters. You'd want several examples of each, on average, so we need at least a billion characters of correction data; probably safer with at least 10 billion.

2. In the language model. To deal with unknown words, we can allow the result of correction to be a word we have not seen. For example, if the input is "electroencephalographicallz", a good correction would be to change the final "z" to an "y", even though "electroencephalographically" is not in our dictionary. We could achieve this with a language model based on components of words: perhaps on syllables or suffixes, but it is easier to base it on sequences of characters: common 2-, 3- and 4-letter sequences.

3. We could consider extending the model by allowing a limited set of edits at edit distance 3. For example, allowing only the insertion of a vowel next to another vowel, or the replacement of a vowel for another vowel, or replacing close consonants like "c" to "s" would handle almost all these cases.

4. The context of the surrounding words can help when there are obvious errors, but two or more good candidate corrections. Why should 'thear' be corrected as 'there' rather than 'their'? It is difficult to tell by the single word alone, but if the query were correction('There's no there thear') it would be clear.To build a model that looks at multiple words at a time, we will need a lot of data.I believe that a spelling corrector that scores 90% accuracy will need to use the context of the surrounding words to make a choice.

5. we could improve the implementation by making it much faster, without changing the results. We could re-implement in a compiled language rather than an interpreted one. We could cache the results of computations so that we don't have to repeat them multiple times.

