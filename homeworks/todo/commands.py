# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import inspect
import json
import shelve

from custom_exceptions import UserExitException
from models import BaseItem
from utils import get_input_function

__author__ = 'sobolevn'


class BaseCommand(object):
    def __init__(self, command):
        self._command = command

    @property
    def command(self):
        return self._command

    @staticmethod
    def label():
        raise NotImplemented()

    def perform(self, objects, *args, **kwargs):
        raise NotImplemented()


class ListCommand(BaseCommand):
    @staticmethod
    def label():
        return 'list'

    def perform(self, objects, *args, **kwargs):
        if len(objects) == 0:
            print('There are no items in storage.')
            return

        for index, obj in enumerate(objects):
            print('{}: {}'.format(index, str(obj)))


class NewCommand(BaseCommand):
    @staticmethod
    def label():
        return 'new'

    @staticmethod
    def _load_item_classes():

        def class_filter(klass):
            return inspect.isclass(klass) \
                   and klass.__module__ == BaseItem.__module__ \
                   and issubclass(klass, BaseItem) \
                   and klass is not BaseItem

        classes = inspect.getmembers(
            sys.modules[BaseItem.__module__],
            class_filter
        )
        return dict(classes)

    def perform(self, objects, *args, **kwargs):
        classes = self._load_item_classes()

        print('Select item type:')
        for index, name in enumerate(classes.keys()):
            print('{}: {}'.format(index, name))

        input_function = get_input_function()
        selection = None

        while True:
            try:
                selection = int(input_function('Input number: '))
                break
            except ValueError:
                print('Bad input, try again.')

        selected_key = list(classes.keys())[selection]
        selected_class = classes[selected_key]
        print('Selected: {}'.format(selected_class.__name__))
        print()

        new_object = selected_class.construct()

        objects.append(new_object)
        print('Added {}'.format(str(new_object)))
        print()
        return new_object


class ExitCommand(BaseCommand):
    @staticmethod
    def label():
        return 'exit'

    def perform(self, objects, *args, **kwargs):
        raise UserExitException('See you next time!')


class DoneCommand(BaseCommand):
    @staticmethod
    def label():
        return 'done'

    def perform(self, objects, *args, **kwargs):
        if len(objects) == 0:
            print('There are no items in storage.')
            return

        for index, obj in enumerate(objects):
            print('{}: {}'.format(index, str(obj)))

        print('Select item')
        input_function = get_input_function()
        selection = None

        while True:
            try:
                selection = int(input_function('Input number: '))
                break
            except ValueError:
                print('Bad input, try again.')

        objects[selection].status = True
        return selection


class UndoneCommand(BaseCommand):
    @staticmethod
    def label():
        return 'undone'

    def perform(self, objects, *args, **kwargs):
        selection = DoneCommand.perform(self, objects, *args, **kwargs)
        objects[selection].status = False


# class TestUndoneCommand(DoneCommand):
#     @staticmethod
#     def label():
#         return 'test'
#
#     def perform(self, objects, *args, **kwargs):
#         super().perform(objects, *args, **kwargs)

class SortCommand(BaseCommand):
    @staticmethod
    def label():
        return 'sort'

    def perform(self, objects, *args, **kwargs):
        input_function = get_input_function()
        sort_methods = ['By complete', 'By title']
        for i, method in enumerate(sort_methods):
            print('{}: {}'.format(i, method))
        sort_method = input_function('Select Sorting method: ')
        if sort_method == '1':
            objects.sort(key=lambda x: str(x))
        elif sort_method == '0':
            objects.sort(key=lambda x: x.status)


class SaveCommand(BaseCommand):
    @staticmethod
    def label():
        return 'save'

    def perform(self, objects, *args, **kwargs):
        db = shelve.open('tododb')
        for i, obj in enumerate(objects):
            db[str(i)] = obj
        db.close()


class LoadCommand(BaseCommand):
    @staticmethod
    def label():
        return 'load'

    def perform(self, objects, *args, **kwargs):
        db = shelve.open('tododb')
        for key in db:
            objects.append(db[key])
        db.close()
