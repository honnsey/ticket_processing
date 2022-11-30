import argparse
import os
import json
import pandas as pd
from sqlalchemy import create_engine

def export_json(params):

    db_name = params.db
    #============= Creat SQLAlchemy Engine =============
    engine = create_engine(f'sqlite:///data/database/{db_name}',
                        echo=False)

    #============= load json file =============

    json_file_name = [name for name in os.listdir(os.path.join("data","json"))
                    if name.endswith(".json")][0]
    json_path = os.path.join("data", "json",json_file_name)
    with open(json_path) as json_file:
        json_dict = json.load(json_file)


    #============= export metadata from json file =============
    metadata_df = pd.DataFrame.from_dict(json_dict['metadata'], orient='index').T
    metadata_df['start_at'] = pd.to_datetime(metadata_df['start_at'],
                                                 dayfirst=True,
                                                 utc=True,
                                                 format="%d-%m-%Y %H:%M:%S %z")
    metadata_df['end_at'] = pd.to_datetime(metadata_df['end_at'],
                                             dayfirst=True,
                                             utc=True,
                                             format="%d-%m-%Y %H:%M:%S %z")
    metadata_df.to_sql('metadata', engine, if_exists='replace', index=False)


    #============= export activities_data from json file =============

    # convert data into pd df
    df_raw = pd.DataFrame(json_dict['activities_data'])
    # unpack column "activity"
    df_raw = pd.concat([df_raw.drop(columns=['activity']), df_raw.activity.apply(pd.Series)],
                        axis=1)
    # unpack column "note", rename for clarity
    if 'note' in df_raw.columns:
        df_raw = pd.concat([df_raw.drop(columns='note'),
                            df_raw.note.apply(pd.Series).drop(columns=0).rename(columns=lambda x: "_".join(["note", x]))],
                        axis=1)

    df_raw['performed_at'] = pd.to_datetime(df_raw['performed_at'],
                                            dayfirst=True,
                                            utc=True,
                                            format="%d-%m-%Y %H:%M:%S %z")
    df_raw.to_sql('activities_data', engine, if_exists='replace', index=False)


if __name__ == '__main__':
    if os.path.exists(os.path.join("data", "database")) == False:
        os.mkdir(os.path.join("data", "database"))

    parser = argparse.ArgumentParser(description="Load json file to sqlite database")
    parser.add_argument('-db', help='name of new database')
    args = parser.parse_args()

    export_json(args)
