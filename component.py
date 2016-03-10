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
	def __init__(self):
		self.id = None
		self.parrent = None
		self.name = ""
		self.type = None
		self.note = ""
	def as_component(self, id, name):
		self.type = 1
		if (id != None):
			self.id = id
			self.name = name
		else:
			self.id = name
			self.name = name
	def as_interface(self, id, name):
		self.type = 2
		if (id != None):
			self.id = id
			self.name = name
		else:
			self.id = name
			self.name = name
	def as_group(self, type, name):
		if (type == "package"):
			self.type = 4
		elif (type == "node"):
			self.type = 5
		elif (type == "folder"):
			self.type = 6
		elif (type == "frame"):
			self.type = 7
		elif (type == "cloud"):
			self.type = 8
		elif (type == "database"):
			self.type = 8
		if (name != None):
			self.id = name
			self.name = name
		else:
			self.id = ""
			self.name = type
	def to_str(self):
		return "Entity"

class Link:
	def __init__(self):
		self.id = None
		self.e_from = None
		self.e_to = None
		self.title = ""
		self.type = None
	def association(self, e1, e2, title):
		self.type = 1
		self.e_from = e1
		self.e_to = e2
		self.title = title
	def generalization(self, e1, e2, title):
		self.type = 2
		self.e_from = e1
		self.e_to = e2
		self.title = title
	def dependency(self, e1, e2, title):
		self.type = 3
		self.e_from = e1
		self.e_to = e2
		self.title = title

		
class Entities:
	def __init__(self):
		self.s = []
		self.l = []
		self.stack_parent = Stack()
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
	def add_component(self, id, name):
		e = Entity()
		e.as_component(id, name)
		self.add(e)
		return e
	def add_interface(self, id, name):
		e = Entity()
		e.as_interface(id, name)
		self.add(e)
		return e
	def maybe_component(self, id):
		if (self.search_name(id) == None):
			e = Entity()
			e.as_component(id, None)
			self.add(e)
	def maybe_interface(self, id):
		if (self.search_name(id) == None):
			e = Entity()
			e.as_interface(id, None)
			self.add(e)
	def association(self, id1, id2, title):
		e1 = self.search_name(id1)
		e2 = self.search_name(id2)
		l = Link()
		l.association(e1, e2, title)
		self.add_link(l)
	def generalization(self, id1, id2, title):
		e1 = self.search_name(id1)
		e2 = self.search_name(id2)
		l = Link()
		l.generalization(e1, e2, title)
		self.add_link(l)
	def dependency(self, id1, id2, title):
		e1 = self.search_name(id1)
		e2 = self.search_name(id2)
		l = Link()
		l.dependency(e1, e2, title)
		self.add_link(l)
	def note(self, id, note):
		e = self.search_name(id)
		e.note = note
	def debug_print(self):
		for d in self.s:
			print "Entity: "
			if (d.type  == 1):
				print " Component"
			if (d.type  == 2):
				print " Interface"
			if (d.type  >3):
				print " Group"
			print " ID: %s" % d.id
			print " Name: %s" % d.name
			print " Note: %s" % d.note
			print " Parrent: %s" % d.parrent
		for d in self.l:
			print "Link: "
			if (d.type  == 1):
				print " Association"
				print " From: %s" % d.e_from.id
				print " To: %s" % d.e_to.id
				print " Title: %s" % d.title
			if (d.type  == 2):
				print " Generalization"
				print " From: %s" % d.e_from.id
				print " To: %s" % d.e_to.id
				print " Title: %s" % d.title
			if (d.type  == 3):
				print " Dependency"
				print " From: %s" % d.e_from.id
				print " To: %s" % d.e_to.id
				print " Title: %s" % d.title

class ComponentTextRuGen:
	def __init__(self, diagramm):
		self.dia = diagramm
		self.Name = u"Проект"
		self.name = u"проект"
	def rand(self, percent):
		r = random.randint(1, 100)
		return r<=percent
	def t_use(self):
		r = random.randint(1, 2)
		if r == 1:
			return u"использует"
		elif r == 2:
			return u"применяет"
			

	def text_interface(self):
		entries = self.dia.s
		count = 0
		a = []
		for i in entries:
			if i.type == 2:
				count += 1
				a.append(i)
		print a
		if count == 0:
			r = random.randint(1, 2)
			if r == 1:
				print self.Name + "не "+self.t_use()+" интерфейсы"
		elif count == 1:
			r = random.randint(1, 2)
			if r == 1:
				print self.Name + u" "+self.t_use()+u" интерфейс "+str(a[0].name)

			else:
				print self.Name + u" "+self.t_use()+" "+str(a[0].name)
		elif count <4:
			r = random.randint(1, 2)
			if r == 1:
				print u"Проект использует интерфейс %s" % (a[0].name)
			else:
				print u"Проект использует интерфейс %s" % (a[0].name)

			if self.rand(50):
				print u"В проекте %d интерфейсов" % (count)


	def generate(self):
		print "Generate:"
		self.text_interface()



