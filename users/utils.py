

def get_userdata(user):
    return {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'mobile_number': user.mobile_number,
        'is_superuser': user.is_superuser,
        'is_customer': user.is_customer,
        'profile_picture': user.profile_picture.url if user.profile_picture else user.profile_picture_url or '',
        'last_login': user.last_login,
    }


def convert_timestamp_to_date_time(timestamp):
    import datetime
    if timestamp:
        return datetime.datetime.fromtimestamp(timestamp)

    return timestamp
