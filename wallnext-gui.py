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


from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import fileinput
import sys
import os
import signal
from subprocess import call as _call

root = Tk(screenName=None, className='WallNext')
frame0 = Frame(root, width=300, height=600)
conf_file = StringVar()
rbut_var0 = IntVar()
rbut_var0.set(0)
rbut_var1 = IntVar()
rbut_var1.set(0)
ent_text0 = StringVar()
ent_text1 = StringVar()
ent_text2 = StringVar() 

path_wall = StringVar()
interval = IntVar()

config0 = []
version = "0.0.5"

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
	if os.access(conf_dir + 'file.conf', os.F_OK) == False:
		print('no file or dir')
		if os.access(conf_dir, os.F_OK) == False:
			print('no dir')
			os.makedirs(conf_dir)
	try:
		cf = open(conf_dir + 'file.conf', "r")
		print('norma', cf)
	except:
		cf = open(conf_dir + 'file.conf', "w")
		cf.write('0 \n' + home_dir + '\n' + '1' + '\n' + '600')
		cf.close()
		cf = open(conf_dir + 'file.conf', "r")
	
	# read conf file
	for i in fileinput.input(conf_dir + 'file.conf'):
		config0.append(i)
	print(config0)
	wall_manager = int(config0[0])
	path_wall = config0[1][:-1]
	if path_wall[-1] != '/':
		path_wall += '/'
	wall_sort = int(config0[2])
	interval = int(config0[3])
	ent_text0.set(path_wall)
	ent_text1.set(interval)
	rbut_var0.set(wall_manager)
	rbut_var1.set(wall_sort)
	conf_file.set(cf)
	cf.close()
	#return 0
	
	
def save_conf(r_var0):
	wall_manager = str(rbut_var0.get())
	path_wall = ent0.get()
	wall_sort = str(rbut_var1.get())
	interval = ent1.get()
	config0 = (wall_manager + '\n'
	+ path_wall + '\n' 
	+ wall_sort + '\n'
	+ interval)
	cf = open(conf_dir + 'file.conf', "w")
	cf.write(config0)
	cf.close()
	print(config0)
	#_call(['killall'])
	try:
		root.destroy()
		_call(['wallnext'])
		
		#sys.exit()
	except:
		try:
			_call(['./wallnext'])
		except:
			_call(['./wallnext.py'])
	#return 0
	
	
# start daemon
def start_daemon(r_var0):
	wall_manager = str(rbut_var0.get())
	path_wall = ent0.get()
	interval = ent1.get()
	config0 = (wall_manager + '\n'
	+ path_wall + '\n' + 
	interval)
	cf = open(conf_dir + 'file.conf', "w")
	cf.write(config0)
	cf.close()
	print(config0)
	#_call(['killall'])
	try:
		#root.destroy()
		_call(['wallnext'])
		
		#sys.exit()
	except:
		_call(['wallnext.py'])


# stop daemon
def stop_daemon(x1):	
	print(conf_dir)
	try:
		cf = open(conf_dir + 'pid', "r")
		print('open')
		kill_pid = int(cf.readline())
		print(kill_pid)
		os.kill(kill_pid, signal.SIGTERM)
		print('kill')
		cf.close()
	except:
		print('except kill')


def about(x):
     showinfo("Editor", "  WallNext \nVersion " + version + 
     "\nThis product includes software developed by a Bessonov Jurij \n \
     aka Strannik-j (http://strannik-j.org) and his contributors.")


def _license(x):
	print()
	win0 = Toplevel(root, bd=5)
	win0.title("License")
	win0.minsize(width=400, height=400) 
	txt0 = Text(win0, width=80, height=30, font="10", wrap=WORD)
	txt0.insert(END, license0)
	txt0.pack()


canv0 = Canvas(frame0, width=500, height=50, bg="lightblue")	
lab0 = Label(frame0, text="Wallpappers changer", font="Sans 12")
lab1 = Label(frame0, text="Desktop manager", font="Sans 10")
lab2 = Label(frame0, text="PATH to wallpappers: ", font="Arial 10")
lab3 = Label(frame0, text="Time interval (sec): ", font="Arial 10")
#lab4 = Label(frame0, text="Sort", font="Arial 10")
rbut0 = Radiobutton(frame0, text="pcmanfm", variable=rbut_var0, value=0)
rbut1 = Radiobutton(frame0, text="Nautilus", variable=rbut_var0, value=1)
rbut2 = Radiobutton(frame0, text="Random", variable=rbut_var1, value=0)
rbut3 = Radiobutton(frame0, text="Sort by name", variable=rbut_var1, value=1)
rbut4 = Radiobutton(frame0, text="Sort by date", variable=rbut_var1, value=2)
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
ent0 = Entry(frame0, width=30, bd=3, textvariable=ent_text0)
ent1 = Entry(frame0, width=5, bd=3, textvariable=ent_text1)
img0 = PhotoImage(file="/usr/share/wallnext/logo.gif")
canv0.create_image(0, 0, image=img0, anchor="nw")

canv0.grid(row=0, column=0, columnspan=5)
frame0.grid(row=0, column=0)
#lab0.grid(row=0, column=0, columnspan=3)
lab1.grid(row=1, column=0)
rbut0.grid(row=2, column=0)
rbut1.grid(row=2, column=1)
lab2.grid(row=3, column=0)
ent0.grid(row=3, column=1, columnspan=4)
rbut2.grid(row=4, column=0)
rbut3.grid(row=4, column=0, columnspan=4)
rbut4.grid(row=4, column=1, columnspan=4)
lab3.grid(row=5, column=0)
ent1.grid(row=5, column=1)
	

but_about.grid(row=7, column=0)
but_license.grid(row=7, column=1)
but_ok.grid(row=7, column=2)
#but_start.grid(row=0, column=0)
but_kill.grid(row=7, column=3)
but_canc.grid(row=7, column=4)


if __name__ == '__main__':
	main()
root.mainloop()
