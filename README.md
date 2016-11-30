# Fun

**Author:** [Raphael Berly](https://www.linkedin.com/in/raphaelberly), data scientist at [Erento](https://www.erento.com/info/jobs/).

### Overview

This repository gathers some small projects which I implemented for various events at [Erento](https://www.erento.com/info/jobs/). 

Hereby a list of the scripts implemented:

* [Kicker Tournament](#kicker-tournament)
* [Lunch Roulette](#lunch-roulette)
* [Secret Santa](#secret-santa)

-----

### Kicker Tournament

This project aims at creating random two-person teams, using a list of names and their preferred position ("Offense", "Defense" or "No preference"). It was used for several Erento Kicker Tournaments, since it was designed.

Running *kicker-tournament/main.py* will output a file *kicker-tournament/teams.csv* containing the teams, and using the data from the file *kicker-tournament/survey.csv*.

-----

### Lunch Roulette

This project aims at creating random N-person teams, using a list of names and a provided team size.

Running *lunch-roulette/main.py* will output a file *lunch-roulette/gifts.csv* containing the list of names and the attributed team, using the data from the file *lunch-roulette/participants.csv*.

Example: `python lunch-roulette/main.py 5`

-----

### Secret Santa

This project aims at attributing randomly a number to everyone from a list of names. It was used to distribute the "secret gifts" at Erento Christmas Party.

Running *secret-santa/main.py* will output a file *secret-santa/gifts.csv* containing the list of names and the attributed gift, using the data from the file *secret-santa/participants.csv*.


