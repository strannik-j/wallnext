#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  wallnext-gui
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
#  * Neither the name of the Strannik-j.org nor the names of its
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


import shutil
import glob
from tkinter import *
#from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.filedialog import askdirectory

from tkinter.ttk import Combobox
import fileinput
import sys
import os
import signal
from subprocess import call as _call

pwd = os.getcwd()
home_dir_path = os.path.expanduser('~')
#home_dir_path = os.environ['HOME']
conf_file_name = 'wallnext.conf'
conf_dir_path = os.path.join(home_dir_path,'.config/wallnext')
conf_file_path = os.path.join(conf_dir_path, conf_file_name)

default_dir_path = os.path.join(pwd,'default')
conf_str_list = []


root = Tk(screenName=None, className='WallNext')
frame0 = Frame(root, width=300, height=600)

read_subdir_var = StringVar()
conf_file = StringVar()
rbut_sort = StringVar()
rbut_sort.set('')
ent_text0 = StringVar()
ent_text1 = StringVar()
ent_text2 = StringVar() 

wall_dir_path = StringVar()
wall_change_interval = IntVar()
wall_manager = ''
conf_str_list = []
version = "0.2.0"

license0 = ('''
			WallNext
			
	Copyright 2011 Strannik-j <mail@strannik-j.org>
	
	Redistribution and use in source and binary forms, with or without
	modification, are permitted provided that the following conditions are
	met:
	
	* Redistributions of source code must retain the above copyright
	  notice, this list of conditions and the following disclaimer.
	* Redistributions in binary form must reproduce the above
	  copyright notice, this list of conditions and the following disclaimer
	  in the documentation and/or other materials provided with the
	  distribution.
	* Neither the name of the Strannik-j.org nor the names of its
	  contributors may be used to endorse or promote products derived from
	  this software without specific prior written permission.
	* All advertising materials mentioning features or use of this software
	  must display the following acknowledgement:
	
		This product includes software developed by a Bessonov Jurij  
		aka Strannik-j (http://strannik-j.org) and his contributors.
	
	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
	"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
	LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
	A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
	OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
	SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
	LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
	DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
	THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
	(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
	OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
''')


home_dir = os.environ['HOME']
conf_dir = home_dir + '/.config/wallnext/'


def main():
	global read_subdir_var
	global wall_manager
	global wall_dir_path
	
	if os.access(conf_file_path, os.F_OK) == False:
		print('no file or dir')
		if os.access(conf_dir, os.F_OK) == False:
			print('no dir')
			os.makedirs(conf_dir)
	try:
		conf_file_obj = open(conf_file_path, "r")
		print('norma', conf_file_obj)
	except:
		conf_file_obj = open(conf_file_path, "w")
		conf_file_obj.write('0 \n' + home_dir + '\n' + '1' + '\n' + '600')
		conf_file_obj.close()
		conf_file_obj = open(conf_file_path, "r")
	
	# read conf file
	print('read conf file')
	for i in fileinput.input(conf_file_path):
		conf_str_list.append(i)
	print(conf_str_list)
	wall_manager = conf_str_list[0][:-1]
	wall_dir_path = conf_str_list[1][:-1]
	read_subdir_var.set(conf_str_list[2][:-1])
	wall_sort = conf_str_list[3][:-1]
	wall_change_interval = int(conf_str_list[4])
	ent_text0.set(wall_dir_path)
	ent_text1.set(wall_change_interval)
	rbut_sort.set(wall_sort)
	conf_file.set(conf_file_obj)
	conf_file_obj.close()
	combobox_wall_manager.set(wall_manager)
	#return 0
	
	
def save_conf(r_var0):
	print('save_conf')
	global wall_manager
	#wall_manager = str(rbut_var0.get())
	wall_dir_path = ent_wall_dir_path.get()
	wall_sort = rbut_sort.get()
	wall_change_interval = ent_interval.get()
	conf_str_list = (wall_manager + '\n'
	+ wall_dir_path + '\n'
	+ read_subdir_var.get() + '\n' 
	+ wall_sort + '\n'
	+ wall_change_interval)
	conf_file_obj = open(conf_file_path, "w")
	conf_file_obj.write(conf_str_list)
	conf_file_obj.close()
	print(conf_str_list)
	#_call(['killall'])
	try:
		root.destroy()
		_call(['wallnext'])
	except:
		try:
			_call(['./wallnext'])
		except:
			_call(['./wallnext.py'])
	#return 0
	
#browse images directory
def _browse(self):
	print('_browse')
	global wall_dir_path
	wall_dir_path = askdirectory(initialdir=wall_dir_path)
	ent_text0.set(wall_dir_path)
	print(wall_dir_path)	
	
	
