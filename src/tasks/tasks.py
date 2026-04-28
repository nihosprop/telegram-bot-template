import logging
import uuid

from datetime import UTC, datetime

from aiogram import Bot
from dishka.integrations.taskiq import FromDishka, inject

from core.main_config import Config

from .broker import broker
from .mixins import MyScheduledTask

logger = logging.getLogger(__name__)
ai_logger = logging.getLogger('ai.mentor.replies')


@broker.task
@inject(patch_module=True)
async def sends_last_month_stats(
    bot: FromDishka[Bot],
    config: FromDishka[Config],
) -> None:
    logger.debug('Entry')

    now = datetime.now(UTC)
    await bot.send_message(
        chat_id=config.bot.admins[0],
        text=f'Example month stats.Time sending: {now}.',
    )
    logger.debug('Exit')


# TODO: move _schedule_id
def _schedule_id(task_name: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, task_name))


# TODO: move settings
STATIC_TASKS = [
    MyScheduledTask(
        task_name=sends_last_month_stats.task_name,
        schedule_id=_schedule_id(task_name=sends_last_month_stats.task_name),
        cron='15 0 1 * *',
    ),
]
