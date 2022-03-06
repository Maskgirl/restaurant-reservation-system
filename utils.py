from models import *
from common import db


def get_all_restaurants():
    all_restaurants = [i.to_dict() for i in Restaurant.query.all()]
    return all_restaurants


def get_unbooked_tables_for_restaurant(restaurant_id):
    tables = [i.to_dict() for i in UnbookedTables.query.filter_by(restaurant_id=restaurant_id)]
    return tables


def get_new_unbooked_tables_obj_list_after_booking(unbooked_tables_obj, start_datetime, end_datetime):
    unbooked_tables_dict = unbooked_tables_obj.to_dict()

    new_unbooked_tables_obj_list = []
    if unbooked_tables_dict['start_datetime'] == str(start_datetime) \
            and unbooked_tables_dict['end_datetime'] != str(end_datetime):
        new_unbooked_tables_obj_list.append(UnbookedTables(restaurant_id=unbooked_tables_obj.restaurant_id,
                                                           no_of_2_chairs_table=unbooked_tables_obj.no_of_2_chairs_table,
                                                           no_of_4_chairs_table=unbooked_tables_obj.no_of_4_chairs_table,
                                                           no_of_6_chairs_table=unbooked_tables_obj.no_of_6_chairs_table,
                                                           no_of_12_chairs_table=unbooked_tables_obj.no_of_12_chairs_table,
                                                           start_datetime=end_datetime,
                                                           end_datetime=unbooked_tables_obj.end_datetime
                                                           ))
    elif unbooked_tables_dict['end_datetime'] == str(end_datetime) \
            and unbooked_tables_dict['start_datetime'] != str(start_datetime):
        new_unbooked_tables_obj_list.append(UnbookedTables(restaurant_id=unbooked_tables_obj.restaurant_id,
                                                           no_of_2_chairs_table=unbooked_tables_obj.no_of_2_chairs_table,
                                                           no_of_4_chairs_table=unbooked_tables_obj.no_of_4_chairs_table,
                                                           no_of_6_chairs_table=unbooked_tables_obj.no_of_6_chairs_table,
                                                           no_of_12_chairs_table=unbooked_tables_obj.no_of_12_chairs_table,
                                                           start_datetime=unbooked_tables_obj.start_datetime,
                                                           end_datetime=start_datetime
                                                           ))
    elif unbooked_tables_dict['end_datetime'] != str(end_datetime) \
            and unbooked_tables_dict['start_datetime'] != str(start_datetime):
        new_unbooked_tables_obj_list.append(UnbookedTables(restaurant_id=unbooked_tables_obj.restaurant_id,
                                                           no_of_2_chairs_table=unbooked_tables_obj.no_of_2_chairs_table,
                                                           no_of_4_chairs_table=unbooked_tables_obj.no_of_4_chairs_table,
                                                           no_of_6_chairs_table=unbooked_tables_obj.no_of_6_chairs_table,
                                                           no_of_12_chairs_table=unbooked_tables_obj.no_of_12_chairs_table,
                                                           start_datetime=end_datetime,
                                                           end_datetime=unbooked_tables_obj.end_datetime
                                                           ))
        new_unbooked_tables_obj_list.append(UnbookedTables(restaurant_id=unbooked_tables_obj.restaurant_id,
                                                           no_of_2_chairs_table=unbooked_tables_obj.no_of_2_chairs_table,
                                                           no_of_4_chairs_table=unbooked_tables_obj.no_of_4_chairs_table,
                                                           no_of_6_chairs_table=unbooked_tables_obj.no_of_6_chairs_table,
                                                           no_of_12_chairs_table=unbooked_tables_obj.no_of_12_chairs_table,
                                                           start_datetime=unbooked_tables_obj.start_datetime,
                                                           end_datetime=start_datetime
                                                           ))

    return new_unbooked_tables_obj_list

    # tables = BookedTables.query.filter_by(restaurant_id=restaurant_id).to_dict()
    # return tables


def get_booked_tables_for_restaurant(restaurant_id):
    tables = [i.to_dict() for i in BookedTables.query.filter_by(restaurant_id=restaurant_id)]
    return tables


def get_booked_tables_for_user(user_id):
    tables = [i.to_dict() for i in BookedTables.query.filter_by(user_id=user_id)]
    return tables


def get_unbooked_tables_with_party_size(party_size):
    tables_obj = db.engine.execute(f"select * from unbooked_tables "
                                   f"where "
                                   f"2*no_of_2_chairs_table+"
                                   f"4*no_of_4_chairs_table+"
                                   f"6*no_of_6_chairs_table+"
                                   f"12*no_of_12_chairs_table>={party_size}")
    keys = tables_obj.keys()
    tables = tables_obj.fetchall()
    tables = [dict(zip(keys, t)) for t in tables]
    return tables


def get_unbooked_tables_with_party_size_and_duration(party_size, duration):
    if duration is None:
        return get_unbooked_tables_with_party_size(party_size)
    tables_obj = db.engine.execute(f"select *,  Cast ((JulianDay(end_datetime) - JulianDay(start_datetime)) * "
                                   f"24 * 60 * 60 As Integer) AS duration "
                                   f"from unbooked_tables "
                                   f"where duration>={duration} and "
                                   f"2*no_of_2_chairs_table+"
                                   f"4*no_of_4_chairs_table+"
                                   f"6*no_of_6_chairs_table+"
                                   f"12*no_of_12_chairs_table>={party_size}")
    keys = tables_obj.keys()
    tables = tables_obj.fetchall()
    tables = [dict(zip(keys, t)) for t in tables]
    return tables
