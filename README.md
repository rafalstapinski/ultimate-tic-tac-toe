# Ultimate Tic-Tac-Toe

### A client/server implementation of a multiplayer game of ultimate tic-tac-toe available at https://stapinski.co/p/uttt

The deploy/ directory is the exact configuration I have running on my DO droplet using nginx and uwsgi. 
The local/ directory can be used to run a local implementation of the game using web.py's builtin web server. 

#### Rules to the game are available on the [Ultimate Tic-Tac-Toe Wikipedia page](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe)

### How to play

1. Go to https://stapinski.co/p/uttt
2. Create a game
3. Share the second player link with your opponent
4. Follow the rules and enjoy!

### The basics

![Share the link with your opponent](https://cloud.githubusercontent.com/assets/4674164/25557370/e4a0ef2e-2cdd-11e7-92ce-7e23343d1178.png)

This is where you will play. You can see whether you are x or o, and whose turn it is.

![The cell you move decides which board your opponent will have to move next](https://cloud.githubusercontent.com/assets/4674164/25557303/f1835f16-2cdc-11e7-8bd9-0f18d3db9549.png)

If you move to the bottom cell of your local board, that means your opponent will have to move in the bottom local board. If the local board is taken (won or filled) your opponent can move anywhere. 

![Single tic-tac-toe](https://cloud.githubusercontent.com/assets/4674164/25557302/f18343d2-2cdc-11e7-9563-3fcc66f0623b.png)

Get tic-tac-toe in a local board to win that board. 

![Ultimate tic-tac-toe](https://cloud.githubusercontent.com/assets/4674164/25557304/f1840006-2cdc-11e7-8126-aff106b83c35.png)

Get tic-tac-toe with local boards and you win the game!
