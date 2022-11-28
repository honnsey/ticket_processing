import argparse

def ticket_gen(params):
    file_name = params.o
    no_of_tickets = params.n

    print(f"{file_name} contains {no_of_tickets} tickets")

    # generate activities

    # generate metadata based on dates of activities

if __name__ == '__main__':
    # take inputs
    parser = argparse.ArgumentParser(description = "Create helpdesk tickets")
    parser.add_argument('-n', help='number of tickets to be generated')
    parser.add_argument('-o', help='json output file name')
    args = parser.parse_args()
    # print(args.accumulate(args.integers))
    ticket_gen(args)
