

def get_userdata(user):
    return {
        'username': user.username,
        'name': user.name,
        'email': user.email,
        'mobile_number': user.mobile_number,
        'gender': user.gender,
        'date_of_birth' : user.date_of_birth,
        'is_superuser': user.is_superuser,
        'is_customer': user.is_customer,
        'profile_picture': user.profile_picture.url if user.profile_picture else user.profile_picture_url or '',
        'last_login': user.last_login,
    }


def convert_timestamp_to_date_time(timestamp):
    import datetime
    if timestamp:
        updated_timestamp = timestamp / 1000
        return datetime.datetime.fromtimestamp(updated_timestamp)

    return timestamp
