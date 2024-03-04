#!/usr/bin/env python3
import logging
import os
import pathlib
import subprocess
import sys
import time
import threading

from PIL import Image, ImageFilter, ImageEnhance
from PySide6 import QtCore, QtGui

import PySideX.QtWidgetsX.modules.color as color
from PySideX.QtWidgetsX.modules.dynamicstyle import StyleParser
from PySideX.QtWidgetsX.modules.envsettings import GuiEnv

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
	def __init__(
			self, toplevel, alpha: float | int = None) -> None:
		"""..."""
		self.__toplevel = toplevel
		self.__alpha = alpha

		self.__gui_env = GuiEnv(
			self.__toplevel.platform().operational_system(),
			self.__toplevel.platform().desktop_environment())

		self.__is_dark = color.is_dark(
			self.__gui_env.settings().window_background_color().to_tuple())

		self.__enable_texture = False
		self.__desktop = Desktop()
		self.__windows = None
		self.__timer = QtCore.QTimer()
		self.__updating = False

		self.__toplevel_id = hex(self.__toplevel.win_id()).replace('0x', '0x0')
		self.__screen_w = self.__toplevel.screen().size().width()
		self.__screen_h = self.__toplevel.screen().size().height()
		self.__shadow_size = self.__toplevel.shadow_size()

		self.__style_sheet = self.__toplevel.style_sheet()
		self.__style_parser = StyleParser(self.__style_sheet)

		self.__is_using_texture = False
		self.__texture_name = 'texture.png'
		self.__textures_path = os.path.join(BASE_DIR, 'textures')
		self.__texture_url = os.path.join(
			self.__textures_path, self.__texture_name)
		self.__texture_image = None
		self.__toplevel_background_color = None
		self.__background_url = (
			f'background: url({self.__texture_url}) no-repeat;')
		self.__normal_style = self.__get_normal_style()

		self.__toplevel.set_style_signal.connect(self.__set_style_signal)
		self.__toplevel.reset_style_signal.connect(self.__set_style_signal)
		self.__toplevel.event_filter_signal.connect(self.__event_filter_signal)

	def set_enable(self, enable: bool) -> None:
		"""..."""
		self.__enable_texture = enable

	def enabled(self) -> bool:
		"""..."""
		return self.__enable_texture

	def update(self) -> None:
		"""..."""
		if not self.__updating:
			self.__updating = True
			thread = threading.Thread(target=self.__update)
			thread.start()

	def background_color(self) -> tuple:
		"""..."""
		return self.__toplevel_background_color

	def texture_image(self) -> Image:
		"""..."""
		return self.__texture_image

	def is_using_texture(self) -> bool:
		"""..."""
		return self.__is_using_texture

	def remove_texture(self) -> None:
		self.__toplevel.set_style_sheet(self.__normal_style)
		self.__is_using_texture = False

	def __background_color(self) -> str:
		toplevel_style = self.__style_parser.widget_scope('MainWindow')
		bg_color = None
		for x in toplevel_style.split(';'):
			if 'background-color' in x:
				bg_color = x + ';'
				break

		if bg_color and 'rgba' in bg_color:
			rgba = color.rgba_str_to_tuple(bg_color)
			self.__alpha = rgba[3]

			n_alpha = 245 if self.__is_dark else 225
			if self.__alpha > n_alpha:
				self.__alpha = n_alpha

			rgb = ", ".join([str(x) for x in rgba[:-1]])
			bg_color = f'background-color: rgba({rgb}, {self.__alpha});'
			self.__toplevel_background_color = (
				int(rgba[-4]), int(rgba[-3]), int(rgba[-2]), self.__alpha)

		if bg_color:
			return 'background: url();' + bg_color
		return 'background: url();'

	def __build_texture(self) -> bool:
		url = os.path.join(self.__textures_path, self.__desktop.id_ + '.png')
		if self.__screenshots() and os.path.isfile(url):
			imgdesk = Image.open(url)

			for win in self.__windows:
				urlfile = os.path.join(self.__textures_path, win.id_ + '.png')
				if os.path.isfile(urlfile) and win.type_ != '-1':
					if win.id_ != self.__toplevel_id:
						imgwin = Image.open(urlfile)
						imgdesk.paste(imgwin, (int(win.x), int(win.y)))

			self.__windows.reverse()
			for wd in self.__windows:
				if wd.id_ == self.__toplevel_id:
					x, y, w, h = int(wd.x), int(wd.y), int(wd.w), int(wd.h)
					out = imgdesk.crop((x, y, x + w, y + h)).convert('RGBA')
					out = self.__composite_background_color(out)
					if out[1]:
						radius = 15 if self.__is_dark else 10
						out = out[0].filter(
							ImageFilter.GaussianBlur(radius=radius + 10))
						# out = ImageEnhance.Brightness(out).enhance(0.97)
						out.save(self.__texture_url, 'PNG', quality=1)
						self.__texture_image = out
						return True
					else:
						return False

	def __composite_background_color(self, img) -> tuple:
		if self.__toplevel_background_color:
			if img.width == self.__toplevel.width(
					) and img.height == self.__toplevel.height():
				imgcolor = Image.new(
					'RGBA', (
						self.__toplevel.width(),
						self.__toplevel.height()),
					color=self.__toplevel_background_color)
				img = Image.alpha_composite(img, imgcolor)

				self.__timer.stop()
			else:
				self.__timer.timeout.connect(self.update)
				self.__timer.start(1000)
				return None, False
		return img, True

	def __event_filter_signal(self, event):
		if not self.__toplevel.is_server_side_decorated():
			if event.type() == QtCore.QEvent.WindowActivate:
				if self.__enable_texture and not self.__is_using_texture:
					self.remove_texture()

			elif event.type() == QtCore.QEvent.HoverEnter:
				if self.__enable_texture:
					self.update()

			elif event.type() == QtCore.QEvent.HoverLeave:
				if self.__enable_texture:
					if self.__is_using_texture:
						self.remove_texture()
					else:
						time.sleep(1)
						self.remove_texture()

			elif event.type() == QtCore.QEvent.Type.Move:
				if self.__enable_texture and self.__is_using_texture:
					self.remove_texture()

			elif event.type() == QtCore.QEvent.Resize:
				if self.__enable_texture and self.__is_using_texture:
					self.remove_texture()

				if self.__toplevel.is_maximized(
						) or self.__toplevel.is_full_screen():
					if self.__enable_texture and not self.__is_using_texture:
						self.__timer.timeout.connect(self.__timer_to_apply)
						self.__timer.start(200)

			elif event.type() == QtCore.QEvent.Close:
				for texture in os.listdir(self.__textures_path):
					os.remove(os.path.join(self.__textures_path, texture))

	def __get_normal_style(self) -> str:
		toplevel_style = self.__style_parser.widget_scope('MainWindow')
		toplevel_style += self.__background_color()
		style = self.__style_sheet + (
			'MainWindow {' f'{toplevel_style}' '}')
		self.__style_parser.set_style_sheet(style)
		return self.__style_parser.style_sheet()

	def __screenshots(self) -> bool:
		"""..."""
		if self.__windows:
			for window in self.__windows:
				try:
					cli.output_by_args([
						'import', '-window', window.id_, '-quality', '1',
						os.path.join(self.__textures_path, window.id_ + '.png')])
				except Exception as err:
					logging.error(err)
			return True
		else:
			return False

	def __set_style_signal(self) -> None:
		# ...
		self.__style_parser.set_style_sheet(self.__toplevel.style_sheet())
		self.__style_sheet = self.__style_parser.style_sheet()
		self.__normal_style = self.__get_normal_style()

	def __timer_to_apply(self):
		self.update()
		self.__timer.stop()

	def __toplevel_window(self) -> Window:
		window = Window()
		window.id_ = self.__toplevel_id
		window.type_ = '0'
		window.x = self.__toplevel.x()
		window.y = self.__toplevel.y()
		window.w = self.__toplevel.width()
		window.h = self.__toplevel.height()
		return window

	def __update(self) -> None:
		if self.__enable_texture:
			self.__windows = self.__valid_windows()
			if self.__build_texture():
				toplevel_style = self.__style_parser.widget_scope('MainWindow')
				toplevel_style += self.__background_url
				style = self.__style_sheet + (
					'MainWindow {' f'{toplevel_style}' '}')

				self.__style_parser.set_style_sheet(style)
				self.__toplevel.set_style_sheet(
					self.__style_parser.style_sheet())
				self.__is_using_texture = True

		self.__updating = False

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
		invalid_windows_id = []
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
								invalid_windows_id.append(w.id_)
						else:
							windows_list.append(w)

		# Puts all valid windows in xprop order
		windows_in_order = []
		for xprop_id in xprop_root:
			if xprop_id not in invalid_windows_id:
				for win in windows_list:
					if win.id_ == xprop_id:
						windows_in_order.append(win)

		windows_in_order.append(self.__toplevel_window())
		return windows_in_order
