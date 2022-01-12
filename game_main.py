import guesser
import consts
import connectivity
from colorama import init,deinit, Fore
import utils
import time

if __name__ == "__main__":
    init(autoreset=True)
    print(Fore.RED +  consts.title)
    if not utils.handlePreparation():
        print(consts.error + f'Critical error in setup, exiting...')
        exit()
    connectionDetails = utils.getConnectionDetails()
    while True:
        serverConnection = connectivity.Connectivity(connectionDetails[0], int(connectionDetails[1]))
        specialTreatment = True if connectionDetails[0] == '146.59.45.35' else False #patka special case ;---)
        authResp = serverConnection.authenticate(connectionDetails[2], connectionDetails[3], specialTreatment)
        if authResp == 0:
            break

        guesserInstance = guesser.Guesser(authResp)

        initialWord = serverConnection.receive()
        wordLength = initialWord.__len__()

        guess = guesserInstance.guessNext(initialWord)

        while True:
            success = serverConnection.send(f'{guess[0]}\n{guess[1]}\n')
            if not success: #handle restart on sending failure
                break
            received = serverConnection.receive()

            if received == False: #handle restart on socket failure
                break

            if received == '#': #server ignored answer, try again
                continue
            
            elif received == '=' and guess[0] == '=': #guessed word and was a good hit
                print(consts.win + f'Word {guess[1]} guessed in {guess[2]} tries')
                points=serverConnection.receive()
                print(f'Got {points} points 😂')
                break

            elif received == '=' and guess[0] == '+': #guessed letter and was a good hit
                print(consts.success + f'Letter {guess[1]} guessed 😎')
                serv_letters = serverConnection.receive()

                guesserInstance.updateCandidates(serv_letters,guess[1]) #update internal guessing state based on received answer

            elif received == '!' and guess[0] == '=': #guessed word and got it wrong
                pass

            elif received == '!' and guess[0] == '+': #guessed letter and got it wrong
                print(consts.log + f'Letter {guess[1]} not present')

                guesserInstance.updateCandidates('0'*wordLength,guess[1]) #update internal guessing state based on received answer

            elif received == '?': #server terminates connection
                print(consts.error + f'Server terminated connection')
                break
            else:
                print(consts.error + f'Unrecognized error with message "{received}"')
                break

            guess = guesserInstance.guessNext() #perform next guess
        utils.printDivider('X')
        time.sleep(1) #sleep 1sec as some servers cant handle that drippy fast swag boi
    deinit()