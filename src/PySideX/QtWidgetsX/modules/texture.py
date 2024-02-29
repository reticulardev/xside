#!/usr/bin/env python3
import logging
import os
import pathlib
import subprocess
import sys

from PIL import Image, ImageFilter

BASE_DIR = pathlib.Path(__file__).resolve().parent
sys.path.append(BASE_DIR.as_posix())

import cli


class Window(object):
	def __init__(self):
		pass


class Desktop(object):
	def __init__(self):
		pass


class Texture(object):
	"""..."""
	def __init__(
			self,
			toplevel_id: str,
			screen_width: int,
			screen_height: int,
			shadow_size: int) -> None:
		"""..."""
		self.__toplevel_id = toplevel_id.replace('0x', '0x0')
		self.__screen_w = screen_width
		self.__screen_h = screen_height
		self.__shadow_size = shadow_size
		self.__path = os.path.join(BASE_DIR, 'textures')
		self.__wmctrl_lg = cli.output_by_args(["wmctrl", "-lG"])
		self.__desktop = Desktop()
		self.__windows = self.__output_screens()

	def create(self):
		if self.__screenshot():
			imgdesk = Image.open(
				os.path.join(self.__path, self.__desktop.id_ + '.png'))

			for win in self.__windows:
				urlfile = os.path.join(self.__path, win.id_ + '.png')
				if os.path.isfile(urlfile) and win.type_ != '-1':
					if win.id_ != self.__toplevel_id:
						imgwin = Image.open(urlfile)
						imgdesk.paste(imgwin, (int(win.x), int(win.y)))

			# imgdesk.save(os.path.join(self.__path, 'desktopscreen.png'))
			for wd in self.__windows:
				if wd.id_ == self.__toplevel_id:
					x, y, w, h = int(wd.x), int(wd.y), int(wd.w), int(wd.h)
					box = (
						x + self.__shadow_size, y + self.__shadow_size,
						x + w - self.__shadow_size,
						y + h - self.__shadow_size)
					region = imgdesk.crop(box)
					out = region.filter(ImageFilter.GaussianBlur(radius=30))
					out.save(os.path.join(self.__path, 'texture_region.png'))

	def __screenshot(self) -> bool:
		"""..."""
		if self.__windows:
			self.__windows.reverse()
			for window in self.__windows:
				cli.output_by_args([
					'import', '-window', window.id_, '-quality', '1',
					os.path.join(self.__path, window.id_ + '.png')])
			return True
		return False

	def __output_screens(self):
		windows_list = []
		if self.__wmctrl_lg:
			for win in self.__wmctrl_lg.split('\n'):
				w = Window()
				try:
					w.id_, w.type_, w.x, w.y, w.w, w.h, *_ = win.split()
				except Exception as err:
					logging.error(err)
				else:
					if w.type_ == '-1' and w.x == '0' and w.y == '0':
						if w.w == str(self.__screen_w) and w.h == str(
								self.__screen_h):
							self.__desktop.id_ = w.id_
					windows_list.append(w)
		return windows_list


if __name__ == '__main__':
	tex = Texture('0x3800007', 1366, 768, 8)
	tex.create()
