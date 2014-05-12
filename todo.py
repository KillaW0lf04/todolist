#! /usr/bin/python3m

"""
Simple Todolist manager for the command line that allows you to view, add or mark tasks as complete
Author: Michael Aquilina 2014
"""

import re
import os


def write_todo(tasks, path):

    with open(path, 'w') as f:
        for data in tasks:
            f.write('* %s\n' % data)


def read_todo(path):
    """
    Parses the todo list in the given path and returns a dictionary of values
    organised by their ID. Returns an empty dictionary if no todo list is available.
    """

    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        data = f.readlines()

    tasks = []
    for line in data:
        m = re.match(r'\* (?P<data>.*)', line)
        task_data = m.group('data')

        tasks.append(task_data)

    return tasks


if __name__ == '__main__':
    import argparse

    path = os.path.expanduser('~/todo.md')

    parser = argparse.ArgumentParser(description='Simple Todo list manager written in Python')
    parser.add_argument('-m', '--mark-complete', type=int, nargs='+')
    parser.add_argument('-a', '--add-task', type=str)

    args = parser.parse_args()

    # Retrieve the todo list
    tasks = read_todo(path)

    if args.add_task:
        tasks.append(args.add_task)

        write_todo(tasks, path)
    elif args.mark_complete:

        for index in sorted(args.mark_complete, reverse=True):
            print('Marking task "%s" as complete' % tasks[index])
            del(tasks[index])

        write_todo(tasks, path)

    # Always print the tasks at the end of an operation
    for id, data in enumerate(tasks):
        print('[%d] %s' % (id, data))
