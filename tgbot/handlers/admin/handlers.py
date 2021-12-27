from datetime import timedelta

import telegram
from django.utils.timezone import now
from telegram import ParseMode, Update, bot, message
from telegram.ext import CallbackContext, MessageHandler, Filters

from tgbot.handlers.admin import static_text
from tgbot.handlers.admin.static_text import msg_for_invite, msg_after_invite
from tgbot.handlers.admin.utils import _get_csv_from_qs_values
from tgbot.models import User, MeetUp


def admin(update: Update, context: CallbackContext) -> None:
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)
    if not u.is_admin:
        update.message.reply_text(static_text.only_for_admins)
        return
    update.message.reply_text(static_text.secret_admin_commands)


def stats(update: Update, context: CallbackContext) -> None:
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)
    if not u.is_admin:
        update.message.reply_text(static_text.only_for_admins)
        return

    text = static_text.users_amount_stat.format(
        user_count=User.objects.count(),  # count may be ineffective if there are a lot of users.
        active_24=User.objects.filter(updated_at__gte=now() - timedelta(hours=24)).count()
    )

    update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


def export_users(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)
    if not u.is_admin:
        update.message.reply_text(static_text.only_for_admins)
        return

    # in values argument you can specify which fields should be returned in output csv
    users = User.objects.all().values()
    csv_users = _get_csv_from_qs_values(users)
    context.bot.send_document(chat_id=u.user_id, document=csv_users)


def get_meetups(update: Update, context: CallbackContext) -> None:
    msg = update.message.text
    if update.message.text == "/get_meetup":
        s = 'Митапы на сегодня' + '\r\n\r\n' + 'Выберете порядковый номер митапа' + '\r\n\r\n'
        for mt in MeetUp.objects.order_by('pk'):
            s += str(mt.pk) + ". " + mt.title + '\r\n' + str(mt.date) + '\r\n\r\n'
        update.message.reply_text(s)
    get_meetup_by_id(update, context)


def get_meetup_by_id(update: Update, context: CallbackContext):
    ids = MeetUp.objects.filter().values_list('pk', flat=True)
    s = ""
    global meetupId
    for mt in ids:
        if update.message.text == str(mt):
            meetupId = update.message.text
            meetupObj = MeetUp.objects.get(pk=mt)
            s += str(meetupObj.pk) + ". " + meetupObj.title + '\r\n' \
                 + meetupObj.description + '\r\n' + msg_for_invite
            update.message.reply_text(s)


def invite_to_meetup(update: Update, context: CallbackContext) -> None:
    meetupObj = MeetUp.objects.get(pk=meetupId)
    user_id = update.message.from_user.id
    user = User.objects.get(user_id=user_id)
    user.meetups.add(meetupObj)

    users = User.objects.filter(meetups__in=[meetupId]).count()
    amount = meetupObj.amountListeners
    free = int(amount) - int(users)

    msg = msg_after_invite + '\r\n\r\n' + "Оставшееся количество свободных мест: " + str(free)
    update.message.reply_text(msg)

