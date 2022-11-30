FRESHDESK Tickets

## FUNCTIONALITIES
This program contains three functionalities:

1. Create FRESHDESK Ticket Activities

"ticket_gen.py" imitates the ticket activity export function of FRESHDESK. The exported data is in .json format and based on the following structure:

{
    "metadata": {
        "start_at": "20-04-2017 10:00:00 +0000",
        "end_at": "21-04-2017 09:59:59 +0000",
        "activities_count": 2
    },
    "activities_data": [{
        "performed_at": "21-04-2017 09:33:38 +0000",
        "ticket_id": 600,
        "performer_type": "user",
        "performer_id": 149018,
        "activity": {
            "note": {
                "id": 4025864,
                "type": 4
            }
        }
    }, {
        "performed_at": "21-04-2017 09:38:24 +0000",
        "ticket_id": 704,
        "performer_type": "user",
        "performer_id": 149018,
        "activity": {
            "shipping_address": "N/A",
            "shipment_date": "21 Apr, 2017",
            "category": "Phone",
            "contacted_customer": true,
            "issue_type": "Incident",
            "source": 3,
            "status": "Open",
            "priority": 4,
            "group": "refund",
            "agent_id": 149018,
            "requester": 145423,
            "product": "mobile"
        }
    }]
}
Notes:
- The program assumes that ticket activities are exported for a 24-hour period, ending with the current date time
- There can be multiple activities related to the same ticket ID within the export time window.
- Generated .json file is saved under $(pwd)/data/json

2. Data Ingestion
"export_json.py" reads and ingests the generated ticket activities into an sqlite database.
- This database is saved under $(pwd)/data/database

3. Data Transform
"sql_queries.py" connects to the database and uses SQL queries to determine:
- Time spent Open
- Time spent Waiting on Customer
- Time spent waiting for response (Pending Status)
- Time till resolution
- Time to first response

for each unique ticket ID.

Outputs from the queries are saved in $(pwd)/data/outputs in .csv format

## INSTRUCTION

This program can be run through the Makefile.
- Step 1: Clone this repo to your local disk
- Step 2: In your terminal, run command "make complete_set_up" to install the package and its requirements
- Step 3: Open Makefile and change the variables as desired, then save Makefile.
- Step 4: Return to your terminal and run command "make create_process_tickets" to create random ticket activities and calculate processing times for each ticket ID.

Notes:
- If the data directory does not exists, then Step 4 will create a data/ directory with subdirectories
- The output of Step 4 should look like this
