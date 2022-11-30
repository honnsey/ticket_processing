#!/usr/bin/env python
# coding: utf-8

import random
from datetime import timedelta, datetime as dt
import pytz
from faker import Faker
import numpy as np
from ticket_processing.field_options import activity_priorities, issue_types, status_order

def contact_customer_check(status):
    if status in ["Closed","Resolved","Waiting for Customer"]:
        return True
    else:
        return random.choice([True, False])

def generate_ticket_ids(n, max_repeat):
    '''
    Return a numpy array of ticket ids based on the number of tickets (n) required
    Ticket IDs can be repeated but not more than the input max_repeat
    '''
    ticket_ids_options = np.arange(1,n+1)
    ticket_ids = np.random.choice(ticket_ids_options,size=n) # generate ticket ids
    dup_flag = 1
    while dup_flag == 1:
        ticket_uniques, unique_counts = np.unique(ticket_ids, return_counts=True) # get unique values and number of occurences

        # one ticket_id cannot have more than 6 activities
        if unique_counts.max() <= max_repeat: # if no value is repeated more than 6 times
            dup_flag = 0
        else: # need to re-generate those
            # find ticket_numbers with more than 6 occurences
            to_resample = ticket_uniques[np.argwhere(unique_counts > max_repeat)]

            # remove values with more than 5 occurences from sampling population
            to_remove = ticket_uniques[np.argwhere(unique_counts >= max_repeat)]
            ticket_ids_options = np.delete(ticket_ids_options,to_remove - 1)

            # for each value in to_resample, get indices in ticket_ids to resample
            idx_ticket_ids_to_resample = [np.where(ticket_ids == x)[0] for x in to_resample]
            idx_ticket_ids_to_resample = np.concatenate([np.delete(a,list(range(0,max_repeat)))
                                                         for a in idx_ticket_ids_to_resample])

            # update ticket_ids
            for i in idx_ticket_ids_to_resample:
                ticket_ids[i] = np.random.choice(ticket_ids_options)

    return ticket_ids

def generate_status(ticket_ids,status_list):
    '''
    Return a numpy array of statuses based on input ticket_ids array
    Tickets of the same ids will have different status
    '''
    status = np.empty(shape= ticket_ids.shape, dtype=object)
    ticket_uniques, ticket_counts = np.unique(ticket_ids, return_counts=True)

    # for tickets of the same id, allocate none repeated status
    ticket_dupes = ticket_uniques[np.where(ticket_counts > 1)]
    if len(ticket_dupes) > 0:
        idx_ticket_dupes = np.concatenate([np.where(ticket_ids == x)[0] for x in ticket_dupes])
        status_dupes = np.concatenate([random.sample(status_list,count)
                                    for count in ticket_counts[np.where(ticket_counts > 1)]])
        status[idx_ticket_dupes] = status_dupes

    # for ticket_ids appearing only once, randomly choose a status from status list
    ticket_single = ticket_uniques[np.where(ticket_counts == 1)]
    if len(ticket_single) > 0:
        idx_ticket_single = np.concatenate([np.where(ticket_ids == x)[0] for x in ticket_single])
        status_single = np.random.choice(status_list,len(ticket_single))
        status[idx_ticket_single] = status_single

    return status

def get_priority(issue_type):
    '''
    Return ticket priority based on issue_type
    '''
    return activity_priorities[list(issue_types.keys()).index(issue_type)]

def transform_unique_array(unique_field,ticket_id):
    '''
    Transform array with per-unique-ticket values to array corresponding to ticket ID
    '''
    # generate empty output array of same shape as ticket_ids
    output = np.empty(shape=ticket_id.shape,dtype = unique_field.dtype)

    # group ticket_ids indices based on ticket_id value
    ticket_uniques, unique_counts = np.unique(ticket_id,return_counts=True)
    idx_ticket_ids = [np.where(ticket_id == x)[0] for x in ticket_uniques]

    # assign value to output
    for j,idx in enumerate(idx_ticket_ids):
        output[idx] = unique_field[j]
    return output


def get_time_per_ticket(status, start_tstamp, end_tstamp):

    status_rank = np.array([status_order.index(_) for _ in status])
    order = status_rank.argsort()
    ranks = order.argsort()

    timestamps = np.sort(
        np.random.choice(np.arange(start_tstamp, end_tstamp),
                         size=len(status),
                         replace=False))
    time_list = [
        dt.strftime(dt.fromtimestamp(x, pytz.timezone("UTC")),
                    "%d-%m-%Y %H:%M:%S %z") for x in timestamps
    ]
    time_ordered = np.array([time_list[i] for i in ranks])

    return time_ordered

def get_single_ship_date(metadata):
    fake = Faker()
    end_date = dt.strptime(metadata['metadata']['start_at'],"%d-%m-%Y %H:%M:%S %z")
    start_date = "".join(["-",str(np.random.randint(0,14,1)[0]),"d"])
    return dt.strftime(fake.date_time_between(start_date=start_date, end_date=end_date),
                   '%d %b, %Y')

def get_tickets_with_notes(ticket_id):
    '''
    Randomly choose a small number of ticket ids and assign a note to each of those.
    Any ticket containing a note will not have other fields
    Return:
    - list of notes for the number of choosen tickets
    - list of ticket ID indices (in input ticket id array) where a note will be created
    '''
    ticket_uniques, unique_counts = np.unique(ticket_id, return_counts=True)

    # randomly choose some ticket ids with notes only
    ticketID_note_pop = ticket_uniques[np.where(unique_counts == 1)[0]]
    choose_random_note = random.choices(
        [1, 0], weights=[10, 90], k=len(ticketID_note_pop)
    )  # if random no. = 1, ticket with notes, else no note
    ticketID_w_notes = ticketID_note_pop * choose_random_note
    ticketID_w_notes = ticketID_w_notes[ticketID_w_notes != 0]  # remove zero

    if len(ticketID_w_notes) > 0:
        # generate note for the choosen ticket ids
        note_id = np.random.randint(1000000, 9999999, len(ticketID_w_notes))
        note_type = np.random.randint(0, 7, len(ticketID_w_notes))
        note = [{"id": x, "type": y} for x, y in zip(note_id, note_type)]
        idx_ticketID_w_notes = np.concatenate(
            [np.where(ticket_id == x)[0] for x in ticketID_w_notes]).tolist()
    else:
        note = []
        idx_ticketID_w_notes = []

    return note, idx_ticketID_w_notes
