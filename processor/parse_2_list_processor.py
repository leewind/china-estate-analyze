# -*- coding: utf-8 -*-
import pymongo
import urllib
import pymysql
import pandas as pd
import numpy as np
# from mysql_util import get_mysql_db_connection, query_fid, query
from mongodb_util import get_mongo_db_client


def main():

    client = get_mongo_db_client()
    db = client["ke"]

    records = db["kelist"].find({})
    print()


    # for r in records:
    #     print(r['content'])

        #     home_df = pd.DataFrame(r['data']['home_datadetail'])
        #     if 'score' not in home_df.columns.values:
        #         continue

        #     home_df = home_df[home_df['score'] != '-']
        #     parse_and_insert(r, home_df, 'homestanding')

        #     away_df = pd.DataFrame(r['data']['away_datadetail'])
        #     if 'score' not in away_df.columns.values:
        #         continue

        #     away_df = away_df[away_df['score'] != '-']
        #     parse_and_insert(r, home_df, 'awaystanding')

    client.close()


if __name__ == "__main__":
    main()
