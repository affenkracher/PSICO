import sys
import operator
import re
import pygame
import os
from PIL import Image
from collections import defaultdict


sizeMappings = {1:(44,44),2:(65, 47),3:(90, 47),4:(116, 47),5:(49, 28),6:(260,54),8:(50, 54),7:(49,54)}

keyMappings = {"esc":(40,73,5),"~":(40, 118,1),"`":(40,118,1),"1":(93 ,118,1),"2":(146, 118,1),"3":(199, 118,1),"4":(255, 118,1),"5":(308, 118,1),"6":(362, 118,1),"7":(417, 118,1),"8":(470, 118,1),"9":(525, 118,1),"0":(579, 118,1),"!":(93 ,118,1),"@":(146, 118,1),"#":(199, 118,1),"$":(255, 118,1),"%":(308, 118,1),"^":(362, 118,1),"&":(417, 118,1),"*":(470, 118,1),"(":(525, 118,1),")":(579, 118,1),"-":(633, 118,1),"=":(686, 118,1),"_":(633, 118,1),"+":(686, 118,1),"del":(755, 118,2),"tab":(50 ,171,2),"q":(118, 171,1),"w":(172, 171,1),"e":(226, 171,1),"r":(280, 171,1),"t":(334, 171,1),"y":(388, 171,1),"u":(442, 171,1),"i":(496, 171,1),"o":(550, 171,1),"p":(604, 171,1),"[":(658, 171,1),"{":(658, 171,1),"]":(712, 171,1),"}":(712, 171,1),"\\":(766, 171,1),"|":(766, 171,1),"a":(133, 222,1),"s":(187, 222,1),"d":(241, 222,1),"f":(295, 222,1),"g":(349, 222,1),"h":(403, 222,1),"j":(457, 222,1),"k":(511, 222,1),"l":(565, 222,1),":":(619, 222,1),";":(619, 222,1),"'":(673, 222,1),"\"":(673, 222,1),"\n":(752, 222,3),"shift":(76 ,275,4),"z":(160, 275,1),"x":(214, 275,1),"c":(268, 275,1),"v":(322, 275,1),"b":(376, 275,1),"n":(430, 275,1),"m":(484, 275,1),",":(538, 275,1),".":(592, 275,1),"<":(538, 275,1),">":(592, 275,1),"/":(646, 275,1),"?":(646, 275,1),"fn":(39 ,331,7),"ctrl":(92 ,331,7),"opt":(147, 331,7),"cmd":(207, 331,8)," ":(378, 331, 6),"up":(714, 318,5),"left":(660, 343,5),"down":(714, 343,5),"right":(767, 343,5)}

numKeymappings = {27 :"esc",96 :"~",49 :"1",50 :"2",51 :"3",52 :"4",53 :"5",54 :"6",55 :"7",56 :"8",57 :"9",48 :"0",45 :"-",61 :"=",8 :"del",9 :"tab",113 :"q",119 :"w",101 :"e",114 :"r",116 :"t",121 :"y",117 :"u",105 :"i",111 :"o",112 :"p",91 :"[",93 :"]",92 :"\\",97 :"a",115 :"s",100 :"d",102 :"f",103 :"g",104 :"h",106 :"j",107 :"k",108 :"l",59 :";",39 :"'",13 :"\n",304 :"shift",122 :"z",120 :"x",99 :"c",118 :"v",98 :"b",110 :"n",109 :"m",44 :",",46 :".",47 :"/",306 :"ctrl",308 :"opt",310 :"cmd",32 :" ",273 :"up",276 :"left",274 :"down",275 :"right"}

outputfile = "heatmapkeyboard.jpeg"


