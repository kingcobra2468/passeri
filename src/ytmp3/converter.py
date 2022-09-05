import os
import asyncio
import pathlib

import editdistance

from autoid3.auto_id3_worker import AutoID3Worker
import yt_dlp


class Converter:
    """Converter downloads Youtube links as MP3s. All mp3s will
    also have their ID3 data populated (cover, title, album) via
    autoid3 (which internally utilizes Shazam).
    """
    YDL_OPTS = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }
        ],
    }

    def __init__(self, links, download_path):
        """Constructor.

        Args:
            links (List[str])): A list of Youtube links.
            download_path (str): The path where mp3s will temporary be downloaded to.
        """
        self._links = links
        self._download_path = download_path
        self.YDL_OPTS['outtmpl'] = os.path.join(
            download_path, '%(title)s.%(ext)s')

    def download(self):
        """Downloads the given links as mp3s and applies autoid3 to them.

        Returns:
            List[str]: A list of paths to the output mp3s.
        """
        with yt_dlp.YoutubeDL(self.YDL_OPTS) as ydl:
            ydl.download(self._links)

        files = self._get_files()
        # get list of actual files on filesystem
        files_created = [os.path.join(self._download_path, file) for file in os.listdir(
            self._download_path) if file.endswith(".mp3")]

        # check if all files exist
        for idx, file in enumerate(files):
            if pathlib.Path(file).exists():
                continue

            # attempt to repair files where names dont match
            for file_created in files_created:
                # if edit distance between actual and current file is less than
                # threshold, then fix the file
                if editdistance.eval(file_created, file) < 10:
                    files[idx] = file_created
                    break

        self._populate_metadata(files)

        return files

    def clean(self):
        """Removes the downloaded files from the filesystem.
        """
        files = self._get_files()

        for file in files:
            pathlib.Path(file).unlink()

    async def __populate_metadata(self, files):
        """Populates the ID3 metadata of the mp3s.

        Args:
            files (List[str]): A list of paths to the mp3s
        """
        mp3_queue = asyncio.Queue()

        for file in files:
            with open(file, 'rb') as f:
                pass
            mp3_queue.put_nowait(file)

        parser = AutoID3Worker(mp3_queue)
        await parser.process_track()

    def _populate_metadata(self, files):
        """Populates the ID3 metadata of the mp3s.

        Args:
            files (List[str]): A list of paths to the mp3s
        """
        asyncio.run(self.__populate_metadata(files))

    def _get_files(self):
        """Gets the paths to output mp3s.

        Returns:
            (List[str]): A list of paths to the output mp3s
        """
        filenames = []
        with yt_dlp.YoutubeDL(self.YDL_OPTS) as ydl:
            for link in self._links:
                info_dict = ydl.extract_info(link, download=False)
                title = info_dict.get('title', None)
                filenames.append(os.path.join(
                    self._download_path, f'{title}.mp3'))

        return filenames

