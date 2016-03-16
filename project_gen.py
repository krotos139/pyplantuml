#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import xml.etree.ElementTree as ET
from xml.parsers import expat
from state import StateDia
import datetime
import gantt

class ProjectParser:
	def __init__(self, filename):
		self.root = ET.parse(filename).getroot()
		self.name = self.root.find("./name").text
		self.code = self.root.find("./code").text
		self.espd_code = self.root.find("./espd_code").text
		self.lider = self.root.find("./lider").text

class PeopleParser:
	def __init__(self, filename):
		self.root = ET.parse(filename).getroot()
	def get(self, id):
		people = self.root.find("./people[@id='%s']" % id)
		if people == None:
			return None
		res = {}
		res["fullname"] = people.find("fullname").text
		res["post"] = people.find("post").text
		res["division"] = people.find("division").text
		res["subdivision"] = people.find("subdivision").text
		return res
	def idarray(self):
		peoples = self.root.findall("./people")
		for people in peoples:
			yield people.attrib["id"]

class PlanEntity:
	def __init__(self):
		self.id = ""
		self.name = ""
		self.description = []
		self.result = []
		self.people = []
		self.starttime = ""
		self.endtime = ""
		self.dfrom = []
		self.dto = []
		self.note = ""
		self.history = []
class PlanEntityLink:
	def __init__(self):
		self.name = ""
		self.direction = 0
class PlanEntityHistory:
	def __init__(self):
		self.text = ""
		self.date = None


class PlanXMLParser:
	def __init__(self, filename):
		self.es = StateDia()
		self.xml = ET.parse(filename).getroot()
		self.entityes = []
		self.parse()
	
	def parse(self):

		entityes = self.xml.findall("./entity")

		for entity in entityes:
			new_e = PlanEntity()
			new_e.id = entity.attrib["id"]
			new_e.name = entity.find("name").text
			ds = entity.findall("./description")
			for d in ds:
				new_e.description.append(d.text)
			ds = entity.findall("./result")
			for d in ds:
				new_e.result.append(d.text)
			ds = entity.findall("./people")
			for d in ds:
				new_e.people.append(d.text)
			try:
				str_starttime = entity.find("./starttime").text
				str_endtime = entity.find("./endtime").text
				starttime = datetime.datetime.strptime(str_starttime, "%d.%m.%y").date()
				endtime = datetime.datetime.strptime(str_endtime, "%d.%m.%y").date()
			except:
				new_e.starttime = None
				new_e.endtime = None
			else:
				new_e.starttime = starttime
				new_e.endtime = endtime
			try:
				new_e.note = entity.find("./note").text
			except:
				pass
			history = entity.findall("./history")
			for d in history:
				a = PlanEntityHistory()
				a.text = d.text
				a.date = datetime.datetime.strptime( d.attrib.get("date", "0") , "%d.%m.%y").date()
				new_e.history.append(a)

			froms = entity.findall("./from")
			for d in froms:
				a = PlanEntityLink()
				a.name = d.text
				a.direction = int(d.attrib.get("direction", "0"))
				new_e.dfrom.append(a)
			toes = entity.findall("./to")
			for d in toes:
				a = PlanEntityLink()
				a.name = d.text
				a.direction = int(d.attrib.get("direction", "0"))
				new_e.dto.append(a)

			self.entityes.append(new_e)


class StateDiaGen:
	def __init__(self, plan):
		self.es = StateDia()
		self.plan = plan
		self.entityes = plan.entityes
	
	def gen(self):
		for entity in self.entityes:
			id = entity.id
			name = entity.name
			e = self.es.entity(id, name)
			ds = entity.description
			for d in ds:
				e.add_desctiption(d)
			ds = entity.result
			for d in ds:
				e.add_desctiption(u"Результат: %s" % d)
			ds = entity.people
			for d in ds:
				e.add_desctiption(u"Исполнители: %s" % d)
			starttime = entity.starttime
			endtime = entity.endtime
			if starttime != None :
				e.add_desctiption(u"Срок выполнения: %s - %s" % (starttime, endtime))
			ds = entity.history
			if len(ds) > 0 :
				e.add_desctiption(u"История выполнения:" )
			for d in ds:
				e.add_desctiption(u"%s: %s" % (d.date, d.text))

			if entity.note != "":
				e.note = entity.note
		for entity in self.entityes:
			id = entity.id
			froms = entity.dfrom
			for d in froms:
				l = self.es.link(d.name, id)
				if l == None:
					print "ERROR: Can't create link on '%s'" % entity.id
					continue
				l.direction = d.direction
			toes = entity.dto
			for d in toes:
				l = self.es.link(id, d.name)
				if l == None:
					print "ERROR: Can't create link on '%s'" % entity.id
					continue
				l.direction = d.direction

	def output(self):
		self.gen()
		return self.es.plantuml().encode("utf8")
	def outfile(self, filename):
		f = open(filename, "w")
		f.write(self.output())
		f.close()

