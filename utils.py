
def findMaxElementInDict(dictToSearch: dict[str, int]) -> str:
    """Given dictionary in form <str: int> find str with highest int value."""
    maxOccurences = max(list(dictToSearch.values()))
    return list(dictToSearch.keys())[list(dictToSearch.values()).index(maxOccurences)]


def mockServerAnswer(word: str, guess: str) -> str:
    ans = ''
    for letter in word:
        if letter == guess:
            ans = ans + '1'
        else:
            ans = ans + '0'
    return ans


def encodeWord(word: str) -> str:
    tab1 = ["a", "c", "e", "m", "n", "o", "r", "s", "u", "w", "z", "x", "v"]
    tab2 = ["ą", "ę", "g", "j", "p", "y", "q"]
    tab3 = ["b", "ć", "d", "h", "k", "l", "ł",
            "ń", "ó", "ś", "t", "ź", "ż", "i"]
    tab4 = ["f"]
    numbered = ""
    for char in word:
        if char in tab1:
            numbered = numbered + "1"
        elif char in tab2:
            numbered = numbered + "2"
        elif char in tab3:
            numbered = numbered + "3"
        elif char in tab4:
            numbered = numbered + "4"
    return numbered


def isPotentialMatch(candidate: str, hints: str, guessedLetter: str) -> bool:
    """Given candidate string, string of hints in form of 011010 and guessed letter decide whether given candidate matches hint"""
    for serv_let, cand_let in zip(hints, candidate):
        if serv_let == "0" and cand_let == guessedLetter:
            return False
        elif serv_let == "1" and cand_let != guessedLetter:
            return False
    return True


def areCandidatesAlmostTheSame(candidates: list[str], positions: list[int], guess: str) -> bool:
    for candidate_word in candidates:
        if positions != [i for i, letter in enumerate(candidate_word) if letter == guess]:
            return False
    return True


if __name__ == '__main__':
    inp = input("Word to encode: ")
    print(encodeWord(inp))
