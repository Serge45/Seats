# -*- encoding: utf-8 -*-
import json

class Student:
    def __init__(self, name='blank', row=0, column=0, count=0):
        self.name = name
        self.position_row = row
        self.position_column = column
        self.count = 0
    def as_json(self):
        d = {}
        d['name'] = self.name
        d['row'] = self.position_row
        d['col'] = self.position_column
        d['count'] = self.count

        return json.dumps(d, ensure_ascii=False)


if __name__ == '__main__':
    s = Student('呵呵')
    print s.as_json()