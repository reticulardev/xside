#!/usr/bin/env python3
import logging
import os
import pathlib
import subprocess
import sys

from PIL import Image, ImageFilter, ImageEnhance

from PySideX.QtWidgetsX.applicationwindow import ApplicationWindow
from PySideX.QtWidgetsX.modules.dynamicstyle import StyleParser

BASE_DIR = pathlib.Path(__file__).resolve().parent
sys.path.append(BASE_DIR.as_posix())

import cli


class Window(object):
	def __init__(self):
		self.id_ = 'Window'

	def __str__(self) -> str:
		return f'<Window: {self.id_}>'

	def __repr__(self) -> str:
		return f'<Window: {self.id_}>'


class Desktop(object):
	def __init__(self):
		self.id_ = 'Desktop'

	def __str__(self) -> str:
		return f'<Desktop: {self.id_}>'

	def __repr__(self) -> str:
		return f'<Desktop: {self.id_}>'


class Texture(object):
	"""..."""
	def __init__(self, toplevel: ApplicationWindow) -> None:
		"""..."""
		self.__toplevel = toplevel

		self.__texture_name = 'texture.png'
		self.__path = os.path.join(BASE_DIR, 'textures')
		self.__texture_url = os.path.join(self.__path, self.__texture_name)
		self.__toplevel_id = hex(self.__toplevel.win_id()).replace('0x', '0x0')
		self.__screen_w = self.__toplevel.screen().size().width()
		self.__screen_h = self.__toplevel.screen().size().height()
		self.__shadow_size = self.__toplevel.shadow_size()
		self.__background_url = (
			f'background: url({self.__texture_url}) no-repeat;')

		self.__desktop = Desktop()
		self.__windows = None

	def apply_texture(self) -> None:
		self.__windows = self.__valid_windows()
		self.build_texture()
		toplevel_style = StyleParser(
			self.__toplevel.style_sheet()).widget_scope(
			'MainWindow')
		toplevel_style += self.__background_url
		style = self.__toplevel.style_sheet() + (
			'MainWindow {'
			f'{toplevel_style}'
			'}')

		parser = StyleParser(style)
		style = parser.style_sheet()
		self.__toplevel.set_style_sheet(style)

	def build_texture(self):
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
					out.save(self.__texture_url)

	def __toplevel_window(self) -> Window:
		w = Window()
		w.id_ = self.__toplevel_id
		w.type_ = '0'
		w.x = self.__toplevel.x()
		w.y = self.__toplevel.y()
		w.w = self.__toplevel.width()
		w.h = self.__toplevel.height()
		return w

	def __screenshots(self) -> bool:
		"""..."""
		if self.__windows:
			for window in self.__windows:
				try:
					cli.output_by_args([
						'import', '-window', window.id_, '-quality', '1',
						os.path.join(self.__path, window.id_ + '.png')])
				except Exception as err:
					logging.error(err)
			return True
		else:
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

		windows_in_order.append(self.__toplevel_window())
		return windows_in_order
