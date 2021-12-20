# -*- coding: utf-8 -*-
import time
import codecs
import multiprocessing as mp
import utils
import json


class Guesser_Testable:
    gloss: dict[str, list[str]]

    def __init__(self) -> None:
        with open('dict.json', 'r') as fp:
            self.gloss = json.load(fp)
            fp.close()

    def guessWord(self, word: str) -> str:
        # --- dev server mocking
        first_in = utils.encodeWord(word)
        # ---
        used_letters = []
        candidates = list(self.gloss[first_in])
        try_count = 0
        # start_time = time.time()
        while(True):
            # print(f'Current candidates: {candidates}')
            # print(f'Current candidates left: {candidates.__len__()}')
            # return answer if only one word left
            if candidates.__len__() == 1:
                # print(f'Word {candidates[0]} ended in {try_count} tries')
                # print(f'This took barely {time.time() - start_time} seconds')
                return try_count
                # return candidates[0]

            # find the most popular letter
            letter_count = {0: 0}
            for candidate_word in candidates:
                for letter in candidate_word:
                    if letter in used_letters:
                        continue
                    elif letter in letter_count:
                        letter_count[letter] = letter_count[letter] + 1
                    else:
                        letter_count.update({letter: 1})
            # print(letter_count)

            # zgaduj zgadula
            guess = utils.findMaxElementInDict(letter_count)
            # print(f'My guess is: {guess}')
            used_letters.append(guess)
            try_count = try_count + 1
            serv_ans = utils.mockServerAnswer(word, guess)
            # print(f'SERWER: {serv_ans}')

            candidates = [
                x for x in candidates if utils.isPotentialMatch(x, serv_ans, guess)]


def carryOnGuesser(pooledGloss: list[str]):
    guessInstance = Guesser_Testable()
    localGloss = {0: 0}
    for testWord in pooledGloss:
        guessedTries = guessInstance.guessWord(testWord)
        if guessedTries in localGloss:
            localGloss[guessedTries] = localGloss[guessedTries] + 1
        else:
            localGloss.update({guessedTries: 1})
    return localGloss


if __name__ == '__main__':
    # multithreaded benchmark for guessing algorithm
    with codecs.open("slowa_picked.txt", "r", "utf-8") as f:
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
    print(20*"-")
    print(f'Number of vcpus available: {mp.cpu_count()}')
    print(f'Number of pools: {threadDividedWordList.__len__()}')
    print(20*"-")

    counter = 0
    for i in range(threadDividedWordList.__len__()):
        print(
            f'Pool no. {i+1} word count: {threadDividedWordList[i].__len__()}')
        for j in range(threadDividedWordList[i].__len__()):
            counter = counter + 1

    print(20*"-")
    # those should be even
    print(f'Pooled words overall: {counter}')
    print(f'Words available in dictionary: {numberOfWords}')
    print(20*"-")

    # measure time
    start_time = time.time()

    pool = mp.Pool(mp.cpu_count())

    # run batch
    results = pool.map(carryOnGuesser, threadDividedWordList)

    pool.close()

    # merge maps into one
    finalMap = {0: 0}
    for result in results:
        for item in result.items():
            if item[0] in finalMap:
                finalMap[item[0]] = finalMap[item[0]] + item[1]
            else:
                finalMap.update({item[0]: item[1]})

    print("Number of words per guessing steps: ")
    # sort maps by keys
    for i in sorted(finalMap):
        print((i, finalMap[i]), end=" ")
    print(20*"-")
    print(f'This took barely {time.time() - start_time} seconds')
    print(
        f'This equals to {numberOfWords/(time.time() - start_time)} words per second')