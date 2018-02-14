## Kiwi.com task: the *book_flight* app
### Description:
This small Python program was made as an assignment for the "Python weekend" course organized by Kiwi.com. The purpose of the application is to utilize Kiwi.com's API to find a flight matching given parameters and simulate its booking.

Flight parameters are entered via command line arguments. Their usage is provided with the execution of `book_flight.py --help` as well as on this readme page. Correct parsing of command line arguments has been tested on Linux and Windows platforms. The program should work on both of them identically, although there might be issues with recognizing command line arguments on some Python installations in Windows. If that occurs, please refer to this stackoverflow answer: https://stackoverflow.com/questions/2640971/windows-is-not-passing-command-line-arguments-to-python-programs-executed-from-t

After parsing the arguments, the program makes a GET HTTP request to Kiwi.com's API in order to find flights matching the chosen parameters. The list of flights is ordered by their price or duration, depending on the command line argument. The cheapest/fastest flight is then booked by making a POST HTTP request to mock booking API. Successful execution of the program returns a confirmation code of the simulated order.

Besides the assignment by Kiwi.com, this program provides an additional functionality. If executed with `--list-flights` option, it prints the ordered list of all matching flights, instead of booking any of them. This feature can be used to compare prices or durations of actual real-world flights on a given date and with given departure and arrival locations.

### Usage:
    book_flight.py [-h] --date DATE --from FROM --to TO
                          [--one-way | --return RETURN] [--cheapest | --fastest]
                          [--bags BAGS] [--list-flights]
    optional arguments:
      -h, --help       show this help message and exit
      --date DATE      find flights on given date (YYYY-MM-DD format)
      --from FROM      find flights departing from given airport (IATA format)
      --to TO          find flights arriving at given airport (IATA format)
      --one-way        find one-way flights [default]
      --return RETURN  find return flights with given number of nights at the
                       destination
      --cheapest       book the cheapest flight [default]
      --fastest        book the fastest flight
      --bags BAGS      book a flight with given number of bags [default = 0]
      --list-flights   list flights ordered by price/duration, don't book any
                       flight

### Examples:
    $ ./book_flight.py --date 2018-08-20 --from BRQ --to BCN --cheapest --one-way
    $ ./book_flight.py --date 2018-08-20 --from BRQ --to DUB --fastest --return 4
    $ ./book_flight.py --date 2018-08-20 --from BRQ --to PRG --one-way --bags 1
    $ ./book_flight.py --date 2018-08-20 --from BRQ --to LHR --fastest --return 6 --list-flights