def load_file():
	#open file
	f = open("logfile.txt", 'r')
	fstr = f.read()
	keyCount = {}
	
	#convert special comands
	cmd = [m.start() for m in re.finditer('\<cmd\>', fstr)]
	keyCount['cmd'] = len(cmd)
	fstr = fstr.replace('<cmd>', '')

	cmd = [m.start() for m in re.finditer('\<del\>', fstr)]
	keyCount['del'] = len(cmd)
	fstr = fstr.replace('<del>', '')

	cmd = [m.start() for m in re.finditer('\<shift\>', fstr)]
	keyCount['shift'] = len(cmd)
	fstr = fstr.replace('<shift>', '')

	cmd = [m.start() for m in re.finditer('\<cntrl\>', fstr)]
	keyCount['ctrl'] = len(cmd)
	fstr = fstr.replace('<cntrl>', '')
	cmd = [m.start() for m in re.finditer('\<ctrl\>', fstr)]
	keyCount['ctrl'] = keyCount['ctrl'] + len(cmd)
	fstr = fstr.replace('<ctrl>', '')

	cmd = [m.start() for m in re.finditer('\<opt\>', fstr)]
	keyCount['opt'] = len(cmd)
	fstr = fstr.replace('<opt>', '')

	cmd = [m.start() for m in re.finditer('\<esc\>', fstr)]
	keyCount['esc'] = len(cmd)
	fstr = fstr.replace('<esc>', '')

	cmd = [m.start() for m in re.finditer('\<fn\>', fstr)]
	keyCount['fn'] = len(cmd)
	fstr = fstr.replace('<fn>', '')

	cmd = [m.start() for m in re.finditer('\<tab\>', fstr)]
	keyCount['tab'] = len(cmd)
	fstr = fstr.replace('<tab>', '')

	cmd = [m.start() for m in re.finditer('\<left\>', fstr)]
	cmd2 = [m.start() for m in re.finditer('\<eft\>', fstr)]
	keyCount['left'] = len(cmd) + len(cmd2)
	fstr = fstr.replace('<left>', '')
	fstr = fstr.replace('<eft>', '')

	cmd = [m.start() for m in re.finditer('\<up\>', fstr)]
	keyCount['up'] = len(cmd)
	fstr = fstr.replace('<up>', '')

	cmd = [m.start() for m in re.finditer('\<down\>', fstr)]
	keyCount['down'] = len(cmd)
	fstr = fstr.replace('<down>', '')

	cmd = [m.start() for m in re.finditer('\<right\>', fstr)]
	keyCount['right'] = len(cmd)
	fstr = fstr.replace('<right>', '')

	
	#remove error keys
	fstr = fstr.replace('Ã', '')
	fstr = fstr.replace('¼', '')
	fstr = fstr.replace('±', '')
	
	#count keys
	for char in fstr:
		if char.istitle():
			keyCount['shift'] +=1
			char = char.lower()
		if char in "\":{}|!@#$%^&*()_+":
			keyCount['shift'] +=1
		if char in keyCount:
			keyCount[char] +=1
		else:
			keyCount[char] = 1
		
	#sort counted keys
	sortedCount = sorted(keyCount.items(), key=operator.itemgetter(1))
	return sortedCount


def display(dt, screen):
	# sum of all keys
	allkeys = 0
	for key, count in dt:
		allkeys += count
	#check wether keys were pressed
	if allkeys != 0:
		for key, count in dt:
			#calculate percentage and adjust
			countfactor = (count/allkeys)*100
			#prepare drawing
			centX = keyMappings[key][0]
			centY = keyMappings[key][1]
			width = sizeMappings[keyMappings[key][2]][0]
			height = sizeMappings[keyMappings[key][2]][1]
			s = pygame.Surface((width, height))
			s.set_alpha(155)
			print(key)
			print(countfactor)
			#set color
			# if countfactor < 1:
			# 	s.fill((255,0,125))
			# elif countfactor < 2:
			# 	s.fill((255,0,255))
			if 0 == countfactor:
				pass
			elif countfactor < 1:
				s.fill((125,0,255))
			elif countfactor < 2:
				s.fill((0,0,255))
			elif countfactor < 3:
				s.fill((0,125,255))
			elif countfactor < 4:
				s.fill((0,255,255))
			elif countfactor < 5:
				s.fill((0,255,125))
			elif countfactor < 6:
				s.fill((0,255,0))
			elif countfactor < 7:
				s.fill((125,255,0))
			elif countfactor < 8:
				s.fill((255,255,0))
			elif countfactor < 9:
				s.fill((255,125,0))
			else:
				s.fill((255,0,0))
			#draw
			screen.blit(s, (centX - width/2, centY - height/2))

def main():
	#create background
	pygame.init()
	keyboard = pygame.image.load("keyboard.png")
	keyRect = keyboard.get_rect()
	size = (width, height) = keyboard.get_size()
	screen = pygame.display.set_mode(size)
	screen.blit(keyboard, keyRect)
	pygame.display.update()
	#load keys
	count = load_file()
	#display keys
	display(count, screen)
	pygame.display.update()
	#save image
	pygame.image.save(screen, outputfile)


main()