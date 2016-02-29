# -*- coding: utf-8 -*-

__author__ = 'sobolevn'

from utils import get_input_function


class Storage(object):
    obj = None

    items = None

    @classmethod
    def __new__(cls, *args):
        if cls.obj is None:
            cls.obj = object.__new__(cls)
            cls.items = []
        return cls.obj


class BaseItem(object):
    def __init__(self, heading, status=False):
        self.status = status
        self.heading = heading

    def __repr__(self):
        return self.__class__

    @classmethod
    def construct(cls):
        raise NotImplemented()


class ToDoItem(BaseItem):
    def __str__(self):
        return 'ToDo: {} {}'.format(self.heading, ' - done' if self.status else '')

    @classmethod
    def construct(cls):
        input_function = get_input_function()
        heading = input_function('Input heading: ')
        return ToDoItem(heading)


class ToBuyItem(BaseItem):
    def __init__(self, heading, price):
        super(ToBuyItem, self).__init__(heading)
        self.price = price

    def __str__(self):
        return 'ToBuy: {} for {} {}'.format(self.heading, self.price, ' - done' if self.status else '')

    @classmethod
    def construct(cls):
        input_function = get_input_function()
        heading = input_function('Input heading: ')
        price = input_function('Input price: ')
        return ToBuyItem(heading, price)


class ToReadItem(BaseItem):
    def __init__(self, heading, link, due_date):
        super(ToReadItem, self).__init__(heading)
        self.link = link
        self.due_date = due_date

    def __str__(self):
        return 'ToRead: {} from {} due {} {}'.format(self.heading, self.link, self.due_date,
                                                     ' - done' if self.status else '')

    @classmethod
    def construct(cls):
        input_function = get_input_function()
        heading = input_function('Input heading: ')
        link = input_function('Input link: ')
        due_date = input_function('Input due_date: ')
        return ToReadItem(heading, link, due_date)
