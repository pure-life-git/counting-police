# counting-police
#### This was a fun project started for a private discord server. It's prefix is "."
-----------------------------------------------------------------
##### This bot can do a lot of general purpose stuff and has some fun features built in, like a dice roller, rock paper scissors, and others.
The main feature of this bot is its ability to monitor a counting channel.
# Rules
1. The number you enter in the counting channel must be exactly one after the previous number.
2. If you enter a number incorrectly, you will receive a strike and the bot will warn you.
3. If you accumulate three strikes, your typing priviledges in the counting channel will be revoked and you will be the role 'Counting Clown'
# To-Do
- [x] Make a README
- [ ] Find a way to implement voice in some capacity
- [ ] Make the bot able to detect if someone edits or deletes their message and reprimand them for it
- [ ] Come up with other cool features
# Feature List
* .help - displays help for all the commands
## Game List 
* .game [game] - adds a game to the Game List
* .gamelist - iterates through and prints out the Game List
* .gameremove [game] - removes a specific game from the Game List
* .gameclear - clears the Game List
* .choosegame - chooses a random game from the Game List
## Other Features
* .poll [option 1] [option 2] [# of seconds] - creates a poll with two options that will defaulty run for 120 seconds unless otherwise specified
* .wolfram [query] - returns a simple query from Wolfram|Alpha
* .wolframfull [query] - returns a full query w/ images from Wolfram|Alpha
* .operator [attacker/defender] - returns a random operator from Rainbow Six Siege basesd on whether the user is attacking or defending
* .rps [rock/paper/scissors] - plays a game of rock paper scissors with the user. There is a 1 in 100 chance the bot picks gun and automatically wins
* .decide [num1] [num2] - generates a random number between the two user-inputted numbers
* .dice - rolls dice using a dice parser Example: .dice 1d4 2d6 would roll 1 4 sided die and 2 six sided die and print out the rolls and the total sum
* .strikes - lets the user know how many strikes they have in the counting channel
* If your message starts with any version of "I'm" or "im", the bot will make a dad joke out of your message
----------------------------------------------------------------------------
