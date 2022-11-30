ticket_amount = 1000
json_file_name = local_test.json
db_name = ticket_activities.sqlite

install:
	@pip install -e .

install_requirements:
	@pip install -r requirements.txt

create_process_tickets:
	@python ticket_processing/ticket_gen.py -n ${ticket_amount} -o ${json_file_name}
	@python ticket_processing/export_json.py -db ${db_name}
	@python ticket_processing/sql_queries.py -db ${db_name}
