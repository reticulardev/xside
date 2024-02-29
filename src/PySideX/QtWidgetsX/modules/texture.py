#!/usr/bin/env python3
import logging
import os
import pathlib
import subprocess
import sys

from PIL import Image, ImageFilter, ImageEnhance

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
		self.__desktop = Desktop()
		self.__windows = self.__valid_windows()

	def create(self):
		if self.__screenshots():
			imgdesk = Image.open(
				os.path.join(self.__path, self.__desktop.id_ + '.png'))

			for win in self.__windows:
				urlfile = os.path.join(self.__path, win.id_ + '.png')
				if os.path.isfile(urlfile) and win.type_ != '-1':
					if win.id_ != self.__toplevel_id:
						imgwin = Image.open(urlfile)
						imgdesk.paste(imgwin, (int(win.x), int(win.y)))

			# imgdesk.save(os.path.join(self.__path, 'desktopscreen.png'))
			self.__windows.reverse()
			for wd in self.__windows:
				if wd.id_ == self.__toplevel_id:
					x, y, w, h = int(wd.x), int(wd.y), int(wd.w), int(wd.h)
					region = imgdesk.crop((x, y, x + w, y + h))
					out = region.filter(ImageFilter.GaussianBlur(radius=35))
					out = ImageEnhance.Brightness(out).enhance(0.8)
					out.save(os.path.join(self.__path, 'texture_region.png'))

	def __screenshots(self) -> bool:
		"""..."""
		if self.__windows:
			for window in self.__windows:
				cli.output_by_args([
					'import', '-window', window.id_, '-quality', '1',
					os.path.join(self.__path, window.id_ + '.png')])
			return True
		return False

	def __valid_windows(self):
		# wmctrl_lg: marks windows that are not windows using an '-1'
		# xprop_root: list windows in order (z-index)
		try:
			wmctrl_lg = cli.output_by_args(['wmctrl', '-lG']).split('\n')
			xprop_root = [
				x.split()[-1].replace('0x', '0x0') for x in [
					x for x in cli.output_by_args(
						['xprop', '-root']).split('\n')
					if '_NET_CLIENT_LIST_STACKING(WINDOW)' in x][0].split(',')
			]
		except Exception as err:
			logging.error(err)
			return None

		# Add windows to the list
		# Create list of non-windows to remove
		windows_id_to_remove = []
		windows_list = []
		if wmctrl_lg:
			for win in wmctrl_lg:
				w = Window()
				try:
					w.id_, w.type_, w.x, w.y, w.w, w.h, *_ = win.split()
				except Exception as err:
					logging.error(err)
				else:
					try:
						minimized_state = [
							x for x in cli.output_by_args(
								['xwininfo', '-id', w.id_, '-stats']
							).split('\n') if 'Map State: IsUnMapped' in x]
					except Exception as err:
						logging.error(err)
						return None

					if not minimized_state:
						if w.type_ == '-1':
							if w.w == str(self.__screen_w) and w.h == str(
									self.__screen_h):
								self.__desktop.id_ = w.id_
								windows_list.append(w)
							else:
								windows_id_to_remove.append(w.id_)
						else:
							windows_list.append(w)

		# Puts all valid windows in xprop order
		windows_in_order = []
		for xprop_id in xprop_root:
			if xprop_id not in windows_id_to_remove:
				for win in windows_list:
					if win.id_ == xprop_id:
						windows_in_order.append(win)

		return windows_in_order


if __name__ == '__main__':
	tex = Texture('0x5a00007', 1366, 768, 8)
	tex.create()
