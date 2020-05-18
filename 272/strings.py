from typing import List
from collections import Counter


def common_words(sentence1: List[str], sentence2: List[str]) -> List[str]:
    """
    Input:  Two sentences - each is a  list of words in case insensitive ways.
    Output: those common words appearing in both sentences. Capital and lowercase 
            words are treated as the same word. 

            If there are duplicate words in the results, just choose one word. 
            Returned words should be sorted by word's length.
    """
    # Create a counter with all the words from each sentence added.
    #    Convert all words to lower case
    #    Use a sets to eliminate duplicates in each sentence
    common_counter = Counter(set([w.lower() for w in sentence1]))
    common_counter.update(set([w.lower() for w in sentence2]))

    # Find the top count - this will always be 2 or less
    top_count = common_counter.most_common(1)[0][1]
    # Find all the words with the top count
    most_common = [count[0]
                   for count in common_counter.most_common() if count[1] == top_count]

    # Return the list sorted by length
    return sorted(most_common, key=lambda w: len(w))
