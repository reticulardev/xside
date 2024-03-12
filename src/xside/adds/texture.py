#!/usr/bin/env python3
import logging
import os
import pathlib
import subprocess
import sys
import time
import threading

from PIL import Image, ImageFilter, ImageEnhance
from PySide6 import QtCore
from __feature__ import snake_case

from xside import modules
from xside.modules import color
from xside.adds.reg import Reg
from xside.modules.stylesheetops import StyleSheetOps


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
		# Params
		self.__toplevel = toplevel
		self.__alpha = alpha
		# Flags
		self.__enable_texture = False
		self.__updating = False
		self.__is_using_texture = False
		# Properties
		self.__path = pathlib.Path(__file__).resolve().parent
		self.__desktop = Desktop()
		self.__desktop_windows = []
		self.__toplevel_id = hex(self.__toplevel.win_id()).replace('0x', '0x0')
		self.__style_sheet = self.__toplevel.style_sheet()
		self.__styleop = StyleSheetOps()
		self.__styleop.set_stylesheet(self.__style_sheet)

		self.__textures_path = os.path.join(self.__path, 'tmp')
		self.__texture_url = os.path.join(self.__textures_path, 'texture.png')
		self.__texture_image = None
		self.__background_color = None
		self.__background_style = self.__get_normal_style()

		self.__reg = Reg()
		self.__reg.set_path(os.path.join(pathlib.Path(__file__).resolve(
			).parent.parent, 'modules', 'static'))
		self.__reg.add('add-texture-enable', False)

		# Sigs
		self.__toplevel.set_style_signal.connect(self.__set_style_signal)
		self.__toplevel.reset_style_signal.connect(self.__set_style_signal)
		self.__toplevel.event_filter_signal.connect(self.__event_filter_signal)

	def background_color(self) -> tuple:
		"""..."""
		return self.__background_color

	def enabled(self) -> bool:
		"""..."""
		return self.__enable_texture

	def is_using_texture(self) -> bool:
		"""..."""
		return self.__is_using_texture

	def remove(self) -> None:
		self.__toplevel.set_style_sheet(self.__background_style)
		self.__is_using_texture = False

	def set_enable(self, enable: bool) -> None:
		"""..."""
		self.__enable_texture = enable
		self.__reg.add('add-texture-enable', enable)

	def texture_image(self) -> Image:
		"""..."""
		return self.__texture_image

	def update(self) -> None:
		"""..."""
		if not self.__updating:
			self.__updating = True
			thread = threading.Thread(
				target=self.__insert_texture_into_window_background)
			thread.start()

	def __build_texture(self) -> bool:
		url = os.path.join(self.__textures_path, self.__desktop.id_ + '.png')
		if self.__create_the_texture_screens() and os.path.isfile(url):
			imgdesk = Image.open(url)

			for win in self.__desktop_windows:
				urlfile = os.path.join(self.__textures_path, win.id_ + '.png')
				if os.path.isfile(urlfile) and win.type_ != '-1':
					if win.id_ != self.__toplevel_id:
						imgwin = Image.open(urlfile)
						imgdesk.paste(imgwin, (int(win.x), int(win.y)))

			self.__desktop_windows.reverse()
			for wd in self.__desktop_windows:
				if wd.id_ == self.__toplevel_id:
					x, y, w, h = int(wd.x), int(wd.y), int(wd.w), int(wd.h)
					out = imgdesk.crop((x, y, x + w, y + h)).convert('RGBA')
					out = self.__composite_background_color(out)
					if out[1]:
						radius = 20 if self.__toplevel.is_dark() else 15
						out = out[0].filter(
							ImageFilter.GaussianBlur(radius=radius))
						# out = ImageEnhance.Brightness(out).enhance(0.97)
						out.save(self.__texture_url, 'PNG', quality=1)
						self.__texture_image = out
						return True
					else:
						return False

	@staticmethod
	def __cli_output_by_args(args: list) -> str | None:
		"""output of command arguments

		by_args(['echo', '$HOME']) -> "/home/user"

		:param args: list args like: ['ls', '-l']
		"""
		try:
			command = subprocess.Popen(
				args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			stdout, stderr = command.communicate()
		except ValueError as er:
			print(er)
			print(f'Error in command args: "{command_args}"')
			return None
		else:
			if not stderr.decode():
				return stdout.decode().strip().strip("'").strip()
			return None

	def __composite_background_color(self, img) -> tuple:
		if self.__background_color:
			if img.width == self.__toplevel.width(
					) and img.height == self.__toplevel.height():
				imgcolor = Image.new(
					'RGBA', (
						self.__toplevel.width(),
						self.__toplevel.height()),
					color=self.__background_color)
				img = Image.alpha_composite(img, imgcolor)
			else:
				t = threading.Thread(target=self.__update_thread, args=(1.0,))
				t.start()
				return None, False
		return img, True

	def __create_the_texture_screens(self) -> bool:
		"""..."""
		if self.__desktop_windows:
			for window in self.__desktop_windows:
				try:
					self.__cli_output_by_args([
						'import', '-window', window.id_, '-quality', '1',
						os.path.join(
							self.__textures_path, window.id_ + '.png')])
				except Exception as err:
					logging.error(err)
			return True
		else:
			return False

	@staticmethod
	def __create_window_object_by_wmctrl_string(
			window_str: str) -> Window | None:
		try:
			id_, type_, x, y, width, height, _, *title = window_str.split()
			window = Window()
			window.id_ = id_
			window.type_ = type_
			window.x = x
			window.y = y
			window.w = width
			window.h = height
			window.title = ' '.join(title)
		except Exception as err:
			logging.error(err)
			print(err)
			return None
		else:
			return window

	def __event_filter_signal(self, event):
		if not self.__toplevel.is_server_side_decorated():
			if event.type() == QtCore.QEvent.WindowActivate:
				if self.__enable_texture and not self.__is_using_texture:
					self.remove()

			elif event.type() == QtCore.QEvent.HoverEnter:
				if self.__enable_texture:
					self.update()

			elif event.type() == QtCore.QEvent.HoverLeave:
				if self.__enable_texture:
					if self.__is_using_texture:
						self.remove()
					else:
						time.sleep(1)
						self.remove()

			elif event.type() == QtCore.QEvent.Type.Move:
				if self.__enable_texture and self.__is_using_texture:
					self.remove()

			elif event.type() == QtCore.QEvent.Resize:
				if self.__enable_texture and self.__is_using_texture:
					self.remove()

				if self.__toplevel.is_maximized(
						) or self.__toplevel.is_full_screen():
					if self.__enable_texture and not self.__is_using_texture:
						t = threading.Thread(target=self.__update_thread)
						t.start()

			elif event.type() == QtCore.QEvent.Close:
				for texture in os.listdir(self.__textures_path):
					if texture != 'tmp':
						os.remove(os.path.join(self.__textures_path, texture))

	def __get_background_color(self) -> str:
		toplevel_style = self.__styleop.widget_stylesheet('MainWindow')
		if toplevel_style:
			bg_color = None
			for x in toplevel_style.split(';'):
				if 'background-color' in x:
					bg_color = x + ';'
					break

			rgba = None
			if bg_color and 'rgba' in bg_color:
				rgba = color.rgba_str_to_tuple(bg_color)
			elif bg_color and '#' in bg_color:
				hexa = bg_color.replace(' ', '').split(':')[-1].split(';')[0]
				print('HEX:', hexa)
				rgba = color.hex_to_rgba(hexa)

			if rgba:
				self.__alpha = rgba[3]

				n_alpha = 245 if self.__toplevel.is_dark() else 225
				if self.__alpha > n_alpha:
					self.__alpha = n_alpha

				rgb = ", ".join([str(x) for x in rgba[:-1]])
				bg_color = f'background-color: rgba({rgb}, {self.__alpha});'
				self.__background_color = (
					int(rgba[-4]), int(rgba[-3]), int(rgba[-2]), self.__alpha)

			if bg_color:
				return 'background: url();' + bg_color
		return 'background: url();'

	def __get_normal_style(self) -> str:
		toplevel_style = self.__styleop.widget_stylesheet('MainWindow')
		if toplevel_style:
			toplevel_style += self.__get_background_color()
			style = self.__style_sheet + (
				'MainWindow {' f'{toplevel_style}' '}')
			self.__styleop.set_stylesheet(style)
		return self.__styleop.stylesheet()

	def __get_windows(self):
		# wmctrl_lg: marks windows that are not windows using an '-1'
		windows_and_components_list = self.__cli_output_by_args(
			['wmctrl', '-lG']).split('\n')

		id_to_remove = []
		valid_windows_list = []
		if windows_and_components_list:
			for item in windows_and_components_list:
				window = self.__create_window_object_by_wmctrl_string(item)

				if not self.__is_window_minimized(window):
					if window.type_ == '-1':
						screen_w = str(
							self.__toplevel.screen().size().width())
						screen_h = str(
							self.__toplevel.screen().size().height())

						if window.w == screen_w and window.h == screen_h:
							self.__desktop.id_ = window.id_
							valid_windows_list.append(window)
						else:
							id_to_remove.append(
								window.id_)
					else:
						valid_windows_list.append(window)

		return self.__windows_in_the_correct_order(
			valid_windows_list, id_to_remove)

	def __insert_texture_into_window_background(self) -> None:
		if self.__enable_texture:
			self.__desktop_windows = self.__get_windows()
			if self.__build_texture():
				scope = self.__styleop.widget_stylesheet('MainWindow')
				if scope:
					self.__styleop.set_stylesheet(
						'MainWindow {'
						f'{scope}'
						f'background: url({self.__texture_url}) no-repeat;'
						'}')
					self.__toplevel.set_style_sheet(
						self.__styleop.stylesheet())
					self.__is_using_texture = True

		self.__updating = False

	def __is_window_minimized(self, window: Window) -> bool:
		try:
			minimized_state = [
				x for x in self.__cli_output_by_args(
					['xwininfo', '-id', window.id_, '-stats']
				).split('\n') if 'Map State: IsUnMapped' in x]
		except Exception as err:
			logging.error(err)
			print('"xwininfo" command error:')
			print(err)
			return False
		else:
			return True if minimized_state else False

	def __is_window_the_desktop(self, window: Window) -> bool:

		if window.w == str(
				self.__toplevel.screen().size().width()
				) and window.h == self.__toplevel.screen().size().height():
			return True
		return False

	def __keep_only_windows_below(self, windows_in_order) -> list:
		topwin = self.__toplevel_window()
		x, y = topwin.x, topwin.y
		w, h = topwin.w + topwin.x, topwin.h + topwin.y

		new_windows = []
		for item in range(len(windows_in_order) - 2, -1, -1):
			win = windows_in_order[item]
			if win.id_ != topwin.id_ and win.type_ != '-1':
				winx, winy = int(win.x), int(win.y)
				winw, winh = int(win.w), int(win.h)

				x = winx if winx < topwin.x else x
				y = winy if winy < topwin.y else y
				w = winw + winx if winw + winx > topwin.w + topwin.x else w
				h = winh + winy if winh + winy > topwin.h + topwin.y else h

				new_windows.insert(0, win)
				if all([
					x < topwin.x, y < topwin.y,
					w > topwin.w + topwin.x, h > topwin.h + topwin.y]):
					break

		if len(new_windows) == 1:
			for win in windows_in_order:
				if win.id_ == self.__desktop.id_:
					new_windows.insert(0, win)
					break

		new_windows.append(topwin)
		return new_windows

	def __set_style_signal(self) -> None:
		# ...
		self.__styleop.set_stylesheet(self.__toplevel.style_sheet())
		self.__style_sheet = self.__styleop.stylesheet()
		self.__background_style = self.__get_normal_style()

	def __toplevel_window(self) -> Window:
		window = Window()
		window.id_ = self.__toplevel_id
		window.type_ = '0'
		window.x = self.__toplevel.x()
		window.y = self.__toplevel.y()
		window.w = self.__toplevel.width()
		window.h = self.__toplevel.height()
		window.title = self.__toplevel.window_title()
		return window

	def __update_thread(self, step: float = 0.2):
		time.sleep(step)
		self.update()

	def __windows_in_the_correct_order(
			self, valid_windows_list: list, id_to_remove: list) -> list:

		# Puts all valid windows in xprop order
		# xprop_root: list windows in order (z-index)
		windows_in_order = [
			x.split()[-1].replace('0x', '0x0') for x in [
				x for x in self.__cli_output_by_args(
					['xprop', '-root']).split('\n')
				if '_NET_CLIENT_LIST_STACKING(WINDOW)' in x][0].split(',')]

		valid_windows_in_order = []
		for xprop_id in windows_in_order:
			if xprop_id not in id_to_remove:
				for item in valid_windows_list:
					if item.id_ == xprop_id:
						valid_windows_in_order.append(item)

		# windows_in_order.append(self.__toplevel_window())
		valid_windows_in_order = self.__keep_only_windows_below(
			valid_windows_in_order)

		return valid_windows_in_order
