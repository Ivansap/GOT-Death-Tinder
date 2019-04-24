from fcm_django.models import FCMDevice


def send_notification(user=None, users=None, title='Test', body='Test message'):
    base_users = []
    if users is not None:
        base_users = [user.user for user in users.all()]

    if user is not None:
        base_users = [user.user]
    devices = FCMDevice.objects.filter(user__in=base_users, active=True)

    if devices:
        devices.send_message(title=title, body=body)
