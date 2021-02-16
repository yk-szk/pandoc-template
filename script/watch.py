#!/usr/bin/python
from pathlib import Path
import time
import subprocess
import argparse

from logzero import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path, always=False):
        super().__init__()
        self.input_path = input_path
        self.args = ['make', str(output_path)]
        if always:
            self.args.append('-B')
        logger.debug('Command: %s', ' '.join(self.args))

    def on_modified(self, event):
        filepath = Path(event.src_path)
        if filepath.name != self.input_path.name:
            return

        logger.info(filepath)
        subprocess.check_call(self.args)


def main():
    parser = argparse.ArgumentParser(
        description='Watch changes to md and generate html.')
    parser.add_argument('output',
                        help="Output filename. default : %(default)s",
                        metavar='<output>',
                        default='manuscript.html',
                        nargs='?')
    parser.add_argument('-B',
                        '--always',
                        help='Add -B option to the make command',
                        action='store_true')

    args = parser.parse_args()
    output_fn = Path(args.output)
    input_fn = output_fn.with_suffix('.md')
    event_handler = MyHandler(input_fn, output_fn, args.always)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    logger.info('Start watching %s', input_fn)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info('KeyboardInterrupt')
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
