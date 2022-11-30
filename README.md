FRESHDESK Tickets

## FUNCTIONALITIES
This program containes three functionalities:

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

2. Data Ingestion
"export_json.py" reads and ingests the generated ticket activities into an sqlite database.

3. Data Transform
"sql_queries.py" connects to the database and uses SQL queries to determine:
- Time spent Open
- Time spent Waiting on Customer
- Time spent waiting for response (Pending Status)
- Time till resolution
- Time to first response
