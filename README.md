# 5143-stockgame

## Overview

- Servers ***S***<sub>***0***</sub>-***S***<sub>***n***</sub> "produce" stocks (randomly picking from existing stocks in mongo OR just random in general).
- Servers will specialize in cheap , average, or expensive stocks (values and ranges to be determined).
- Each Server ***S***<sub>***n***</sub> will generate a stock and place it onto a bounded queue waiting for clients to claim it. I think each stock should expire if not claimed in a reasonable amount of time (no idea what reasonable is, TBD).
- Clients ***C***<sub>***0***</sub>-***C***<sub>***n***</sub> are all tring to "get" a stock from Servers ***S***<sub>***0***</sub>-***S***<sub>***n***</sub>. 
- To "claim" a stock, a client must guess the correct price of the stock (simple high low game).

### Example:

- A client sends a float value to a server.
- The server will respond with:
  -  `-1 = stock is higher`
  -  `1 = stock is lower`
  -  `0 = stock is equal`

####  Lets say the Stock price is 1000.00

Exchange between client server doing the guessing game:
- ***C***<sub>***i***</sub> -> ***S***<sub>***j***</sub> 100.00         # client: guesses 100
- ***S***<sub>***j***</sub> -> ***C***<sub>***i***</sub> -1             # server: higher
- ***C***<sub>***i***</sub> -> ***S***<sub>***j***</sub> 200.00         # client: doubles guess
- ***S***<sub>***j***</sub> -> ***C***<sub>***i***</sub> -1             # server: higher
- ***C***<sub>***i***</sub> -> ***S***<sub>***j***</sub> 400.00         # client: doubles guess
- ***S***<sub>***j***</sub> -> ***C***<sub>***i***</sub> -1             # server: higher
- ***C***<sub>***i***</sub> -> ***S***<sub>***j***</sub> 800.00         # client: doubles guess
- ***S***<sub>***j***</sub> -> ***C***<sub>***i***</sub> -1             # server: higher
- ***C***<sub>***i***</sub> -> ***S***<sub>***j***</sub> 1600.00        # client: doubles guess
- ***S***<sub>***j***</sub> -> ***C***<sub>***i***</sub> 1              # server: lower
- ***C***<sub>***i***</sub> -> ***S***<sub>***j***</sub> 1200.00        # client: reduces guess by splitting last two guesses
- ***S***<sub>***j***</sub> -> ***C***<sub>***i***</sub> -1             # server: lower
- ***C***<sub>***i***</sub> -> ***S***<sub>***j***</sub> 1000.00        # client: reduces guess by another 50% of last difference
- ***S***<sub>***j***</sub> -> ***C***<sub>***i***</sub> 0              # server: go it!

This is just an example of how to approach a stock price. You could implement different strategies to get faster results.

### Mutual Exclusion

- The critical section is up to us. 
- It can be a server needs a lock from a client (binary semaphore or simple lock)
- It can be a server gives X locks to clients (counting semaphore) so more than 1 can guess.
- OR
- A token server gives out tokens that gives clients the chance to guess. We could then compete for tokens as well some how. 


### Ultimate Goals of Game

- Clients should figure out who gives most expensive stock and concentrates on trying to get stocksd from them.
- Servers should stick with a certian range of prices for some period of time, then go to another price (cheap, middle, expensive) to keep it interesting and clients guessing.
- Client with most amount of stock worth wins.

