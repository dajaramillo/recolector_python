# -*- coding: utf-8 -*-
__author__ = 'Daniel Jaramillo'

class dato:

    def __init__(self, username, name, date_time,date, time, page, section, subsection, unit, session, course, answers):
        self.username = username
        self.name = name
        self.date_time = date_time
        self.date = date
        self.time = time
        self.page = page
        self.section = section
        self.subsection = subsection
        self.unit = unit
        self.session = session
        self.course = course
        self.answers = answers
        
    def toDBCollection (self):
        return {
            "username":self.username,
            "name": self.name,
            "date_time": self.date_time,
            "date": self.date,
            "time": self.time,
            "page": self.page,
            "section": self.section,
            "subsection": self.subsection,
            "unit": self.unit,
            "session": self.session,
            "course": self.course,
            "answers": self.answers
        }

    def __str__(self):
        return "username: %s - name: %s -date_time: %s - date: %s - time: %s - page: %s - section: %s - subsection: %s - unit: %s - session: %s - course: %s - answers: %s" \
               %(self.username, self.name, self.date_time, self.date, self.time, self.page, self.section, self.subsection, self.unit, self.session, self.course, self.answers)