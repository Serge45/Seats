# -*- encoding: utf-8 -*-
import json

class Student:
    def __init__(self, name='blank', row=0, column=0, count=0, num=0):
        self.name = name
        self.row = row
        self.col = column
        self.count = 0
        self.num = num
    def as_json(self):
        d = {}
        d['name'] = self.name
        d['row'] = self.row
        d['col'] = self.col
        d['count'] = self.count
        d['num'] = self.num

        return json.dumps(d, ensure_ascii=False)


if __name__ == '__main__':
    s = Student('呵呵')
    print s.as_json()