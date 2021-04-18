import logging
import os
from telegram.poll import Poll

from django.core.management.base import BaseCommand, CommandError
from telegram.error import InvalidToken
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram import ReplyKeyboardMarkup


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    @classmethod
    def _get_token(cls):
        token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
        logger.info(f'token={token}')
        if token == '':
            logger.warning('Possibly, TELEGRAM_BOT_TOKEN is not set')
        return token

    @classmethod
    def _get_updater(cls):
        """
        Try to get telegram API and initialize Updater object.
        Raise exception if API TOKEN is invalid.
        """
        try:
            updater = Updater(token=cls._get_token(), use_context=True)
        except InvalidToken as e:
            raise CommandError(
                'Can not init telegram API, '
                'because telegram authentication token is invalid'
            )
        else:
            return updater

    @staticmethod
    def start(update, context):
        logger.warning(update.effective_user.username)
        logger.warning(update.effective_user.first_name)
        logger.warning(update.effective_user.last_name)
        # context.bot.send_message(
        #     chat_id=update.effective_chat.id,
        #     text=f'Здарова {update.effective_user.first_name} \n'
        #          f'https://f4.bcbits.com/img/0007035661_10.jpg'
        # )
        reply_keyboard = [['Boy', 'Girl', 'Other']]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        # context.bot.send_message(
        #     chat_id=update.effective_chat.id,
        #     text=f'{update.effective_user.first_name} послушай',
        #     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        # )
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo='https://f4.bcbits.com/img/0007035661_10.jpg'
        )
        context.bot.send_poll(
            chat_id=update.effective_chat.id,
            question='What artist?',
            options=['Burial', 'Mixan'],
            type='quiz',
            correct_option_id=0
        )

    def handle(self, *args, **options):
        logger.warning('Starting bot')
        updater = self._get_updater()
        dispatcher = updater.dispatcher
        start_handler = CommandHandler('start', self.start)
        dispatcher.add_handler(start_handler)
        updater.start_polling()
