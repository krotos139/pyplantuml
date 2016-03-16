#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import re
import random

class Stack:
	def __init__(self):
		self.items = []

	def isEmpty(self):
		return self.items == []

	def push(self, item):
		self.items.append(item)

	def pop(self):
		return self.items.pop()

	def peek(self):
		if (len(self.items) == 0):
			return None
		return self.items[len(self.items)-1]

	def size(self):
		return len(self.items)

class Entity:
	def __init__(self, id, name = ""):
		self.id = id
		self.parrent = None
		self.name = name
		self.note = ""
		self.desc = []
	def add_desctiption(self, s):
		self.desc.append(s)
	def add_note(self, s):
		self.note = s

class Link:
	def __init__(self, e1, e2):
		self.id = None
		self.e_from = e1
		self.e_to = e2
		self.title = ""
		self.direction = 0
	def set_title(self, title):
		self.title = title
		
class StateDia:
	def __init__(self):
		self.s = []
		self.l = []
		self.stack_parent = Stack()
		self.entity("START", "")
		self.entity("END", "")
	def entity(self, id, name):
		item = Entity(id, name)
		item.parrent = self.stack_parent.peek()
		self.s.append(item)
		return item
	def link(self, id1, id2):
		e1 = self.search_name(id1)
		e2 = self.search_name(id2)
		if (e1 == None):
			print "ERROR: not found '%s'" % id1
			return None
		if (e2 == None):
			print "ERROR: not found '%s'" % id2
			return None
		l = Link(e1, e2)
		self.l.append(l)
		return l

	def search_name(self, id):
		for d in self.s:
			if (d.id ==  id):
				return d
		return None
		
	def push_group(self, item):
		self.stack_parent.push(item)
	def pop_group(self):
		self.stack_parent.pop()

	def debug_print(self):
		for d in self.s:
			print "Entity: "
			print " ID: %s" % d.id
			print " Name: %s" % d.name
			print " Note: %s" % d.note
			print " Parrent: %s" % d.parrent
		for d in self.l:
			print "Link: "
			print " From: %s" % d.e_from.id
			print " To: %s" % d.e_to.id
			print " Title: %s" % d.title
	def plantuml(self):
		s = "@startuml\n"
		for d in self.s:
			if (d.id == "START") | (d.id == "END"):
				continue
			s += "state \"%s\" as %s\n" % (d.name, d.id)
			for i in d.desc:
				s += "%s : %s\n" % (d.id, i)
			if d.note != "":
				s += "note right of %s: %s\n" % (d.id, d.note)
		for d in self.l:
			def sprep(x):
				if (x == "START") | (x == "END"):
					return "[*]"
				return x
			s_from = sprep(d.e_from.id)
			s_to = sprep(d.e_to.id)
			if (d.direction == 0):
				delimiter = "-->"
			else:
				delimiter = "->"
			if d.title == "":
				s += "%s %s %s\n" % (s_from, delimiter, s_to)
			else:
				s += "%s %s %s : %s\n" % (s_from, delimiter, s_to, d.title)
		s += "@enduml\n"
		return s






