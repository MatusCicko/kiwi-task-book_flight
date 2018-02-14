#!/usr/bin/python3

import sys
import argparse
import requests
from datetime import datetime


def convertTimestamp(timestamp):
    """Read a Unix timestamp and return it in a human-readable time format."""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def parseArgs(argv):
    """Parse arguments from the command line and return parameters of the flight.

    A parser is set up in order to evaluate command line arguments and build
    a "parameters" dictionary containing instructions for the flight search.
    If the "date" argument is invalid, the function raises a ValueError exception
    and causes the program to terminate.

    Successful execution of a function returns flight parameters, number of bags
    to be booked and a boolean variable indicating, whether the program should
    book a flight or only list found flights.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--date', required=True, dest='Date',
                        help='find flights on given date (YYYY-MM-DD format)')
    parser.add_argument('--from', required=True, dest='From',
                        help='find flights departing from given airport (IATA format)')
    parser.add_argument('--to', required=True, dest='To',
                        help='find flights arriving at given airport (IATA format)')

    flight_type = parser.add_mutually_exclusive_group()
    flight_type.add_argument('--one-way', dest='Oneway', action='store_true',
                             help='find one-way flights [default]')
    flight_type.add_argument('--return', dest='Return', type=int,
                             help='find return flights with given\
                             number of nights at the destination')

    flight_sort = parser.add_mutually_exclusive_group()
    flight_sort.add_argument('--cheapest', dest='Cheapest', action='store_true',
                             help='book the cheapest flight [default]')
    flight_sort.add_argument('--fastest', dest='Fastest', action='store_true',
                             help='book the fastest flight')

    parser.add_argument('--bags', dest='Bags', type=int, default=0,
                        help='book a flight with given number of bags [default = 0]')
    parser.add_argument('--list-flights', dest='List_flights', action='store_true',
                        help='list flights ordered by price/duration,\
                        don\'t book any flight')

    args = parser.parse_args()

    # Uses the datetime module to test if the entered date is valid.
    try:
        Date = datetime.strptime(args.Date, '%Y-%m-%d')
    except ValueError:
        return ValueError

    parameters = dict()
    parameters['dateFrom'] = Date.strftime('%d/%m/%Y')
    parameters['dateTo'] = Date.strftime('%d/%m/%Y')
    parameters['flyFrom'] = args.From
    parameters['to'] = args.To

    if args.Fastest:
        parameters['sort'] = 'duration'
    else:
        parameters['sort'] = 'price'

    if args.Return != None:
        parameters['typeFlight'] = 'round'
        parameters['daysInDestinationFrom'] = args.Return
        parameters['daysInDestinationTo'] = args.Return
    else:
        parameters['typeFlight'] = 'oneway'

    return parameters, args.Bags, args.List_flights


def findFlights(parameters):
    """Use the given parameters to find flights and return them in a dictionary."""
    response = requests.get('https://api.skypicker.com/flights', params=parameters)
    return response.json()


def listFlights(data):
    """Print a list of found flights, ordered by their price or duration."""
    for i in range(len(data)):
        print('ID:', i+1, end='\t  ')
        print('Departure:', convertTimestamp(data[i]['dTime']), end='    ')
        print('From:', data[i]['flyFrom'], end='    ')
        print('To:', data[i]['flyTo'], end='    ')
        print('Duration:', data[i]['duration']['total'], end='\t')
        print('Stay nights:', data[i]['nightsInDest'], end='\t  ')
        print('Price:', data[i]['price'], end='\n')


def bookFlight(b_token, bags):
    """Book a specific flight and return the confirmation number or False if unsuccessful.

    The flight is booked using its booking token, the number of bags to be booked
    and personal details of a fictional passenger. If the booking is confirmed,
    the function returns the confirmation number of the order. Otherwise it returns
    False and causes the program to terminate.
    """
    details = {
        'booking_token' : b_token,
        'bags' : bags,
        'currency' : 'EUR',
        'passengers' : {
            'title' : 'Mr',
            'firstName' : 'John',
            'lastName' : 'Doe',
            'birthday' : '1988-02-29',
            'documentID' : 'AB12345',
            'email' : 'john.doe@email.com'
            }
        }
    response = requests.post('http://128.199.48.38:8080/booking', json=details).json()
    if response['status'] == 'confirmed':
        return response['pnr']
    else:
        return False


def main(argv):
    """Call defined functions in order to run the program from its start to its exit.

    At first, the program parses the given command line arguments. If the entered
    date is invalid, the program terminates with exit code 1.

    Then the program evaluates, whether it should list the found flights
    or book a flight. In the first case, the program calls a respective function
    and terminates with exit code 0.

    If the program should book a flight, it attempts to do so in a respective function,
    which returns the result of the attempt. If it was successful, the program
    terminates with exit code containing the confirmation number. Otherwise
    the program terminates with exit code 2.
    """
    parsed = parseArgs(argv)
    if parsed == ValueError:
        print('Invalid date or format! Please enter in YYYY-MM-DD format.')
        sys.exit(1)
    parameters, bags, list_flights = parsed
    payload = findFlights(parameters)

    if list_flights:
        listFlights(payload['data'])
        sys.exit(0)
    else:
        b_token = payload['data'][0]['booking_token']
        booking = bookFlight(b_token, bags)
        if booking == False:
            print('Oops! Something went wrong. Your flight could not be booked.')
            sys.exit(2)
        else:
            sys.exit(booking)


if __name__ == '__main__':
    main(sys.argv)
