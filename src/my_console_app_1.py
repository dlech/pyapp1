import asyncio
import functools
import logging
import sys
import time

import winsdk.windows.applicationmodel as wam
import winsdk.windows.ui.notifications as wun
import winsdk.windows.ui.notifications.management as wunm

logger = logging.getLogger(__name__)


def on_notification_changed(
    sender: wunm.UserNotificationListener, args: wun.UserNotificationChangedEventArgs
):
    logger.info(
        "%r, id: %d, kind: %s", sender, args.user_notification_id, args.change_kind.name
    )

    if args.change_kind == wun.UserNotificationChangedKind.REMOVED:
        return

    notification = sender.get_notification(args.user_notification_id)

    if notification is None:
        logger.warning("could not get notification")
        return

    logger.info(
        "created: %s",
        notification.creation_time.astimezone(),
    )
    logger.info("expires: %s", notification.notification.expiration_time.astimezone())

    try:
        logger.info("name: %s", notification.app_info.display_info.display_name)
    except OSError as ex:
        if ex.winerror == -2147467263:  # Not implemented (0x80004001)
            logger.warning("app_info not available!")
        else:
            raise


async def main():
    loop = asyncio.get_running_loop()
    listener: wunm.UserNotificationListener = (
        wunm.UserNotificationListener.get_current()
    )
    token = listener.add_notification_changed(
        functools.partial(loop.call_soon_threadsafe, on_notification_changed)
    )

    try:
        toast_xml = wun.ToastNotificationManager.get_template_content(
            wun.ToastTemplateType.TOAST_TEXT02
        )
        launch_attr = toast_xml.create_attribute("launch")
        launch_attr.value = "--toast-activated"
        toast_node = toast_xml.select_single_node("/toast")
        toast_node.attributes.set_named_item(launch_attr)

        app_info: wam.AppInfo = wam.AppInfo.get_current()
        logger.info(app_info.app_user_model_id)
        notifier = wun.ToastNotificationManager.create_toast_notifier(
            app_info.app_user_model_id
        )
        toast = wun.ToastNotification(toast_xml)
        notifier.show(toast)

        await asyncio.Event().wait()
    finally:
        listener.remove_notification_changed(token)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("args: %r", sys.argv)

    if "--toast-activated" in sys.argv:
        time.sleep(5)
        sys.exit(0)

    asyncio.run(main())
