#! /usr/bin/python3m

"""
Simple Todolist manager for the command line that allows you to view, add or mark tasks as complete
Author: Michael Aquilina 2014
"""

import re
import os

from collections import defaultdict

# TODO: Cleanup code
#       Convert to class
#       Add color terminal support
#       Better Error Handling
#       Allow deleting and inserting at 'all' selection


def show_todo_list(task_list, sections):

    def show_section(section):
        for index, task in enumerate(task_list.get(section, [])):
            print('[%d] %s' % (index, task))

    # Always display default first and don't show a heading
    if 'default' in sections:
        show_section('default')

    # Follow the order specified in the command line
    for section in sections:
        if section != 'default':
            print('> %s' % section)
            show_section(section)


def write_todo(task_list, file_path):
    """
    Writes a todolist formatted dictionary to file for reading at a later stage.
    task_list dictionaries passed should contain lists of todo items organised by their
    section name.
    """

    with open(file_path, 'w') as f:

        # Always write the default list on the top
        for task in task_list['default']:
            f.write('* %s\n' % task)

        # Grab the list of all other sections
        others = task_list.keys()
        for section in others:
            if section != 'default' and len(task_list[section]) > 0:
                f.write('\n')
                f.write('>%s\n' % section)
                for task in task_list[section]:
                    f.write('* %s\n' % task)


def read_todo(file_path):
    """
    Returns a dictionary of lists organised by their section. A 'default'
    section is always available in the dictionary but does not guarantee the
    list to have any contents
    """

    task_list = defaultdict(list)
    if not os.path.exists(file_path):
        return task_list

    # Read all data at one go for speed
    with open(file_path, 'r') as f:
        buffer = f.readlines()

    current_section = 'default'
    for line in buffer:
        if line.startswith('>'):
            # Clean up section names
            current_section = line[1:]
            current_section = current_section.strip()
            current_section = current_section.lower()

            task_list[current_section] = []
        else:
            # Attempt to match
            m = re.match(r'\* (?P<data>.*)', line)
            if m:
                task_data = m.group('data')
                task_list[current_section].append(task_data)

    return task_list


def main(args):
    # Begin Processing Here
    tasks = read_todo(todo_path)

    # If all specified then show all sections except completed
    if 'all' in args.sections:
        sections = set(tasks.keys()) - {'completed'}
    else:
        sections = args.sections

    if args.edit:
        import subprocess
        editor = os.environ.get('EDITOR', 'vim')
        subprocess.call([editor, todo_path])
        return

    if args.list:
        print(' '.join(tasks.keys()))
        return

    # Command Line Options
    if args.mark_complete:
        if len(sections) > 1:
            print('ERROR: Cannot mark task when specifying multiple sections')
        else:
            task_section = tasks[sections[0]]

            for index in args.mark_complete:
                if index < len(task_section):
                    target = task_section[index]
                    print('NOTE: Marked "%s" as complete' % target)
                    tasks['completed'].append(task_section[index])
                    task_section[index] = None
                else:
                    print('ERROR: Invalid Index specified for "%s"' % sections[0])

            tasks[sections[0]] = [task for task in task_section if task is not None]
            write_todo(tasks, todo_path)
    elif args.add_task:
        if len(sections) > 1:
            print('ERROR: Cannot add task when specifying multiple sections')
        else:
            task_section = tasks[sections[0]]
            task_section.append(' '.join(args.add_task))

            write_todo(tasks, todo_path)
    elif args.delete:
        if 'all' in args.sections:
            print('ERROR: Cannot delete all!')
        else:
            print('Deleted sections: %s' % sections)

            for i in range(len(sections)):
                del tasks[sections[i]]

            write_todo(tasks, todo_path)
            sections = ['default']

    print('Available: %s' % sorted(list(tasks.keys())))
    show_todo_list(tasks, sections)


if __name__ == '__main__':
    import argparse

    todo_path = os.path.expanduser('~/todo.md')

    parser = argparse.ArgumentParser(description='Simple Todo list manager written in Python')
    parser.add_argument('sections', default=['default'], nargs='*')
    parser.add_argument('-m', '--mark-complete', type=int, nargs='+', help='Marks a specified task as complete')
    parser.add_argument('-a', '--add-task', type=str, nargs='+', help='Adds a task to a todo list')
    parser.add_argument('-d', '--delete', action='store_true', help='Deletes the section specified')
    parser.add_argument('-l', '--list', action='store_true', help='List available sections')
    parser.add_argument('-e', '--edit', action='store_true', help='Edit the todo list with your default editor')

    main(parser.parse_args())
