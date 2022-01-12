# -*- coding: utf-8 -*-
import json
import utils
import time
from colorama import init, deinit
import consts


class Guesser:
    gloss: dict[str, list[str]]
    candidates: list[str]
    try_count: int = 0
    used_letters: list[str] = []

    def __init__(self, dictionary: int) -> None:
        """Initialize Guesser instance with given dictionary"""
        self.used_letters = []
        print(f'Selected alphabet {dictionary}')
        with open(f'dict_{dictionary}.json', 'r') as fp:
            self.gloss = json.load(fp)
            fp.close()

    def guessNext(self, initial: str = None) -> tuple[str, str] | tuple[str, str, int]:
        """Perform next guess using internal candidates list, if executed with optional parameter 'initial' starts guessing new word, effectively resetting progress.\n
        Returns tuple (operation, guess), where operation may be + or = and guess may be single letter(+) or whole word(=) according to operation. \n
        Calling guessNext with optional parameter initial= results in clearing internal guess state and starts guessing new word given in initial="""
        if initial != None:
            self.try_count = 0
            self.used_letters = []
            self.candidates = list(self.gloss[initial])
        if self.candidates.__len__() <= 10:
            print(f'Current candidates: {self.candidates}')
        print(f'Current candidates left: {self.candidates.__len__()}')

        if self.candidates.__len__() <= 2:
            self.try_count = self.try_count + 1
            return ('=', self.removeLastCandidate(), self.try_count)

        letter_scores: dict[str, list[int]] = {}
        letter_popularity: dict[int,int] = {}
        for candidate in self.candidates:
            candidate_used_letters: list[str] = list(self.used_letters)
            for letter in candidate:
                if letter not in self.used_letters:
                    if letter in letter_popularity:
                        letter_popularity[letter] = letter_popularity[letter] + 1
                    else:
                        letter_popularity.update({letter: 1})

                if letter in candidate_used_letters:
                    continue

                score = utils.calculateLetterScore(letter, candidate)

                candidate_used_letters.append(letter)

                if score == 0:
                    continue
                if letter in letter_scores:
                    letter_scores[letter].append(score)
                else:
                    letter_scores.update({letter: [score]})
            # print(f'Letter scores: {letter_scores.items()}')

        letter_count: dict[str, int] = {}
        for key,value in letter_scores.items():
            trimmed = utils.removeDuplicates(value)
            # print(f'Trimmed values: {trimmed} for {key}')
            if value.__len__() == self.candidates.__len__() and trimmed.__len__() == 1:
                continue
 
            # print(f'Letter {key} score is {trimmed.__len__()}')
            letter_count.update({key: trimmed.__len__()})

        # zgaduj zgadula
        guess_candidates: list[str] = utils.findMaxElementsInDict(letter_count)
        print(f'Guess candidates: {guess_candidates}')
        if guess_candidates.__len__() == 1:
            guess = guess_candidates[0]
            # print(f'Single best candidate: {guess}')

        else:
            while True:
                temp = utils.findMaxElementInDict(letter_popularity)
                if temp in guess_candidates:
                    guess = temp
                    break
                else:
                    del letter_popularity[temp]


        print(f'My guess is: {guess}')
        utils.printDivider()
        self.used_letters.append(guess)
        self.try_count = self.try_count + 1
        return ("+", guess)

    def removeLastCandidate(self):
        """Removes last candidate from list"""
        return self.candidates.pop()

    def updateCandidates(self,serv_ans: str, guess: str):
        """Updates potential matching words based on performed guess and server answer"""
        self.candidates = [x for x in self.candidates if utils.isPotentialMatch(x, serv_ans, guess)]


if __name__ == '__main__':
    #offline test for single words, type 'exit' to, well... exit
    init(autoreset=True)
    guessInstance = Guesser(2) 
    while True:
        wordToGuess = input("Enter word to guess: ")
        if wordToGuess == 'exit':
            break
        encoded = utils.encodeWord(wordToGuess, True)
        guess = guessInstance.guessNext(encoded)
        while True:
            print(guess)
            if guess[0] == '=':
                if guess[1] != wordToGuess:
                    guess = guessInstance.guessNext()
                    continue
                print(consts.win + f'Word {wordToGuess} found in {guess[2]} tries')
                break
            ans = utils.mockServerAnswer(wordToGuess, guess[1])
            print(ans)
            guessInstance.updateCandidates(ans, guess[1])
            guess = guessInstance.guessNext()
        if guess[1] == wordToGuess:
            print(consts.win + f'Word guessed properly')
        utils.printDivider()
    deinit()
