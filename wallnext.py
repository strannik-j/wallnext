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
import shutil
import signal
import glob
from random import randrange
from subprocess import call as _call
from time import sleep as _sleep
import sys
import fileinput

wall_change_interval = 0
wall_dir_path = ''
wall_sort = 0
chG = 0
conf_str_list = []
wall_manager = 0
wall_img_now = []

img_files_list = []


pwd = os.getcwd()
home_dir_path = os.path.expanduser('~')
#home_dir_path = os.environ['HOME']
conf_file_name = 'wallnext.conf'
conf_dir_path = os.path.join(home_dir_path,'.config/wallnext')
conf_file_path = os.path.join(conf_dir_path, conf_file_name)

default_dir_path = os.path.join(pwd,'default')
sub_wall_dir_path = []
read_subdir_var = 0
conf_str_list = []
#sub_wall_dir_list = []
version = "0.2.0"


def read_wall_dir(wall_dir_path):
	print('read_wall_dir')
	
	true_files = ('.jpg', '.png', 'jpeg', '.JPG', '.PNG', 'JPEG')
	wall_dir_path = wall_dir_path
	all_img_files_list = os.listdir(wall_dir_path)
	
	for a in all_img_files_list:
		if len(a) >= 5:
			if a[-4:] in true_files:
				img_files_list.append(os.path.join(wall_dir_path,a))
	return img_files_list

def read_sub_wall_dir(wall_dir_path):
	#global sub_wall_dir_list
	sub_img_files_list = []
	print('read_sub_wall_dir')
	print('wall_dir_path = ',wall_dir_path)
	print('glob = ',glob.glob(wall_dir_path+'*/'))
	sub_wall_dir_list = glob.glob(wall_dir_path+'*/')
	print('sub_wall_dir_list = ',sub_wall_dir_path)
	for i in sub_wall_dir_list:
		true_files = ('.jpg', '.png', 'jpeg', '.JPG', '.PNG', 'JPEG')
		#wall_dir_path = wall_dir_path
		all_files_list = os.listdir(i)
		
		for a in all_files_list:
			
			if len(a) >= 5:
				if a[-4:] in true_files:
					
					sub_img_files_list.append(os.path.join(i,a))
	print('ass')
	return sub_img_files_list
def random_pic(img_files_list):
	print('random_pic')
	ch0 = 0
	ch0 = int(ch0)
	rand = []
	max_pic = len(img_files_list)
	while ch0 < max_pic:
		ran = randrange(0, max_pic, 1)
		if rand.count(ran) == 0:
			rand.append(ran)
			ch0 += 1
	print('Random procedure \
	rand = ', rand)
	return rand, max_pic
	
	
def img_now(rand, img_files_list,ch1=0):
	print('img_now')
	#global wall_img_now_file
	#print('Now pic \
	#img_files_list = ', img_files_list)
	wall_img_now_file = 'xxx'
	print(wall_img_now_file)
	print('www',os.access(wall_img_now_file, os.R_OK))
	while os.access(wall_img_now_file, os.F_OK) == False:
		a = rand[ch1]
		ch1 += 1
		print ('Number picture: \
		ch1 = ', ch1)
		wall_img_now_file = img_files_list[a]
		print('wall_img_now_file = ', wall_img_now_file)
	print('except img_files_list')
	return wall_img_now_file 


def get_pic(now_img_files_list):
	print('get_pic')
	global wall_manager
	tmpfls = ''
	
	print('get pic: ', now_img_files_list)
	#pwd = os.getcwd() + '/'
	tmpfl = open('/tmp/wallnext_tmp.sh', 'w') 
	print('wall_manager = ',type(wall_manager))
	if wall_manager == 'gsettings':
		tmpfls = ('#!/bin/bash \n'
		'gsettings set org.gnome.desktop.background picture-uri file://"' + now_img_files_list + '"')
		
	elif wall_manager == 'pcmanfm':
		tmpfls = ('#!/bin/bash \n'
		'pcmanfm --set-wallpaper "' + now_img_files_list + '"')
	elif wall_manager == 'feh':
		tmpfls = ('#!/bin/bash \n'
		'feh --bg-scale "' + now_img_files_list + '"')
	else:
		print("i don'n know this wall manager")
	print('tmpfls = ',tmpfls)
	tmpfl.write(tmpfls)
	tmpfl.close()
	os.chmod(os.path.join(pwd,'/tmp/wallnext_tmp.sh'), 0o777)
	_call(['/tmp/./wallnext_tmp.sh'])
	os.remove('/tmp/wallnext_tmp.sh')

	
