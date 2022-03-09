from datetime import timedelta

from models import *
from common import db
from sqlalchemy import and_


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


def book_tables(
        unbooked_tables_id,
        user_id,
        no_of_2_chairs_table,
        no_of_4_chairs_table,
        no_of_6_chairs_table,
        no_of_12_chairs_table,
        start_datetime,
        end_datetime
):
    if no_of_2_chairs_table == 0 \
            and no_of_4_chairs_table == 0 \
            and no_of_6_chairs_table == 0 \
            and no_of_12_chairs_table == 0:
        return {
            'status': False,
            'message': 'Wrong inputs.'
        }

    end_datetime += timedelta(minutes=10)

    unbooked_tables_cur = UnbookedTables.query.filter(and_(UnbookedTables.id == unbooked_tables_id,
                                                           UnbookedTables.start_datetime <= start_datetime,
                                                           UnbookedTables.end_datetime >= end_datetime,
                                                           UnbookedTables.no_of_2_chairs_table >= no_of_2_chairs_table,
                                                           UnbookedTables.no_of_4_chairs_table >= no_of_4_chairs_table,
                                                           UnbookedTables.no_of_6_chairs_table >= no_of_6_chairs_table,
                                                           UnbookedTables.no_of_12_chairs_table >= no_of_12_chairs_table)
                                                      )

    if unbooked_tables_cur.count() == 0:
        return {
            'status': False,
            'message': 'unbooked tables are not available.'
        }

    unbooked_tables_obj = unbooked_tables_cur[0]
    restaurant_id = unbooked_tables_obj.restaurant_id

    new_unbooked_tables_obj_list = get_new_unbooked_tables_obj_list_after_booking(unbooked_tables_obj, start_datetime,
                                                                                  end_datetime)

    for new_unbooked_tables_obj in new_unbooked_tables_obj_list:
        db.session.add(new_unbooked_tables_obj)

    if no_of_2_chairs_table != unbooked_tables_obj.no_of_2_chairs_table \
            or no_of_4_chairs_table != unbooked_tables_obj.no_of_4_chairs_table \
            or no_of_6_chairs_table != unbooked_tables_obj.no_of_6_chairs_table \
            or no_of_12_chairs_table != unbooked_tables_obj.no_of_12_chairs_table:
        unbooked_tables_obj.start_datetime = start_datetime
        unbooked_tables_obj.end_datetime = end_datetime
        unbooked_tables_obj.no_of_2_chairs_table -= no_of_2_chairs_table
        unbooked_tables_obj.no_of_4_chairs_table -= no_of_4_chairs_table
        unbooked_tables_obj.no_of_6_chairs_table -= no_of_6_chairs_table
        unbooked_tables_obj.no_of_12_chairs_table -= no_of_12_chairs_table
        db.session.add(unbooked_tables_obj)
    else:
        db.session.delete(unbooked_tables_obj)

    booked_tables_obj = BookedTables(restaurant_id=restaurant_id,
                                     user_id=user_id,
                                     no_of_2_chairs_table=no_of_2_chairs_table,
                                     no_of_4_chairs_table=no_of_4_chairs_table,
                                     no_of_6_chairs_table=no_of_6_chairs_table,
                                     no_of_12_chairs_table=no_of_12_chairs_table,
                                     start_datetime=start_datetime,
                                     end_datetime=end_datetime
                                     )
    db.session.add(booked_tables_obj)
    db.session.commit()
    db.session.flush()

    return {
        'status': True
    }


def get_booked_tables_for_restaurant(restaurant_id):
    tables = [i.to_dict() for i in BookedTables.query.filter_by(restaurant_id=restaurant_id)]
    return tables


def get_booked_tables_for_user(user_id):
    tables = [i.to_dict() for i in BookedTables.query.filter_by(user_id=user_id)]
    return tables


def get_unbooked_tables(unbooked_tables_id):
    tables_obj = db.engine.execute(f"""
    select id, restaurant_id, start_datetime, DATETIME(end_datetime, '-10 minutes') as 'end_datetime',
    unbooked_tables.no_of_2_chairs_table,
    unbooked_tables.no_of_4_chairs_table,
    unbooked_tables.no_of_6_chairs_table,
    unbooked_tables.no_of_12_chairs_table,
    (2*unbooked_tables.no_of_2_chairs_table+
    4*unbooked_tables.no_of_4_chairs_table+
    6*unbooked_tables.no_of_6_chairs_table+
    12*unbooked_tables.no_of_12_chairs_table) as capacity from unbooked_tables 
    where id={unbooked_tables_id}
    """)
    keys = tables_obj.keys()
    tables = tables_obj.fetchall()
    tables = [dict(zip(keys, t)) for t in tables]
    return tables[0]


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


