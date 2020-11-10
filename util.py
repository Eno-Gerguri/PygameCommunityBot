import sys, os, time, asyncio
import discord, pygame, numpy, threading
from typing import Union

# Safe subscripting
def safeSub(li, ind):
	try:
		return li[ind]
	except:
		return ''

# Split
def split(com):
	spl = []
	tm = ''
	for c in com:
		if c in [' ', '\n']:
			if tm != '':
				spl.append(tm)
				tm = ''
		else:
			tm += c
	if tm != '':
		spl.append(tm)
	return spl


# Filters mention to get ID '<@!6969>' to 6969
def filterID(mention):
	a = mention.split('<')
	a = ''.join(a).split('@')
	a = ''.join(a).split('!')
	a = ''.join(''.join(a).split('>'))
	return a

# Sends an embed with a much more tight function
async def sendEmbed(channel, title, description, color=0xFFFFAA):
	await channel.send(embed=discord.Embed(title=title, description=description, color=color))

class ThreadWithTrace(threading.Thread):
	def __init__(self, *args, **keywords):
		threading.Thread.__init__(self, *args, **keywords)
		self.killed = False

	def start(self):
		self.__run_backup = self.run
		self.run = self.__run
		threading.Thread.start(self)

	def __run(self):
		sys.settrace(self.globaltrace)
		self.__run_backup()
		self.run = self.__run_backup

	def globaltrace(self, frame, event, arg):
		if event == 'call':
			return self.localtrace
		else:
			return None

	def localtrace(self, frame, event, arg):
		if self.killed:
			if event == 'line':
				raise SystemExit()
		return self.localtrace

	def kill(self):
		self.killed = True