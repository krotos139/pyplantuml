#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import re
import random
import xml.etree.ElementTree as ET
from xml.parsers import expat

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
		e = Entity("START", "")
		self.add(e)
		e = Entity("END", "")
		self.add(e)
	def add(self, item):
		item.parrent = self.stack_parent.peek()
		self.s.append(item)
	def add_link(self, item):
		self.l.append(item)
	def search_name(self, id):
		for d in self.s:
			if (d.id ==  id):
				return d
		return None
		
	def push_group(self, item):
		self.add(item)
		self.stack_parent.push(item)
	def pop_group(self):
		self.stack_parent.pop()

	def link(self, id1, id2):
		e1 = self.search_name(id1)
		e2 = self.search_name(id2)
		l = Link(e1, e2)
		self.add_link(l)
		return l
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





class StateXMLParser:
	def __init__(self):
		self.es = StateDia()
	
	def parse(self, filename):
		xml = ET.parse(filename).getroot()

		entityes = xml.findall("./entity")

		for entity in entityes:
			print "ENTITY"
			id = entity.attrib["id"]
			name = entity.find("name").text
			e = Entity(id, name)
			descriptions = entity.findall("./description")
			for d in descriptions:
				e.add_desctiption(d.text)
			self.es.add(e)
		for entity in entityes:
			id = entity.attrib["id"]
			froms = entity.findall("./from")
			for d in froms:
				l = self.es.link(d.text, id)
				l.direction = int(d.attrib.get("direction", "0"))
			toes = entity.findall("./to")
			for d in toes:
				l = self.es.link(id, d.text)
				l.direction = int(d.attrib.get("direction", "0"))

				
parser = StateXMLParser()
parser.parse("state.xml")
#parser.es.debug_print()
print parser.es.plantuml()

