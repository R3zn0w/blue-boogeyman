import guesser
import consts
import connectivity
from colorama import init,deinit, Fore, Back
from os.path import exists
import codecs

def getConnectionDetails() -> list[str]:
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

def provideConnectionDetails() -> list[str]:
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

init(autoreset=True)
print(Fore.RED +  consts.title)

connectionDetails = getConnectionDetails()

serverConnection = connectivity.Connectivity(connectionDetails[0], int(connectionDetails[1]))
authResp = serverConnection.authenticate(connectionDetails[2], connectionDetails[3])
if authResp == 0:
    exit()

guesserInstance = guesser.Guesser_Proto(authResp)

initialWord = serverConnection.receive()
wordLength = initialWord.__len__()

guess = guesserInstance.guessNext(initialWord)
while True:
    success = serverConnection.send(f'{guess[0]}{guess[1]}')
    if not success:
        break
    received = serverConnection.receive()
    if received == '#': #try again
        continue
    
    elif received == '=' and guess[0] == '=':
        print(consts.success + f'Word {guess[1]} guessed 😎')
        points= serverConnection.receive()
        print(f'Got {points} points 😂')
        break

    elif received == '=' and guess[0] == '+':
        print(consts.success + f'Letter {guess[1]} guessed 😎')
        serv_letters = serverConnection.receive()
        guesserInstance.updateCandidates(serv_letters,guess[1])

    elif received == '!' and guess[0] == '+':
        print(consts.log + f'Letter {guess[1]} not present')
        guesserInstance.updateCandidates('0'*wordLength,guess[1])

    else:
        print(consts.error + f'Unrecognized error')
        break

    guess = guesserInstance.guessNext()

deinit()