def get_unbooked_tables_with_party_size_and_duration(party_size, duration, start_datetime, end_datetime):
    if duration is None:
        return get_unbooked_tables_with_party_size(party_size)
    end_datetime += timedelta(minutes=10)
    tables_obj = db.engine.execute(f"""
    select unbooked_tables.id, restaurant.name, STRFTIME('%d/%m/%Y, %H:%M', start_datetime) as 'from', 
    STRFTIME('%d/%m/%Y, %H:%M', DATETIME(end_datetime, '-10 minutes')) as 'to', 
    unbooked_tables.no_of_2_chairs_table, 
    unbooked_tables.no_of_4_chairs_table,
    unbooked_tables.no_of_6_chairs_table,
    unbooked_tables.no_of_12_chairs_table,
    (2*unbooked_tables.no_of_2_chairs_table+
    4*unbooked_tables.no_of_4_chairs_table+
    6*unbooked_tables.no_of_6_chairs_table+
    12*unbooked_tables.no_of_12_chairs_table) as capacity
    from unbooked_tables
    join restaurant on restaurant.id=unbooked_tables.restaurant_id
    where Cast((JulianDay(end_datetime) - JulianDay(start_datetime)) * 24 * 60 * 60 As Integer)>={duration} 
    and (
        '{start_datetime}'<=start_datetime and '{end_datetime}'>=end_datetime 
        or 
            (
                (start_datetime<='{start_datetime}' and end_datetime<='{end_datetime}' 
                and JulianDay('{start_datetime}')+{duration}.0/(24*60*60)<=JulianDay(end_datetime))
            or 
                (start_datetime>='{start_datetime}' and end_datetime>='{end_datetime}'
                and JulianDay('{end_datetime}')-{duration}.0/(24*60*60)>=JulianDay(start_datetime))
            or 
                ('{start_datetime}'>=start_datetime and '{end_datetime}'<=end_datetime 
                 and JulianDay('{start_datetime}')+{duration}.0/(24*60*60)<=JulianDay('{end_datetime}'))
            ) 
        
    )
    and capacity>={party_size}""")
    keys = tables_obj.keys()
    tables = tables_obj.fetchall()
    tables = [dict(zip(keys, t)) for t in tables]
    return tables


def get_restaurant_details(restaurant_id):
    return Restaurant.query.filter_by(id=restaurant_id).first().to_dict()


def get_user_bookings(user_id):
    tables_obj = db.engine.execute(f"""
       select booked_tables.id, restaurant.name, STRFTIME('%d/%m/%Y, %H:%M', start_datetime) as 'from', 
       STRFTIME('%d/%m/%Y, %H:%M',  DATETIME(end_datetime, '-10 minutes')) as 'to', 
       booked_tables.no_of_2_chairs_table, 
       booked_tables.no_of_4_chairs_table,
       booked_tables.no_of_6_chairs_table,
       booked_tables.no_of_12_chairs_table,
       (2*booked_tables.no_of_2_chairs_table+
       4*booked_tables.no_of_4_chairs_table+
       6*booked_tables.no_of_6_chairs_table+
       12*booked_tables.no_of_12_chairs_table) as capacity
       from booked_tables
       join restaurant on restaurant.id=booked_tables.restaurant_id
       where booked_tables.user_id={user_id}""")
    keys = tables_obj.keys()
    tables = tables_obj.fetchall()
    tables = [dict(zip(keys, t)) for t in tables]
    return tables  # return [i.to_dict() for i in BookedTables.query.filter_by(user_id=user_id)]


def delete_booking(booked_tables_id):
    '''
    6-7 booked

    7-11
    5-6

    any row having start_datetime == 7 then update that row for example update 7-11 to 6-11
    any row having end_datetime == 6 the update that row for example update 6-11 to 5-11

    '''


def python_datetime_to_html_input_tag_datetime_local(dt):
    return dt.strftime("%Y-%m-%dT%H:%M")
