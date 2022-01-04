import guesser
import consts
import connectivity
from colorama import init,deinit, Fore
import utils

if __name__ == "__main__":
    init(autoreset=True)
    print(Fore.RED +  consts.title)
    if not utils.handlePreparation():
        print(consts.error + f'Critical error in setup, exiting...')
        exit()
    connectionDetails = utils.getConnectionDetails()
    while True:
        serverConnection = connectivity.Connectivity(connectionDetails[0], int(connectionDetails[1]))
        authResp = serverConnection.authenticate(connectionDetails[2], connectionDetails[3])
        if authResp == 0:
            break

        guesserInstance = guesser.Guesser(authResp)

        initialWord = serverConnection.receive()
        wordLength = initialWord.__len__()

        guess = guesserInstance.guessNext(initialWord)

        while True:
            success = serverConnection.send(f'{guess[0]}\n{guess[1]}\n')
            if not success:
                break
            received = serverConnection.receive()

            if received == False:
                break

            if received == '#': #try again
                continue
            
            elif received == '=' and guess[0] == '=':
                print(consts.win + f'Word {guess[1]} guessed in {guess[2]} tries')
                points=serverConnection.receive()
                print(f'Got {points} points 😂')
                break

            elif received == '=' and guess[0] == '+':
                print(consts.success + f'Letter {guess[1]} guessed 😎')
                serv_letters = serverConnection.receive()
                guesserInstance.updateCandidates(serv_letters,guess[1])

            elif received == '!' and guess[0] == '=':
                pass

            elif received == '!' and guess[0] == '+':
                print(consts.log + f'Letter {guess[1]} not present')
                guesserInstance.updateCandidates('0'*wordLength,guess[1])

            elif received == '?':
                print(consts.error + f'Server terminated connection')
                break
            else:
                print(consts.error + f'Unrecognized error with message "{received}"')
                break

            guess = guesserInstance.guessNext()
        utils.printDivider('X')

    deinit()