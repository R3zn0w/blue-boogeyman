# -*- coding: utf-8 -*-
import json
import utils
import time
import codecs
from colorama import init, Fore, Back, deinit


class Guesser_Proto:
    gloss: dict[str, list[str]]

    def __init__(self) -> None:
        with open('dict.json', 'r') as fp:
            self.gloss = json.load(fp)
            fp.close()

    def guessWord(self, word: str) -> str:
        # --- to przychodzi od serwera
        first_in = utils.encodeWord(word)
        # ---
        used_letters = []
        candidates = list(self.gloss[first_in])
        try_count = 0
        start_time = time.time()
        while(True):
            print(f'Current candidates: {candidates}')
            print(f'Current candidates left: {candidates.__len__()}')
            # wywal jesli jedno haslo
            if candidates.__len__() == 1:
                print(f'Word {candidates[0]} ended in {try_count} tries')
                print(f'This took barely {time.time() - start_time} seconds')
                return candidates[0]

            # znajdz najpopularniejsza literke w zestawie
            letter_count = {0: 0}
            for candidate_word in candidates:
                for letter in candidate_word:
                    if letter in used_letters:
                        continue
                    elif letter in letter_count:
                        letter_count[letter] = letter_count[letter] + 1
                    else:
                        letter_count.update({letter: 1})
            print(f'Letter count: {letter_count}')

            # zgaduj zgadula
            guess = utils.findMaxElementInDict(letter_count)

            while True:
                positions = []
                # nie random - pierwsze slowo (bez znaczenia)
                for idx, candidate_word_letter in enumerate(candidates[0]):
                    if candidate_word_letter == guess:
                        positions.append(idx)

                if positions.__len__() == 0:
                    print(Back.GREEN + Fore.BLACK +
                          f'Candidate {guess} optimal!')
                    break

                if not utils.areCandidatesAlmostTheSame(candidates, positions, guess):
                    print(Back.LIGHTGREEN_EX + Fore.BLACK +
                          f'Candidate {guess} optimal!')
                    break

                else:
                    print(20*"+")
                    del letter_count[guess]
                    used_letters.append(guess)
                    print(Back.LIGHTRED_EX + Fore.BLACK +
                          f'Candidate {guess} inoptimal, removing!')
                    print(Back.WHITE + Fore.BLACK +
                          f'New letter count: {letter_count}')
                    guess = utils.findMaxElementInDict(letter_count)

            print(f'My guess is: {guess}')
            print(20*'-')
            used_letters.append(guess)
            try_count = try_count + 1
            serv_ans = utils.mockServerAnswer(word, guess)
            # print(f'SERWER: {serv_ans}')

            candidates = [
                x for x in candidates if utils.isPotentialMatch(x, serv_ans, guess)]


if __name__ == '__main__':
    init(autoreset=True)
    guessInstance = Guesser_Proto()
    while True:
        wordToGuess = input("Enter word to guess: ")
        if wordToGuess == 'exit':
            break
    # with codecs.open("slowa_test.txt", "r", "utf-8") as f:
    #     fullWordList = f.read().splitlines()
    #     f.close()
    # for wordToGuess in fullWordList:
        guessInstance.guessWord(wordToGuess)
        print(Back.CYAN + 20*'-')

    deinit()
