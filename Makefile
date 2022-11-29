ticket_amount = 1000
json_file_name = local_test.json

install:
	@pip install -e .

create_export_tickets:
	@python ticket_processing/ticket_gen.py -n ${ticket_amount} -o ${json_file_name}
	@python ticket_processing/export_json.py

create_data_dir:
	@mkdir data
	@mkdir data/json
	@mkdir data/database

empty_data_dir:
	@rm -f data/json/*.json
	@rm data/database/*.sqlite
