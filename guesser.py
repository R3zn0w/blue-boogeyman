# -*- coding: utf-8 -*-
import json
import utils
import time
from colorama import init, deinit
import consts


class Guesser_Proto:
    gloss: dict[str, list[str]]
    candidates: list[str]
    try_count: int = 0
    used_letters: list[str] = []

    def __init__(self, dictionary: int) -> None:
        print(f'Selected alphabet {dictionary}')
        with open(f'dict_{dictionary}.json', 'r') as fp:
            self.gloss = json.load(fp)
            fp.close()

    def guessNext(self, initial: str = None) -> tuple[str, str]:
        if initial != None:
            self.candidates = list(self.gloss[initial])
        print(f'Current candidates: {self.candidates}')
        print(f'Current candidates left: {self.candidates.__len__()}')
        # wywal jesli jedno haslo
        if self.candidates.__len__() == 1:
            print(f'Word {self.candidates[0]} found in {self.try_count} tries')
            return ('=', self.candidates[0])

        # znajdz najpopularniejsza literke w zestawie
        letter_count = {0: 0}
        for candidate_word in self.candidates:
            for letter in candidate_word:
                if letter in self.used_letters:
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
            for idx, candidate_word_letter in enumerate(self.candidates[0]):
                if candidate_word_letter == guess:
                    positions.append(idx)

            if positions.__len__() == 0:
                print(consts.success +
                        f'Candidate {guess} optimal!')
                break

            if not utils.areCandidatesAlmostTheSame(self.candidates, positions, guess):
                print(consts.success +
                        f'Candidate {guess} optimal!')
                break

            else:
                print(20*"+")
                del letter_count[guess]
                self.used_letters.append(guess)
                print(consts.log +
                        f'Candidate {guess} inoptimal, removing!')
                print(consts.log +
                        f'New letter count: {letter_count}')
                guess = utils.findMaxElementInDict(letter_count)

        print(f'My guess is: {guess}')
        print(20*'-')
        self.used_letters.append(guess)
        self.try_count = self.try_count + 1
        return ("+", guess)



    def updateCandidates(self,serv_ans: str, guess: str):
        self.candidates = [x for x in self.candidates if utils.isPotentialMatch(x, serv_ans, guess)]


if __name__ == '__main__':
    init(autoreset=True)
    guessInstance = Guesser_Proto(1)
    while True:
        wordToGuess = input("Enter word to guess: ")
        if wordToGuess == 'exit':
            break
        #TODO: rewrite into sequentional version
        #guessInstance.guessWord(wordToGuess) 
        print(consts.info + 20*'-')
    deinit()
