import argparse
import sqlite3
from texttable import Texttable
import os
import pandas as pd


def sqlite_query(params):

    db_name = params.db

    conn = sqlite3.connect(f'data/database/{db_name}')
    c = conn.cursor()

    c.execute('''
    CREATE Temp Table temp_tbl as
    select
        ticket_id, status , performed_at,
        rank() over (partition by ticket_id
                    order by performed_at ) as time_rank
    from activities_data ad''')

    c.execute('''
    select rawTbl.ticket_id,
        max(case when (rawTbl.status = "Open" and rawTbl.sub_act_ts is NULL)
                then round((JULIANDAY(m.end_at) - JULIANDAY(rawTbl.performed_at))* 86400/3600)
                else (case when (rawTbl.status = "Open" and rawTbl.sub_act_ts is not NULL)
                        then round((JULIANDAY(rawTbl.sub_act_ts) - JULIANDAY(rawTbl.performed_at))* 86400/3600)
                        end)
        end) time_spent_open,
        max(case when (rawTbl.status = "Waiting for Customer" and rawTbl.sub_act_ts is NULL)
                then round((JULIANDAY(m.end_at) - JULIANDAY(rawTbl.performed_at))* 86400/3600)
                else (case when (rawTbl.status = "Waiting for Customer" and rawTbl.sub_act_ts is not NULL)
                            then round((JULIANDAY(rawTbl.sub_act_ts) - JULIANDAY(rawTbl.performed_at))* 86400/3600)
                            end)
        end) time_spent_waiting_on_customer,
        max(case when (rawTbl.status = "Pending" and rawTbl.sub_act_ts is NULL)
                then round((JULIANDAY(m.end_at) - JULIANDAY(rawTbl.performed_at))* 86400/3600)
                else (case when (rawTbl.status = "Pending" and rawTbl.sub_act_ts is not NULL)
                            then round((JULIANDAY(rawTbl.sub_act_ts) - JULIANDAY(rawTbl.performed_at))* 86400/3600)
                            end)
        end) time_spent_waiting_for_response,
        max(case when (rawTbl.status = "Resolved" and rawTbl.prev_act_ts is NULL)
                then round((JULIANDAY(rawTbl.performed_at) - JULIANDAY(m.start_at))* 86400/3600)
                else (case when (rawTbl.status = "Resolved" and rawTbl.prev_act_ts is not NULL)
                            then round((JULIANDAY(rawTbl.performed_at) - JULIANDAY(rawTbl.prev_act_ts))* 86400/3600)
                            end)
        end) time_till_resolution,
        max(case when (rawTbl.status = "Pending" and rawTbl.sub_act_ts is not NULL)
                then round((JULIANDAY(rawTbl.sub_act_ts) - JULIANDAY(rawTbl.performed_at))* 86400/3600)
        end) time_to_first_response
    from metadata m ,
    (select main.*,
        prev.performed_at as prev_act_ts,
        sub.performed_at as sub_act_ts
    from temp.temp_tbl as main
    left join temp.temp_tbl as prev on (main.time_rank = prev.time_rank + 1 and main.ticket_id = prev.ticket_id)
    left join temp.temp_tbl as sub on (main.time_rank = sub.time_rank - 1 and main.ticket_id = sub.ticket_id)) as rawTbl
    group by ticket_id
            ''')
    rows = c.fetchall()

    return rows

if __name__ == '__main__':
    if os.path.exists(os.path.join("data","outputs")) == False:
        os.mkdir(os.path.join("data", "outputs"))

    parser = argparse.ArgumentParser(
        description="Load json file to sqlite database")
    parser.add_argument('-db', help='name of existing database')
    args = parser.parse_args()

    rows = sqlite_query(args)
    pd.DataFrame(rows,
                 columns=[
                     "ticket_id", "time_spent_open",
                     "time_spent_waiting_on_customer",
                     "time_spent_waiting_for_response", "time_till_resolution",
                     "time_to_first_response"
                 ]).to_csv('data/outputs/outputs.csv', index=False)
