import argparse

from data_gen_support import *
from field_options import *

def ticket_gen(params):
    file_name = params.o
    n = params.n # number of tickets

    print(f"{file_name} contains {n} tickets")

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
    status_p_ticket = [status[idx] for idx in idx_ticket_ids]  # list of arrays
    timestamps_p_ticket = np.concatenate(
        [get_time_from_status(x, metadata) for x in status_p_ticket])

    performed_at = transform_unique_array(timestamps_p_ticket, ticket_id)

    # generate fields for each unique ticket ID
    performer_type = np.array(['user'] * len(ticket_uniques))
    performer_id = np.random.choice(performer_ids,
                                    len(ticket_uniques),
                                    replace=True)
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




if __name__ == '__main__':
    # take inputs
    parser = argparse.ArgumentParser(description = "Create helpdesk tickets")
    parser.add_argument('-n', help='number of tickets to be generated')
    parser.add_argument('-o', help='json output file name')
    args = parser.parse_args()
    # print(args.accumulate(args.integers))
    ticket_gen(args)
