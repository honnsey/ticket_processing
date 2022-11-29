import argparse
import os
import json
from numpyencoder import NumpyEncoder
from data_gen_support import *
from field_options import *

def ticket_gen(params):
    file_name = params.o
    n = int(params.n) # number of tickets

    #============= generate metadata =============
    metadata = {
        "metadata": {
            "start_at":
            " ".join([
                dt.strftime(dt.now() + timedelta(days=-1), "%d-%m-%Y %H:%M:%S"),
                "+0000"
            ]),
            "end_at":
            " ".join([dt.strftime(dt.now(), "%d-%m-%Y %H:%M:%S"),
                    "+0000"]),  # assume extract ticket at set time
            'activities_count':n
        }
    }

    #============= generate ticket ids =============
    ticket_id = generate_ticket_ids(n, len(status_list))
    ticket_uniques, unique_counts = np.unique(ticket_id, return_counts=True)
    idx_ticket_ids = [np.where(ticket_id == x)[0] for x in ticket_uniques]

    #============= generate ticket status =============
    status = generate_status(ticket_id, status_list)

    #============= generate performed_at timestamp =============
    # get array of status for each unique ticket
    start_tstamp = dt.strptime(metadata['metadata']['start_at'],
                               "%d-%m-%Y %H:%M:%S %z").timestamp()
    end_tstamp = dt.strptime(metadata['metadata']['end_at'],
                             "%d-%m-%Y %H:%M:%S %z").timestamp()
    status_p_ticket = [status[idx] for idx in idx_ticket_ids]  # list of arrays
    timestamps_p_ticket = np.array(
        [get_time_per_ticket(x, start_tstamp, end_tstamp) for x in status_p_ticket],dtype=object)

    performed_at = transform_unique_array(timestamps_p_ticket, ticket_id)

    # generate fields for each unique ticket ID
    performer_type = np.array(['user'] * len(ticket_uniques))
    performer_id = np.random.choice(performer_ids, len(ticket_uniques), replace=True)
    shipping_address = np.array(['N/A'] * len(ticket_uniques))
    category = np.random.choice(list(products.keys()),
                                len(ticket_uniques),
                                replace=True)
    issue_type = np.random.choice(list(issue_types.keys()),
                                len(ticket_uniques),
                                replace=True)
    source = np.random.randint(1, 12 + 1, size=len(ticket_uniques))
    # priority based on issue_type
    priority = np.array([get_priority(x)
                        for x in issue_type])  # based on issue_type
    group = np.concatenate([
        np.random.choice(issue_types[k], 1) for k in issue_type
    ])  # based on issue_type
    agent_id = performer_id

    requesters = np.arange(1, n + 1)
    requester = np.random.choice(requesters, len(ticket_uniques), replace=True)
    product = np.concatenate([np.random.choice(products[k], 1)
                            for k in category])  # based on category
    # shipment date depends on issue type
    shipment_date_p_ticket = np.empty(ticket_uniques.shape, object)
    idx = np.where((issue_type == 'Return') | (issue_type == 'Shipping'))[0]
    shipment_date_p_ticket[idx] = [
        get_single_ship_date(metadata) for i in range(len(idx))
    ]

    # populate generated data to match size of ticket_id
    performer_type = transform_unique_array(performer_type, ticket_id)
    performer_id = transform_unique_array(performer_id, ticket_id)
    shipping_address = transform_unique_array(shipping_address, ticket_id)
    category = transform_unique_array(category, ticket_id)
    issue_type = transform_unique_array(issue_type, ticket_id)
    source = transform_unique_array(source, ticket_id)
    priority = transform_unique_array(priority, ticket_id)
    group = transform_unique_array(group, ticket_id)
    agent_id = transform_unique_array(agent_id, ticket_id)
    requester = transform_unique_array(requester, ticket_id)
    product = transform_unique_array(product, ticket_id)
    shipment_date = transform_unique_array(shipment_date_p_ticket, ticket_id)
    contacted_customer = np.array([contact_customer_check(x) for x in status])

    #============= generate notes for randomly choosen ticket =============
    note, idx_ticketID_w_notes = get_tickets_with_notes(ticket_id)

    #============= generate & save json file =============

    activities_data = []
    for i in range(len(ticket_id)):
        activities_data.append({
            "performed_at": performed_at[i],
            "ticket_id": ticket_id[i],
            "performer_type": performer_type[i],
            "performer_id": performer_id[i],
            "activity": {
                "shipping_address": shipping_address[i],
                "shipment_date": shipment_date[i],
                "category": category[i],
                "contacted_customer": contacted_customer[i],
                "issue_type": issue_type[i],
                "source": source[i],
                "status": status[i],
                "priority": priority[i],
                "group": group[i],
                "agent_id": agent_id[i],
                "requester": requester[i],
                "product": product[i]
            }
        })

    # for each activity, remove fields baed on conditions
    for i,data in enumerate(activities_data):
        # add notes and remove other fields where notes are generated
        if i in idx_ticketID_w_notes:
            del data['activity']
            data['activity'] = {"note": note[idx_ticketID_w_notes.index(i)]}

        # remove shipment_date and shipment_address fields where value is None
        else:
            if data['activity']['shipment_date']== None:
                del data['activity']['shipment_date']
                del data['activity']['shipping_address']

            # if ticket has to do with Vendor, remove contact customer
            if data['activity']['issue_type']== 'Vendor':
                del data['activity']['contacted_customer']

    # join metadata and activities_data and save file to local disk
    final = metadata.copy()
    final.update({"activities_data": activities_data})

    expected_path = os.path.join("data", "json")
    if os.path.exists(expected_path) == False:
        os.makedirs(expected_path)
    else:
        [
            os.remove(os.path.join(expected_path,name))
            for name in os.listdir(expected_path)
        ]

    with open(os.path.join("data",'json',file_name), 'w') as outfile:
        json.dump(final,outfile,cls=NumpyEncoder,indent=4)

if __name__ == '__main__':
    # take inputs
    parser = argparse.ArgumentParser(description = "Export helpdesk tickets")
    parser.add_argument('-n', help='number of tickets to be generated')
    parser.add_argument('-o', help='json output file name')
    args = parser.parse_args()
    # print(args.accumulate(args.integers))
    ticket_gen(args)
