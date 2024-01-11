from typing import TYPE_CHECKING

import os
import time
import threading
import asyncio
from asgiref.sync import sync_to_async

import sys

from django.utils import timezone
from django.apps import AppConfig


if TYPE_CHECKING:
    from .models import token
    from .models import player

from inshack.settings import BASE_DIR

class TokenCleaner(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        from .models import token
        print(f"TokenCleaner started successfully at {timezone.now()}")

        while True:
            # get the timestamp of 1h ago
            timestamp = timezone.now() - timezone.timedelta(hours=1)
            # delete tokens that have been created more than 1h ago
            outdated_tokens = [t for t in token.objects.all() if t.date < timestamp]
            for t in outdated_tokens:
                t.delete()
                print(f"Token {t} deleted at {timezone.now()}")

            time.sleep(60)


class FileCleaner(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.stop_event = asyncio.Event()  # Événement pour arrêter la boucle asynchrone
        self.start()

    def run(self):
        print(f"FileCleaner started successfully at {timezone.now()}")
        asyncio.run(self.run_asynchronously())

    async def run_asynchronously(self):
        try:
            while not self.stop_event.is_set():
                await self.delete_files()
                await asyncio.sleep(3600)
        except asyncio.CancelledError:
            pass  # Ignore the CancelledError when the thread is stopped

    @sync_to_async
    def delete_file_sync(self, file):
        os.remove(file)
        print(f"File {file} deleted at {timezone.now()}")

    async def delete_files(self):
        async for file in self.get_files_to_delete():
            if file is not None:
                await self.delete_file_sync(file)

    async def get_files_to_delete(self):
        # Use sync_to_async for synchronous database queries
        profile_pictures = await sync_to_async(self.get_profile_pictures)()
        # get all unused profile pictures
        for file in await sync_to_async(self.get_profile_pictures_folder_files)():

            if file not in profile_pictures and file != str(BASE_DIR / 'media' / 'profile_pictures' / 'default.png'):
                yield BASE_DIR / file

    def get_profile_pictures(self):
        # Synchronous database query
        from .models import player
        return [p.profile_picture.name for p in player.objects.all() if p.profile_picture is not None]

    def get_profile_pictures_folder_files(self):
        # Synchronous filesystem operation
        profile_pictures_folder = BASE_DIR / 'media' / 'profile_pictures'
        return [str(profile_pictures_folder / f) for f in os.listdir(profile_pictures_folder)]

    def stop(self):
        self.stop_event.set()

