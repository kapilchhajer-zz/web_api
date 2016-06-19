from app import db
from app import cel
from app.models.User import User
from app.helpers import accounts_request_helpers
from app.constants import PUSH_CHANNEL_PREFIX
from app import pusher_client


@cel.task(max_retries=3, default_retry_delay=20)
def update_user_details(user_id, app_url):
    try:
        user = User.query.filter(User.id == user_id).first()
        if not user:
            raise Exception('No such user in system')
        if user.email:
            key = 'email'
            value = user.email
        elif user.pracc_id:
            key = 'pracc_id'
            value = user.pracc_id
        elif user.phone:
            key = 'phone'
            value = user.phone
        user_info = accounts_request_helpers.get_user_info(key, value, app_url)
        if user_info:
            user.email = user_info['Email']
            user.pracc_id = user_info['PractoAccountId']
            user.phone = user_info['Mobile']
            user.name = user_info['Name']
            db.session.add(user)
            db.session.commit()
    except Exception as e:
        raise update_user_details.retry(exc=e)


@cel.task
def notify_followups(user_ids):
    for _id in user_ids:
        update_message = '{"command":"updateReminders"}'
        channel = PUSH_CHANNEL_PREFIX + str(_id)
        pusher_client.publish(channel, update_message)
