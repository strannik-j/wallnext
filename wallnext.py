#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  wallnext
#
#  Copyright 2011 Strannik-j <mail@strannik-j.org>
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the  nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#  * All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#
#		This product includes software developed by a Bessonov Jurij  
#		aka Strannik-j (http://strannik-j.org) and his contributors.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import os
import signal
from tkinter.filedialog import *
from random import randrange
from subprocess import call as _call
from time import sleep as _sleep
import sys
import fileinput

interval = 0
path_wall = ''
wall_sort = 0
chG = 0
config0 = []


def read_dir(path_wall):
	true_files = ('.jpg', '.png', 'jpeg', '.JPG', '.PNG', 'JPEG')
	wall_dir = path_wall
	all_files = os.listdir(wall_dir)
	pic_files = []
	for a in all_files:
		if len(a) >= 5:
			if a[-4:] in true_files:
				pic_files.append(a)
	return pic_files, wall_dir


def random_pic(pic_files):
	ch0 = 0
	ch0 = int(ch0)
	rand = []
	max_pic = len(pic_files)
	while ch0 < max_pic:
		ran = randrange(0, max_pic, 1)
		if rand.count(ran) == 0:
			rand.append(ran)
			ch0 += 1
	print('Random procedure \
	rand = ', rand)
	return rand, max_pic
	
	
def now_pic(rand, pic_files, wall_dir, ch1=0):
	print('Now pic \
	pic_files = ', pic_files)
	now_pic_file = 'xxx'
	print(os.access(wall_dir + now_pic_file, os.R_OK))
	while os.access(wall_dir + now_pic_file, os.F_OK) == False:
		a = rand[ch1]
		ch1 += 1
		print ('Number picture: \
		ch1 = ', ch1)
		now_pic_file = pic_files[a]
		print('now_pic_file = ', now_pic_file)
	print('except pic_files')
	return now_pic_file 


def get_pic(now_pic_files, wall_dir):
	print('get pic: ', now_pic_files)
	pwd = os.getcwd() + '/'
	tmpfl = open('.tmp_file.sh', 'w') 
	tmpfls = ('#!/bin/bash \n'
	'pcmanfm --set-wallpaper "' + wall_dir + now_pic_files + '"')
	tmpfl.write(tmpfls)
	tmpfl.close()
	os.chmod(pwd + '.tmp_file.sh', 999)
	_call(['./.tmp_file.sh'])
	os.remove('.tmp_file.sh')

	
def _rand(pic_files):
	rand_files, chM = random_pic(pic_files)
	return rand_files, chM
	
ch3 = 0 


def _start0(rand_files, pic_files, ch3, wall_dir, chM, interval):

	while ch3 < chM:
		print('ch3 = ', ch3)
		print('chM = ', chM)
		now_p = now_pic(rand_files, pic_files, wall_dir, ch3)
		get_pic(now_p, wall_dir)
		ch3 += 1
		_sleep(interval)
	else:
		print('_start: ch3 = chM')
		return 0


def _start1(pic_files, ch3, wall_dir, chM, interval):
	while ch3 < chM:
		print('ch3 = ', ch3)
		print('chM = ', chM)
		now_p = pic_files[ch3]
		get_pic(now_p, wall_dir)
		ch3 += 1
		print ('interval = ', interval)
		_sleep(interval)
	else:
		print('_start: ch3 = chM')
		return 0
		
def __init__():
	
	home_dir = os.environ['HOME']
	conf_dir = home_dir + '/.config/wallnext/'

# check presence of a config file
	if os.access(conf_dir + 'file.conf', os.F_OK) == False:
		# check: no file or dir
		
		# check presence of a confin dir in a .config dir
		if os.access(conf_dir, os.F_OK) == False:
			# no dir
			os.makedirs(conf_dir)		# create "wallnext" dir in a "~/.config" dir
		# start gui
		try:
			_call(['wallnext-gui'])			# start a GUI
		except:
			try:
				_call(['./wallnext-gui'])
			except:
				_call(['wallnext-gui.py'])
		sys.exit()
	else:
		print('else')
		
	cf = open(conf_dir + 'file.conf', 'r')	# read .conf file

	# derive a line of a config file
	for i in fileinput.input(conf_dir + 'file.conf'):
		config0.append(i)

	wall_manager = config0[0] 					# wallpappers manager
	path_wall = config0[1][:-1] + '/'		# PATH to wallpappers 
	wall_sort = int(config0[2])
	interval = int(config0[3])			# time interval
	print(interval)
	
	## kill PID (stop daemon)
	try:
		cf = open(conf_dir + 'pid', "r")
		#print('open')
		kill_pid = int(cf.readline())
		#print(kill_pid)
		os.kill(kill_pid, signal.SIGTERM)
		#print('kill')
		cf.close()
	except:
		print('except kill')
	
	## create PID file	
	cf = open(conf_dir + 'pid', "w")
	pid = str(os.getpid())
	cf.write(pid)
	cf.close()

	pic_files, wall_dir = read_dir(path_wall)
	while True:
		if wall_sort == 0:
			print('Random sort')
			rand_files, chM = random_pic(pic_files)
			_start0(rand_files, pic_files, ch3, wall_dir, chM, interval)
		elif wall_sort == 1:
			print("Sort by name \n", pic_files)
			chM = len(pic_files)
			_start1(pic_files, ch3, wall_dir, chM, interval)
		else:
			print('wall_sort = ',wall_sort)
			sys.exit()
	
__init__()
