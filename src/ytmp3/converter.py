import os
import asyncio

from autoid3.auto_id3_worker import AutoID3Worker
import youtube_dl


class Converter:
    YDL_OPTS = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    def __init__(self, links, download_path):
        self._links = links
        self._download_path = download_path
        self.YDL_OPTS["outtmpl"] = os.path.join(download_path, "%(title)s.%(ext)s")

    def download(self):
        with youtube_dl.YoutubeDL(self.YDL_OPTS) as ydl:
            ydl.download(self._links)

        files = self._get_files()
        self._populate_metadata(files)

        return files

    async def __populate_metadata(self, files):
        mp3_queue = asyncio.Queue()

        for file in files:
            mp3_queue.put_nowait(file)

        parser = AutoID3Worker(mp3_queue)
        await parser.process_track()

    def _populate_metadata(self, files):
        asyncio.run(self.__populate_metadata(files))

    def _get_files(self):
        filenames = []
        with youtube_dl.YoutubeDL(self.YDL_OPTS) as ydl:
            for link in self._links:
                info_dict = ydl.extract_info(link, download=False)
                title = info_dict.get("title", None)

                filenames.append(os.path.join(self._download_path, f"{title}.mp3"))

        return filenames
