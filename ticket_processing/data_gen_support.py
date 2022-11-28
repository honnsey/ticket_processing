#!/usr/bin/env python
# coding: utf-8


import random
from faker import Faker
fake = Faker()
from datetime import timedelta, datetime as dt
import numpy as np
from field_options import activity_priorities, issue_types


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
    idx_ticket_dupes = np.concatenate([np.where(ticket_ids == x)[0] for x in ticket_dupes])
    status_dupes = np.concatenate([random.sample(status_list,count)
                                   for count in ticket_counts[np.where(ticket_counts > 1)]])
    status[idx_ticket_dupes] = status_dupes

    # for ticket_ids appearing only once, randomly choose a status from status list
    ticket_single = ticket_uniques[np.where(ticket_counts == 1)]
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

def fake_time_long_format(start_date_dt, end_date_dt):
    '''
    Return a fake date between input start date and end date.
    Both inputs must be of type datetime
    Output in string, format e.g. '28-11-2022 12:05:37 +0000'
    '''
    fake = Faker()
    fake_date_dt = fake.date_time_between(start_date=start_date_dt, end_date=end_date_dt)
    return " ".join([dt.strftime(fake_date_dt, "%d-%m-%Y %H:%M:%S"), "+0000"])

# function to create timestamp for each ticket
def get_time_from_status(status,metadata):
    '''
    Input is an array of status for one ticket
    Output is a numpy array of correspoding timestamp based on status
    '''
    # generate empty array of same shape as status
    output = np.empty(shape = status.shape,dtype = object)

    # convert metadata start and end dates to datetime format
    end_date_dt = dt.strptime(metadata['metadata']['end_at'],"%d-%m-%Y %H:%M:%S %z")
    start_date_dt = dt.strptime(metadata['metadata']['start_at'],"%d-%m-%Y %H:%M:%S %z")

    # closed status corresponds to latest timestamp
    if "Closed" in status:
        idx = np.argwhere(status =='Closed')[0][0] # idx type = integer
        output[idx] = fake_time_long_format(start_date_dt + timedelta(hours = 6),end_date_dt) # string format
        end_date_dt = dt.strptime(output[idx],"%d-%m-%Y %H:%M:%S %z")

    # resolved corresponds to latest or 2nd latest timestamp
    if "Resolved" in status:
        idx = np.argwhere(status =='Resolved')[0][0] # idx type = integer
        output[idx] = fake_time_long_format(start_date_dt + timedelta(hours = 2),end_date_dt) # string format
        end_date_dt = dt.strptime(output[idx],"%d-%m-%Y %H:%M:%S %z")

    # for other status, generate a random timestamp
    remaining_status = np.setdiff1d(status,np.array(['Closed','Resolved']))
    if len(remaining_status) > 0:
        output_idx = np.concatenate([np.where(status == x)[0] for x in remaining_status])
        output[output_idx] = [fake_time_long_format(start_date_dt,end_date_dt)
                              for i in range(len(remaining_status))]

    return output

def get_single_ship_date(metadata):
    end_date = dt.strptime(metadata['metadata']['start_at'],"%d-%m-%Y %H:%M:%S %z")
    start_date = "".join(["-",str(np.random.randint(0,14,1)[0]),"d"])
    return dt.strftime(fake.date_time_between(start_date=start_date, end_date=end_date),
                   '%d %b,%Y')