def _rand(img_files_list):
	print('_rand')
	rand_files_list, chM = random_pic(img_files_list)
	return rand_files_list, chM
	
ch3 = 0 


def _start_random(rand_files_list, img_files_list, ch3, chM, wall_change_interval):
	global wall_img_now
	print('_start_random')
	while ch3 < chM:
		print('ch3 = ', ch3)
		print('chM = ', chM)
		wall_img_now = img_now(rand_files_list, img_files_list, ch3)
		print('wall_img_now = ', wall_img_now)
		get_pic(wall_img_now)
		ch3 += 1
		_sleep(wall_change_interval)
	else:
		print('_start: ch3 = chM')
		return 0


def _start_name(img_files_list, ch3, chM, wall_change_interval):
	while ch3 < chM:
		print('ch3 = ', ch3)
		print('chM = ', chM)
		wall_img_now = img_files_list[ch3]
		get_pic(wall_img_now)
		ch3 += 1
		print ('wall_change_interval = ', wall_change_interval)
		_sleep(wall_change_interval)
	else:
		print('_start: ch3 = chM')
		return 0
		
def __init__():
	global pwd
	global wall_manager
	global home_dir_path
	global conf_dir_path
	global read_subdir_var

	# check presence of a config file
	# Проверяем наличие config каталога, и если его нет, создаем
	if not os.path.exists(conf_dir_path):
		os.makedirs(conf_dir_path) 

	# check presence of a confin dir in a .config dir
	# Проверяем наличие config файла, и если его нет, копируем из default
	if not os.path.exists(conf_file_path):
		print('no conf file')
		shutil.copy2(os.path.join(default_dir_path,conf_file_name),conf_file_path)		
		
		# start gui
		print(pwd)
		os.chdir(pwd)
		try:
			_call(['wallnext-gui'])			# start a GUI
		except:
			try:
				_call(['./wallnext-gui'])
			except:
				_call(['./wallnext-gui.py'])
			sys.exit()

		
	conf_file_obj = open(conf_file_path, 'r')	# read .conf file

	# derive a line of a config file
	for i in fileinput.input(conf_file_path):
		conf_str_list.append(i)

	wall_manager = conf_str_list[0][:-1] 					# wallpappers manager
	wall_dir_path = conf_str_list[1][:-1]				# PATH to wallpappers 
	read_subdir_var = conf_str_list[2][:-1]
	wall_sort = conf_str_list[3][:-1]
	wall_change_interval = int(conf_str_list[4])			# time wall_change_interval
	print(wall_change_interval)
	
	## kill PID (stop daemon)
	print('pwd = ', pwd)
	try:
		pid_file_obj = open(os.path.join(conf_dir_path,'pid'), "r")
		#print('open')
		kill_pid = int(pid_file_obj.readline())
		print('kill_pid = ',kill_pid)
		os.kill(kill_pid, signal.SIGTERM)
		print('kill')
		pid_file_obj.close()
	except:
		print('except kill')
	
	## create PID file	
	pid_file_obj = open(os.path.join(conf_dir_path,'pid'), "w")
	pid = str(os.getpid())
	pid_file_obj.write(pid)
	pid_file_obj.close()

	img_files_list = read_wall_dir(wall_dir_path)
	if read_subdir_var == '1':
		img_files_list += read_sub_wall_dir(wall_dir_path)
	while True:
		if wall_sort == 'random':
			print('Random sort \n', img_files_list)
			print('len = ',len(img_files_list))
			xxx = set(img_files_list)
			print('len2 = ', len(xxx))
			rand_files_list, chM = random_pic(img_files_list)
			#print(rand_files_list)
			_start_random(rand_files_list, img_files_list, ch3, chM, wall_change_interval)
		elif wall_sort == 'name':
			print("Sort by name \n", img_files_list)
			chM = len(img_files_list)
			_start_name(img_files_list, ch3, chM, wall_change_interval)
		else:
			print('wall_sort = ',wall_sort, type(wall_sort))
			
			sys.exit()
	
__init__()
