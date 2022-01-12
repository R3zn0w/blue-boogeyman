
# blue-boogeyman

  

## Requirements

  

Python >=3.10 && Colorama

  

`pip install -r .\requirements.txt`

  
  

## Run

`git clone https://github.com/R3zn0w/blue-boogeyman`

`cd ./blue-boogeyman`

Put your words.txt file in here (one word per line).

`python ./game_main.py`

Run game from game_main.py

Script will perform initial configuration and detect missing files, generating words and needed dictionaries. By default words of length >=5 are picked, to change this behaviour, edit line 112 in file `utils.py`

Remember that this is only client portion, you need your own server in order to actually play.

It is possible to test working offline
`python ./guesser.py`
Will allow to manually input words to guess and observe results, for more logging uncomment lines in guesser.py

  

## Benchmark

`python ./guesser_tests.py`
Benchmark using guesser_tests.py (will put 100% stress on your CPU, might take a lot of time).

For benchmarking, first run game_main and complete first config

  

### Proper readme is still WIP
