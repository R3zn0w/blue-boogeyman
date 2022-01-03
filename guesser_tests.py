# -*- coding: utf-8 -*-
import time
import codecs
import multiprocessing as mp
import utils
import json
import consts

#TODO: rewrite to include sequentional version

class Guesser_Testable:
    gloss: dict[str, list[str]]
    candidates: list[str]
    try_count: int = 0
    used_letters: list[str] = []

    def __init__(self, dictionary: int) -> None:
        """Initialize Guesser instance with given dictionary"""
        self.used_letters = []
        with open(f'dict_{dictionary}.json', 'r') as fp:
            self.gloss = json.load(fp)
            fp.close()

    def guessNext(self, initial: str = None) -> tuple[str, str] | tuple[str, str, int]:
        """Perform next guess using internal candidates list, if executed with optional parameter 'initial' starts guessing new word, effectively resetting progress.\n
        Returns tuple (operation, guess), where operation may be + or = and guess may be single letter(+) or whole word(=) according to operation."""
        if initial != None: #reset state if guessing again
            self.try_count = 0
            self.used_letters = []
            self.candidates = list(self.gloss[initial])

        # wywal jesli jedno haslo
        if self.candidates.__len__() == 1:
            self.try_count = self.try_count + 1
            return ('=', self.candidates[0], self.try_count)

        # znajdz najpopularniejsza literke w zestawie
        letter_count: dict[int,int] = {}
        for candidate_word in self.candidates:
            for letter in candidate_word:
                if letter in self.used_letters:
                    continue
                elif letter in letter_count:
                    letter_count[letter] = letter_count[letter] + 1
                else:
                    letter_count.update({letter: 1})

        # zgaduj zgadula
        guess = utils.findMaxElementInDict(letter_count)

        while True:
            positions = []
            # nie random - pierwsze slowo (bez znaczenia)
            for idx, candidate_word_letter in enumerate(self.candidates[0]):
                if candidate_word_letter == guess:
                    positions.append(idx)

            if positions.__len__() == 0:
                break

            if not utils.areCandidatesAlmostTheSame(self.candidates, positions, guess):
                break

            else:
                del letter_count[guess]
                self.used_letters.append(guess)
                guess = utils.findMaxElementInDict(letter_count)

        self.used_letters.append(guess)
        self.try_count = self.try_count + 1
        return ('+', guess)



    def updateCandidates(self,serv_ans: str, guess: str):
        """Updates potential matching words based on performed guess and server answer"""
        self.candidates = [x for x in self.candidates if utils.isPotentialMatch(x, serv_ans, guess)]


def carryOnGuesser(pooledGloss: list[str]) -> dict[int,int]:
    guessInstance = Guesser_Testable(2)
    tryGloss: dict[int, int] = {}
    for testWord in pooledGloss:
        encoded = utils.encodeWord(testWord, True)
        guess = guessInstance.guessNext(encoded)
        while True:
            if guess[0] == '=':
                break
            guessInstance.updateCandidates(utils.mockServerAnswer(testWord, guess[1]), guess[1])
            guess = guessInstance.guessNext()
        if guess[1] != testWord:
            print(consts.error + f'Word {testWord} not guessed!')

        guessedTries = guess[2]

        if guessedTries in tryGloss:
            tryGloss[guessedTries] = tryGloss[guessedTries] + 1
        else:
            tryGloss.update({guessedTries: 1})
    return tryGloss


if __name__ == '__main__':
    from colorama import init, deinit
    init(autoreset=True)
    # multithreaded benchmark for guessing algorithm
    with codecs.open("words_picked.txt", "r", "utf-8") as f:
        fullWordList = f.read().splitlines()
        f.close()

    numberOfWords = fullWordList.__len__()

    # split wordlist equally for all available cores
    # calculate sublist size
    step = int(numberOfWords/mp.cpu_count())

    # list to hold them all
    threadDividedWordList = []

    for cpu in range(mp.cpu_count()):
        subList = []
        for i in range(cpu*step, (cpu+1)*step):
            subList.append(fullWordList[i])

        # compensate for division rounding error and append remaining words to last pool
        if (cpu == mp.cpu_count()-1):
            diff = numberOfWords - step*mp.cpu_count()
            for i in range((cpu+1)*step, (cpu+1)*step+diff):
                subList.append(fullWordList[i])

        threadDividedWordList.append(subList)

    # print info
    utils.printDivider()
    print(f'Number of vcpus available: {mp.cpu_count()}')
    print(f'Number of pools: {threadDividedWordList.__len__()}')
    utils.printDivider()

    counter = 0
    for i in range(threadDividedWordList.__len__()):
        print(
            f'Pool no. {i+1} word count: {threadDividedWordList[i].__len__()}')
        for j in range(threadDividedWordList[i].__len__()):
            counter = counter + 1

    utils.printDivider()
    # those should be even
    print(f'Pooled words overall: {counter}')
    print(f'Words available in dictionary: {numberOfWords}')
    utils.printDivider()

    # measure time
    start_time = time.time()

    pool = mp.Pool(mp.cpu_count())

    # run batch
    results = pool.map(carryOnGuesser, threadDividedWordList)

    pool.close()

    # merge maps into one
    finalMap: dict[int, int] = {}
    for result in results:
        for item in result.items():
            if item[0] in finalMap:
                finalMap[item[0]] = finalMap[item[0]] + item[1]
            else:
                finalMap.update({item[0]: item[1]})

    print(f'Number of words per guessing steps: ')
    # sort maps by keys
    for i in sorted(finalMap):
        print((i, finalMap[i]), end=" ")
    print(f'\nAverage guessing steps needed: {utils.averageGuessesFromGuessMap(finalMap)}')
    utils.printDivider()
    print(f'This took barely {time.time() - start_time} seconds')
    print(
        f'This equals to {numberOfWords/(time.time() - start_time)} words per second')
    deinit()