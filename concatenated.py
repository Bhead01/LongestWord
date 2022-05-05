import urllib.request


class Node:
    def __init__(self, letter=None, isTerminal=False):
        self.letter = letter
        self.isTerminal = isTerminal
        self.children = {}


class Trie:
    def __init__(self):
        self.root = Node()
        self.counts = {}

    def insert(self, word):
        current = self.root
        for letter in word:
            if letter not in current.children:
                current.children[letter] = Node(letter)
            current = current.children[letter]
        current.isTerminal = True

    def __contains__(self, word):
        current = self.root
        for letter in word:
            if letter not in current.children:
                return False
            current = current.children[letter]
        return current.isTerminal

    # Returns how many subwords can make up the word, as well as the subwords that make up the big word
    def decompose(self, word):
        # Do not accept the empty string ''
        if not word:
            return 0, []
        # Check if we've seen this word before
        if word in self.counts:
            return self.counts[word]
        # If not then we need to start traversing the trie
        current = self.root
        for index, letter in enumerate(word):
            if letter not in current.children:
                return 0, []
            current = current.children[letter]
            if current.isTerminal:
                suffix = word[index + 1:]  # Get the suffix
                suffix_count, suffix_list = self.decompose(suffix)  # decompose the suffix
                self.counts[suffix] = suffix_count, suffix_list  # store count for memoization
                if suffix_count:  # if suffix is decomposable
                    # add prefix to suffix list, add 1 to suffix count and return
                    return 1 + suffix_count, [word[:index + 1]] + suffix_list
        return current.isTerminal, [word]

    # Returns (isCompound, # small words, list of small words)
    def getCompound(self, word):
        decompose_num, decompose_list = self.decompose(word)
        return decompose_num > 1, decompose_num, decompose_list


def load(filename):
    words = []
    trie = Trie()
    file = urllib.request.urlopen(filename)
    for line in file:
        decoded_line = line.decode("utf-8")
        word = decoded_line.strip()
        trie.insert(word)
        words.append(word)

    return trie, words


def processList(compoundList):
    compoundList.sort(key=lambda tup: len(tup[0]), reverse=True)
    return compoundList


def getCompoundList(trie, words):
    compound = []
    for word in words:
        isValid, num, dlist = trie.getCompound(word)
        if isValid:
            compound.append((word, num, dlist))
    return compound


def example(filename='https://gist.githubusercontent.com/bobbae/4ca309a1857158d5766d4ede4235cae0/raw/77d5e62835c80d30b87ab7f4a84a63a4a64f7cb2/words.txt'):
    trie, words = load(filename)

    compoundList = processList(getCompoundList(trie, words))


    # returns prints longest compound word if it exists
    longestWord = compoundList[0][0]
    secondLongestWord = compoundList[1][0]

    if len(longestWord):
        print("Longest compound word found is: \t\"" + longestWord + "\"")
        print("Concatenated from " + str(compoundList[0][1]) + " words: " + str(compoundList[0][2]))
    else:
        print("No largest compound words exist in this list.")
    if len(secondLongestWord):
        print("Second Longest compound word found is: \t\"" + secondLongestWord + "\"")
        print("Concatenated from " + str(compoundList[1][1]) + " words: " + str(compoundList[1][2]))
    else:
        print("No second largest compound words exist in this list.")

    print("Number of compound words is " + str(len(compoundList)))

    return trie, words, compoundList


def main():
    filename = "https://gist.githubusercontent.com/bobbae/4ca309a1857158d5766d4ede4235cae0/raw/77d5e62835c80d30b87ab7f4a84a63a4a64f7cb2/words.txt"
    example(filename)

if __name__ == "__main__":
    main()

# original source file from  https://github.com/fizzxed/LongestConcatenatedWord/blob/master/ConcatWords.py


