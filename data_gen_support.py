import numpy as np

def generate_ticket_ids(n, max_repeat):
    '''
    Return a numpy array of ticket ids based on the number of tickets (n) required
    Ticket IDs can be repeated but not more than the input max_repeat
    '''
    ticket_ids_options = np.arange(1, n + 1) # sampling population

    ticket_ids = np.random.choice(ticket_ids_options, size=n)
    dup_flag = 1
    while dup_flag == 1:
        ticket_uniques, unique_counts = np.unique(ticket_ids,return_counts=True)  # get unique values and number of occurences

        # one ticket_id cannot have more than 6 activities
        if unique_counts.max() <= max_repeat:  # if no value is repeated more than 6 times
            dup_flag = 0
        else:  # need to re-generate those
            # find ticket_numbers with more than 6 occurences
            to_resample = ticket_uniques[np.argwhere(
                unique_counts > max_repeat)]

            # remove values with more than 5 occurences from sampling population
            to_remove = ticket_uniques[np.argwhere(unique_counts >= max_repeat)]
            ticket_ids_options = np.delete(ticket_ids_options, to_remove - 1)

            # for each value in to_resample, get indices in ticket_ids to resample
            idx_ticket_ids_to_resample = [np.where(ticket_ids == x)[0] for x in to_resample]
            idx_ticket_ids_to_resample = np.concatenate([np.delete(a, list(range(0, max_repeat)))
                                                         for a in idx_ticket_ids_to_resample])

            # update ticket_ids
            for i in idx_ticket_ids_to_resample:
                ticket_ids[i] = np.random.choice(ticket_ids_options)

    return ticket_ids