class PlanCSVGen:
	def __init__(self, plan, peoples, project):
		self.es = StateDia()
		self.plan = plan
		self.entityes = plan.entityes
		self.peoples = peoples
	
	def gen(self):
		s = ""
		s += u"Отдел|Подразделение|Шифр проекта|Описание работ|Дата начала|Дата окончания|Исполнитель|Куратор|Результаты выполнения|Примечание\n"
		for entity in self.entityes:
			if len(entity.people) == 0:
				print "WARINIG no people!!!"
				continue
			people_id = entity.people[0]
			people = self.peoples.get(people_id)
			if people == None:
				print "WARINIG no %s in reest !!!" % (people_id)
				continue

			entity_peoples = ""
			ds = entity.people
			for d in ds:
				 entity_peoples += "%s, " % d
			entity_history = ""
			ds = entity.history
			for d in ds:
				entity_history += "%s: %s\n" % (d.date, d.text)
			description = reduce(lambda res, x: "%s\n%s" % (res, x), entity.description, "")
			s += "\"%s\"|\"%s\"|\"%s\"|\"%s\"|\"%s\"|\"%s\"|\"%s\"|\"%s\"|\"%s\"|\"%s\"\n" % (
				people["division"],
				people["subdivision"],
				project.name,
				entity.name,
				entity.starttime,
				entity.endtime,
				entity_peoples,
				project.lider,
				entity_history,
				"%s\n%s" % (description, entity.note)
				)
		return s
	def output(self):
		return self.gen().encode("utf8")
	def outfile(self, filename):
		f = open(filename, "w")
		f.write(self.output())
		f.close()

class GanttGen:
	def __init__(self, plan, peoples, project):
		self.es = StateDia()
		self.plan = plan
		self.entityes = plan.entityes
		self.peoples = peoples	
		self.project = project
		self.gproject = None
		self.gen()

	def gen(self):
		# Change font default
		gantt.define_font_attributes(fill='black',
			stroke='black',
			stroke_width=0,
			font_family="Verdana")

		self.gproject = gantt.Project(name=self.project.name)

		resources = {}
		for pid in self.peoples.idarray():
			resources[pid] = gantt.Resource(pid)

		for entity in self.entityes:
			resarray = []
			for people in entity.people:
				resarray.append(resources[people])
			
			task = gantt.Task(name=entity.id,
				fullname=entity.name,
		                start=entity.starttime,
				stop=entity.endtime,
		                #duration=(entity.endtime - entity.starttime).days,
                		resources=resarray)
			self.gproject.add_task(task)

		tasks = self.gproject.get_tasks()
		for entity in self.entityes:
			task = None
			for t in tasks:
				if t.name == entity.id:
					task = t
					break
			froms = entity.dfrom
			for d in froms:
				for t in tasks:
					if t.name == d.name:
						task.add_depends([t])
						break
		return self.gproject
	def outtasks(self, filename):
		self.gproject.make_svg_for_tasks(filename=filename,
			today=datetime.date.today(),
			scale=gantt.DRAW_WITH_WEEKLY_SCALE)
	def outresources(self, filename):
		self.gproject.make_svg_for_resources(filename=filename,
			today=datetime.date.today(),
			scale=gantt.DRAW_WITH_WEEKLY_SCALE)
	def outcsv(self, filename):
		self.gproject.csv(filename)


project = ProjectParser("project.xml")
people = PeopleParser("people.xml")
plan = PlanXMLParser("state.xml")
state_dia = StateDiaGen(plan)
#parser.es.debug_print()
#print state_dia.output()
plancsv = PlanCSVGen(plan, people, project)
#print plancsv.gen()
ganttgen = GanttGen(plan, people, project)

state_dia.outfile("out_statedia.txt")
plancsv.outfile("out_plan.csv")
ganttgen.outtasks("out_gantt.svg")
ganttgen.outresources("out_resources.svg")
ganttgen.outcsv("out_csv.csv")

