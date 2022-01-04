import codecs
import consts
from os.path import exists
from shutil import get_terminal_size
import json

def areCandidatesAlmostTheSame(candidates: list[str], positions: list[int], guess: str) -> bool:
    """Leftover for testing purposes"""
    #TODO: do śmieci po testach
    for candidate_word in candidates:
        if positions != [i for i, letter in enumerate(candidate_word) if letter == guess]:
            return False
    return True

def encodeWord(word: str, isNormalVersionForLogicallyThinkingHuman: bool) -> str:
    """Encode single word into its numerical representation in given system (e.g. "koko" -> "3131")"""

    map1 = {1:['w', 'e', 'r', 'u', 'i', 'o', 'a', 's', 'z', 'x', 'c', 'v', 'n', 'm', 'ę', 'ó', 'ą', 'ś', 'ń', 'ć', 'ż', 'ź'],
    2: ['p', 'y', 'j', 'g', 'q'],
    3: ['t', 'l', 'b', 'd', 'h', 'k', 'ł'],
    4: ["f"]}

    map2 = {1:["a", "c", "e", "m", "n", "o", "r", "s", "u", "w", "z", "x", "v"],
    2: ["ą", "ę", "g", "j", "p", "y", "q"],
    3: ["b", "ć", "d", "h", "k", "l", "ł", "ń", "ó", "ś", "t", "ź", "ż", "i"],
    4: ["f"]}

    selectedVersionMap = map2 if isNormalVersionForLogicallyThinkingHuman else map1
    numbered = ''
    for char in word:
        for key in selectedVersionMap.keys():
            if char in selectedVersionMap[key]:
                numbered = numbered + str(key)
                break
    return numbered

def findMaxElementInDict(dictToSearch: dict[str, int]) -> str:
    """Given dictionary in form <str: int> find str with highest int value."""
    maxOccurences = max(list(dictToSearch.values()))
    return list(dictToSearch.keys())[list(dictToSearch.values()).index(maxOccurences)]

def findMaxElementsInDict(dictToSearch: dict[str, int]) -> list[str]:
    """Given dictionary in form <str: int> find strings with highest int value."""
    maxOccurences = max(list(dictToSearch.values()))
    return [key for key, value in dictToSearch.items() if value == maxOccurences]

def generateDictionaries(isNormalVersionForLogicallyThinkingHuman: bool) -> None:
    """Create dictionary from file "words_picked.txt" that maps numeral representation into all possible words (e.g. "11111111": ["aaronowa", "aaronowe", ... ])"""
    gloss: dict[str, list[str]] = {}
    with codecs.open("words_picked.txt", "r", "utf-8") as f:
        words = f.read().splitlines()
        f.close()
    for word in words:
        numbered = encodeWord(word, isNormalVersionForLogicallyThinkingHuman)
        if numbered in gloss:
            gloss[numbered].append(word)
        else:
            gloss.update({numbered: [word]})

    with open(f'dict_{2 if isNormalVersionForLogicallyThinkingHuman else 1}.json', 'w') as fp:
        json.dump(gloss, fp)
    fp.close()

def getConnectionDetails() -> list[str]:
    """Presents available (if any) saved connection details for user allowing to choose desired one"""
    if exists('servers.txt'):
        with codecs.open('servers.txt', 'r', 'utf-8') as fp:
            servers = fp.readlines()
            fp.close()
        print(f'Select connection details: ')
        for idx,server in enumerate(servers):
            splitted = server.split()
            print(f'{idx+1}) {" ".join(splitted[0:3])}')
        selected = input(f'Which one? (select any other number for manual input) ')
        if int(selected) > servers.__len__():
            print(consts.error + f'Selected manual input.')
            return provideConnectionDetails()
        elif servers[int(selected)-1].split().__len__() != 5:
            print(consts.error + f'File format error, falling back to manual input!')
            return provideConnectionDetails()
        else:
            return servers[int(selected)-1].split()[1:]
    else:
        print(f'No servers.txt found. Provide connection details.')
        return provideConnectionDetails()

def handlePreparation() -> bool:
    """Check for existence of wordlists and dictionaries required to run the algorithm (files are: words.txt, words_picked.txt, dict_1.json and dict_2.json)"""
    if not exists('words.txt'):
        print(consts.error + f'No words.txt file! Exiting...')
        return False
    if not exists('words_picked.txt'):
        print(consts.error + f'No words_picked.txt file! Will generate now...')
        pickWords(5)

    if exists('dict_1.json') and exists('dict_2.json'):
        return True

    print(consts.error + f'No maps generated! Will generate now...')

    if not exists('dict_1.json'):
        generateDictionaries(False)
    if not exists('dict_2.json'):
        generateDictionaries(True)
    
    print(consts.info + "Required files generated successfully")
    return True

def isPotentialMatch(candidate: str, hints: str, guessedLetter: str) -> bool:
    """Given candidate string, string of hints in form of 011010 and guessed letter decide whether given candidate matches hint"""
    for serv_let, cand_let in zip(hints, candidate):
        if serv_let == "0" and cand_let == guessedLetter:
            return False
        elif serv_let == "1" and cand_let != guessedLetter:
            return False
    return True


def mockServerAnswer(word: str, guess: str) -> str:
    """Function for development purposes"""
    ans = ''
    for letter in word:
        if letter == guess:
            ans = ans + '1'
        else:
            ans = ans + '0'
    return ans

def pickWords(lowerLimit: int = 0, upperLimit: int = 420) -> None:
    """Create new words file "words_picked.txt" with (lowerLimit >= letters <= upperLimit) words"""
    with codecs.open("words.txt", "r", "utf-8") as f:
        temp = f.read().splitlines()
        f.close()
    with codecs.open("words_picked.txt", "w", "utf-8") as f:
        for word in temp:
            if word.__len__() >= lowerLimit and word.__len__() <= upperLimit:
                f.write(f'{word}\n')
        f.close()

def printDivider(char: str = '-'):
    print(char*int(get_terminal_size((40,40))[0]/2))

def provideConnectionDetails() -> list[str]:
    """Prompt user for manual input of server connection details and offer possibility of saving"""
    ip = input(f'Server ip: ')
    port = input(f'Server port: ')
    login = input(f'Login: ')
    password = input(f'Password: ')
    save = input(f'Do you want to save those details? [y/aNy]')
    if save.lower() == 'y':
        name = input(f'Friendly creds name: ')
        with codecs.open("servers.txt", "a", "utf-8") as f:
            f.write(f'\n{name} {ip} {port} {login} {password}')
            f.close()
    return [ip,port,login,password]

def averageGuessesFromGuessMap(guessMap: dict[int, int]) -> float:
    weighedSum = 0
    wordsCount = 0
    for key,item in guessMap.items():
        weighedSum = weighedSum + key*item
        wordsCount = wordsCount + item
    return weighedSum/wordsCount

def calculateLetterScore(letter: str, word: str):
    score: int = 0
    for idx, word_letter in enumerate(word):
        if letter == word_letter:
            score = score + pow(2,idx)
    return score

def removeDuplicates(listToRemoveFrom: list[str]):
    listToReturn: list[str] = []
    for item in listToRemoveFrom:
        if item not in listToReturn:
            listToReturn.append(item)
    return listToReturn