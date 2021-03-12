from google.cloud import bigquery
from typing import Any


class GBQClient:
    """
    This connector class is for creating Google Big Query operations.
    As prerequisite, one needs to login into gcloud and specific authentication mechanisms.
    :params 
        - `**kwargs` : Various settings for GBQ client object
    """

    def __init__(self, **kwargs):
        # Need to comment below line due to lack of GOOGLE_APPLICATION_CREDENTIALS
        # self.client = bigquery.Client(**kwargs)
        pass

    def insert_row_in_table(self, **kwargs):
        # Method yet to implement
        pass

    def insert_rows_in_table(
        self, table_id: str, rows_to_insert: list, fake_call: bool = True
    ) -> list:
        """
        To insert multiple rows into a Google Big query table
        specially useful for streaming insert
        :params
            - table_id : table ID to append these rows e.g. `project.dataset.table`
            - rows_to_insert : List of dictionary objects, each representing one record
            - fake_call : To bypass actual call for Google Big Query
        
        :returns
            - errors: List of any errors in inserting specific records.
                      If all rows added, then it is an empty list i.e. [] as value
        """
        # TODO: Check if table exists or not
        if fake_call is False:
            # Need to comment due to lack to proper client object
            # errors = self.client.insert_rows_json(table_id, rows_to_insert)
            errors: list = []
            if errors:
                raise Exception("Insertion failed for some rows:", errors)

            return errors
        else:
            print("New Rows Inserted:", len(rows_to_insert))
            return []