# start daemon
def start_daemon(r_var0):
	print('start_daemon')
	global conf_dir_path
	global wall_manager
	global wall_dir_path
	wall_manager = str(rbut_var0.get())
	wall_dir_path = ent_wall_dir_path.get()
	wall_change_interval = ent_interval.get()
	conf_str_list = (wall_manager + '\n'
	+ wall_dir_path + '\n' + 
	wall_change_interval)
	conf_file_obj = open(conf_file_path, "w")
	conf_file_obj.write(conf_str_list)
	conf_file_obj.close()
	print(conf_str_list)
	#_call(['killall'])
	try:
		#root.destroy()
		_call(['wallnext'])
		
		#sys.exit()
	except:
		_call(['wallnext.py'])


# stop daemon
def stop_daemon(x1):
	print('stop_daemon')
	global conf_dir_path	
	try:
		pid_file_obj = open(os.path.join(conf_dir_path,'pid'), "r")
		print('open PID file')
		kill_pid = int(pid_file_obj.readline())
		print(kill_pid)
		os.kill(kill_pid, signal.SIGTERM)
		print('kill')
		pid_file_obj.close()
	except:
		print('except kill')
	try:
		os.remove(os.path.join(conf_dir_path,'pid'))
		print('remove pid file')
	except:
		print('no pid file')
def about(self):
     showinfo("Editor", "  WallNext \nVersion " + version + 
     "\nThis product includes software developed by a Bessonov Jurij \n \
     aka Strannik-j (http://strannik-j.org) and his contributors.")


def _license(x):
	print()
	win0 = Toplevel(root, bd=5)
	win0.title("License")
	win0.minsize(width=400, height=400) 
	txt0 = Text(win0, width=80, height=30, font="5", wrap=WORD)
	txt0.insert(END, license0)
	txt0.pack()


canv0 = Canvas(frame0, width=500, height=50, bg="lightblue")	
lab0 = Label(frame0, text="Wallpappers changer", font="Sans 12")
lab1 = Label(frame0, text="Desktop manager", font="Sans 10")
lab2 = Label(frame0, text="PATH to wallpappers: ", font="Arial 10")
lab3 = Label(frame0, text="Interval (sec): ", font="Arial 10")
#lab4 = Label(frame0, text="Sort", font="Arial 10")


rbut_sort_random = Radiobutton(frame0, text="Random", variable=rbut_sort, value='random')
rbut_sort_name = Radiobutton(frame0, text="Sort by name", variable=rbut_sort, value='name')
rbut_sort_date = Radiobutton(frame0, text="Sort by date", variable=rbut_sort, value='date')
	
combobox_wall_manager = Combobox(frame0,values = ["gsettings","pcmanfm","Nautilus","feh"],height=5)

read_subdir_cbut = Checkbutton(frame0, text = 'Subdir include', variable = read_subdir_var, onvalue='1', offvalue = '0')


but_ok = Button(frame0, text="OK", width=8)
but_ok.bind("<Button-1>", save_conf)
but_canc = Button(frame0, text="Отмена", width=8)
but_canc.bind("<Button-1>", sys.exit)
but_start = Button(frame0, text="Start daemon")
but_start.bind("<Button-1>", start_daemon)
but_kill = Button(frame0, text='Stop daemon')
but_kill.bind("<Button-1>", stop_daemon)
but_about = Button(frame0, text="about")
but_about.bind("<Button-1>", about)
but_license = Button(frame0, text="License")
but_license.bind("<Button-1>", _license)
but_browse = Button(frame0, text="Browse", width=6)
but_browse.bind("<Button-1>", _browse)


ent_wall_dir_path = Entry(frame0, width=30, bd=3, textvariable=ent_text0)
ent_interval = Entry(frame0, width=5, bd=3, textvariable=ent_text1)


if os.access('/usr/share/wallnext/logo.gif', os.R_OK) == True:
	print('Found logo')
	img0 = PhotoImage(file="/usr/share/wallnext/logo.gif")
	canv0.create_image(0, 0, image=img0, anchor="nw")
else:
	print('Warning: no logo')
canv0.grid(row=0, column=0, columnspan=5)
frame0.grid(row=0, column=0)
#lab0.grid(row=0, column=0, columnspan=3)
lab1.grid(row=1, column=0)
combobox_wall_manager.grid(row=1,column=1,columnspan=3)
lab2.grid(row=3, column=0)
ent_wall_dir_path.grid(row=3, column=1, columnspan=3)
but_browse.grid(row=3, column=4)

lab3.grid(row=4, column=0)
ent_interval.grid(row=4, column=1)
read_subdir_cbut.grid(row=4, column=2, columnspan=2)
	

rbut_sort_random.grid(row=5, column=0)
rbut_sort_name.grid(row=5, column=0, columnspan=4)
rbut_sort_date.grid(row=5, column=1, columnspan=4)



but_about.grid(row=7, column=0)
but_license.grid(row=7, column=1)
but_ok.grid(row=7, column=2)
#but_start.grid(row=0, column=0)
but_kill.grid(row=7, column=3)
but_canc.grid(row=7, column=4)


if __name__ == '__main__':
	main()
root.mainloop()
