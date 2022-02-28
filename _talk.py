from datetime import datetime

from common import db
from common import create_app

restaurant_id = 1
user_id = 1
no_of_2_chairs_table = 1
no_of_4_chairs_table = 0
no_of_6_chairs_table = 0
no_of_12_chairs_table = 0
start_timestamp = datetime(2022, 2, 28, 6, 0, 0, 0)
end_timestamp = datetime(2022, 2, 28, 7, 0, 0, 0)

available_tables_list = list(db.engine.execute(f"select * from unbooked_tables"
                                               f" where start_timestamp<='{start_timestamp}'"
                                               f" and end_timestamp>='{end_timestamp}'"
                                               f" and no_of_2_chairs_table>={no_of_2_chairs_table}"
                                               f" and no_of_4_chairs_table>={no_of_4_chairs_table}"
                                               f" and no_of_6_chairs_table>={no_of_6_chairs_table}"
                                               f" and no_of_12_chairs_table>={no_of_12_chairs_table}"))