class ComponentDiagramParser:
	def __init__(self):
		self.es = Entities()
		self.startuml = re.compile(r'@startuml',re.U)
		self.start = re.compile(ur'^\ *(?P<type>\w+)( \"(?P<name>.+)\")* {$',re.U)
		self.stop = re.compile(ur'^\ *}\ *$',re.U)
		self.component1 = re.compile(ur'^\ *\[(?P<name>[\w ]+)\]( as (?P<id>\w+))*\ *$',re.U)
		self.component2 = re.compile(ur'^\ *component \[*(?P<name>[\w \\]+)\]*( as (?P<id>\w+))*\ *$',re.U)
		self.interface1 = re.compile(ur'^\ *\(\) \"(?P<name>[\w ]+)\"( as (?P<id>\w+))*\ *$',re.U)
		self.interface2 = re.compile(ur'^\ *interface \"*(?P<name>[\w \\]+)\"*( as (?P<id>\w+))*\ *$',re.U)
		self.link_association_1 = re.compile(ur'^\ *((?P<interface1>[\w]+)|\[(?P<component1>[\w ]+)\]) - ((?P<interface2>[\w]+)|\[(?P<component2>[\w ]+)\])( : (?P<title>[\w \\]+))*',re.U)
		self.link_generalization_1 = re.compile(ur'^\ *((?P<interface1>[\w]+)|\[(?P<component1>[\w ]+)\]) (->|-->) ((?P<interface2>[\w]+)|\[(?P<component2>[\w ]+)\])( : (?P<title>[\w \\]+))*',re.U)
		self.link_generalization_2 = re.compile(ur'^\ *((?P<interface2>[\w]+)|\[(?P<component2>[\w ]+)\]) (<-|<--) ((?P<interface1>[\w]+)|\[(?P<component1>[\w ]+)\])( : (?P<title>[\w \\]+))*',re.U)
		self.link_generalization_3 = re.compile(ur'^\ *((?P<interface1>[\w]+)|\[(?P<component1>[\w ]+)\]) -(?P<direction>left|right|up|down)-> ((?P<interface2>[\w]+)|\[(?P<component2>[\w ]+)\])( : (?P<title>[\w \\]+))*',re.U)
		self.link_dependency_1 = re.compile(ur'^\ *((?P<interface1>[\w]+)|\[(?P<component1>[\w ]+)\]) \.\.> ((?P<interface2>[\w]+)|\[(?P<component2>[\w ]+)\])( : (?P<title>[\w \\]+))*',re.U)
		self.link_dependency_2 = re.compile(ur'^\ *((?P<interface2>[\w]+)|\[(?P<component2>[\w ]+)\]) <\.\. ((?P<interface1>[\w]+)|\[(?P<component1>[\w ]+)\])( : (?P<title>[\w \\]+))*',re.U)
		self.note1 = re.compile(ur'^note (?P<direction>left|right|top|bottom) of ((?P<interface>[\w]+)|\[(?P<component>[\w ]+)\]) : (?P<description>[\w \\]+)$',re.U)
		self.note_start = re.compile(ur'^note (?P<direction>left|right|top|bottom) of ((?P<interface>[\w]+)|\[(?P<component>[\w ]+)\])$',re.U)
		self.note_stop = re.compile(ur'^end note$',re.U)
	
	def parse(self, file):
		f = open(file, 'r')

		data = f.readlines()


		note_multiline = False
		note_id = None
		note_text = ""
		for ds in data:
			d = ds.decode('CP1251')
			m = self.startuml.match(d)
			if m != None:
				print "StartUML"
			m = self.component1.match(d)
			if m != None:
				print "COMPONENT 1"
				gd = m.groupdict()
				e = Entity()
				e.as_component(gd["id"], gd["name"])
				self.es.add(e)
			m = self.component2.match(d)
			if m != None:
				print "COMPONENT 2"
				gd = m.groupdict()
				e = Entity()
				e.as_component(gd["id"], gd["name"])
				self.es.add(e)
			m = self.interface1.match(d)
			if m != None:
				print "INTERFACE 1"
				gd = m.groupdict()
				e = Entity()
				e.as_interface(gd["id"], gd["name"])
				self.es.add(e)
			m = self.interface2.match(d)
			if m != None:
				print "INTERFACE 2"
				gd = m.groupdict()
				e = Entity()
				e.as_interface(gd["id"], gd["name"])
				self.es.add(e)
			m = self.link_association_1.match(d)
			if m != None:
				print "LINK Association 1"
				gd = m.groupdict()
				if (gd["interface1"] != None):
					id1 = gd["interface1"]
					self.es.maybe_interface(id1)
				if (gd["interface2"] != None):
					id2 = gd["interface2"]
					self.es.maybe_interface(id2)
				if (gd["component1"] != None):
					id1 = gd["component1"]
					self.es.maybe_component(id1)
				if (gd["component2"] != None):
					id2 = gd["component2"]
					self.es.maybe_component(id2)
				self.es.association(id1, id2, gd["title"])
			m = self.link_generalization_1.match(d)
			if m != None:
				print "LINK Generalization 1"
				gd = m.groupdict()
				if (gd["interface1"] != None):
					id1 = gd["interface1"]
					self.es.maybe_interface(id1)
				if (gd["interface2"] != None):
					id2 = gd["interface2"]
					self.es.maybe_interface(id2)
				if (gd["component1"] != None):
					id1 = gd["component1"]
					self.es.maybe_component(id1)
				if (gd["component2"] != None):
					id2 = gd["component2"]
					self.es.maybe_component(id2)
				self.es.generalization(id1, id2, gd["title"])
			m = self.link_generalization_2.match(d)
			if m != None:
				print "LINK Generalization 2"
				gd = m.groupdict()
				if (gd["interface1"] != None):
					id1 = gd["interface1"]
					self.es.maybe_interface(id1)
				if (gd["interface2"] != None):
					id2 = gd["interface2"]
					self.es.maybe_interface(id2)
				if (gd["component1"] != None):
					id1 = gd["component1"]
					self.es.maybe_component(id1)
				if (gd["component2"] != None):
					id2 = gd["component2"]
					self.es.maybe_component(id2)
				self.es.generalization(id1, id2, gd["title"])
			m = self.link_generalization_3.match(d)
			if m != None:
				print "LINK Generalization 3"
				gd = m.groupdict()
				if (gd["interface1"] != None):
					id1 = gd["interface1"]
					self.es.maybe_interface(id1)
				if (gd["interface2"] != None):
					id2 = gd["interface2"]
					self.es.maybe_interface(id2)
				if (gd["component1"] != None):
					id1 = gd["component1"]
					self.es.maybe_component(id1)
				if (gd["component2"] != None):
					id2 = gd["component2"]
					self.es.maybe_component(id2)
				self.es.generalization(id1, id2, gd["title"])
			m = self.link_dependency_1.match(d)
			if m != None:
				print "LINK Dependency 1"
				gd = m.groupdict()
				if (gd["interface1"] != None):
					id1 = gd["interface1"]
					self.es.maybe_interface(id1)
				if (gd["interface2"] != None):
					id2 = gd["interface2"]
					self.es.maybe_interface(id2)
				if (gd["component1"] != None):
					id1 = gd["component1"]
					self.es.maybe_component(id1)
				if (gd["component2"] != None):
					id2 = gd["component2"]
					self.es.maybe_component(id2)
				self.es.dependency(id1, id2, gd["title"])
			m = self.link_dependency_2.match(d)
			if m != None:
				print "LINK Dependency 2"
				gd = m.groupdict()
				if (gd["interface1"] != None):
					id1 = gd["interface1"]
					self.es.maybe_interface(id1)
				if (gd["interface2"] != None):
					id2 = gd["interface2"]
					self.es.maybe_interface(id2)
				if (gd["component1"] != None):
					id1 = gd["component1"]
					self.es.maybe_component(id1)
				if (gd["component2"] != None):
					id2 = gd["component2"]
					self.es.maybe_component(id2)
				self.es.dependency(id1, id2, gd["title"])
			m = self.note1.match(d)
			if m != None:
				print "NOTE 1"
				gd = m.groupdict()
				if (gd["interface"] != None):
					id = gd["interface"]
					self.es.maybe_interface(id)
				if (gd["component"] != None):
					id = gd["component"]
					self.es.maybe_component(id)
				self.es.note(id, gd["description"])
			m = self.note_stop.match(d)
			if m != None:
				print "NOTE STOP"
				note_multiline = False
				self.es.note(note_id, note_text)
			if (note_multiline):
				note_text += d + "\n"
			m = self.note_start.match(d)
			if m != None:
				print "NOTE START"
				note_multiline = True
				gd = m.groupdict()
				if (gd["interface"] != None):
					note_id = gd["interface"]
					self.es.maybe_interface(note_id)
				if (gd["component"] != None):
					note_id = gd["component"]
					self.es.maybe_component(note_id)
				note_text = ""
			m = self.start.match(d)
			if m != None:
				print "START 1"
				gd = m.groupdict()
				e = Entity()
				e.as_group(gd["type"], gd["name"])
				self.es.push_group(e)
			m = self.stop.match(d)
			if m != None:
				print "STOP"
				self.es.pop_group()
				
parser = ComponentDiagramParser()
parser.parse("3.txt")
gen = ComponentTextRuGen(parser.es)
parser.es.debug_print()

gen.generate()

