ticket_amount = 20
json_file_name = test_20.json
db_name = ticket_activities_20.sqlite
output_csv = output_20.csv

install:
	@pip install -e .

install_requirements:
	@pip install -r requirements.txt

create_process_tickets:
	@python ticket_processing/ticket_gen.py -n ${ticket_amount} -o ${json_file_name}
	@python ticket_processing/export_json.py -db ${db_name}
	@python ticket_processing/sql_queries.py -db ${db_name} -o ${output_csv}
	@echo '**${ticket_amount} tickets generated and processed successfully!**'
