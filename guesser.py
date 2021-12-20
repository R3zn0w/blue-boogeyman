# -*- coding: utf-8 -*-
import json
import utils
import time
import codecs


class Guesser:
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
        start_time = time.time()
        while(True):
            print(f'Current candidates: {candidates}')
            print(f'Current candidates left: {candidates.__len__()}')
            # return answer if only one word left
            if candidates.__len__() == 1:
                print(f'Word {candidates[0]} ended in {try_count} tries')
                print(f'This took barely {time.time() - start_time} seconds')
                return candidates[0]

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
            print(letter_count)

            # zgaduj zgadula
            guess = utils.findMaxElementInDict(letter_count)
            print(f'My guess is: {guess}')
            used_letters.append(guess)
            try_count = try_count + 1
            serv_ans = utils.mockServerAnswer(word, guess)
            # print(f'SERWER: {serv_ans}')

            candidates = [
                x for x in candidates if utils.isPotentialMatch(x, serv_ans, guess)]


if __name__ == '__main__':
    guessInstance = Guesser()
    while True:
        wordToGuess = input("Enter word to guess: ")
        guessInstance.guessWord(wordToGuess)
        print(20*'-')
