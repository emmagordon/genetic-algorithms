#!/usr/bin/env python2.7

import sys

from character_set import AsciiCharacterSet, CharacterSet


class SegmentationFault(Exception):
    pass


class InvalidBrainfuck(Exception):
    pass


class TuringMachine(object):
    def __init__(self, tape_length=30000, cell_size=256):
        self.tape_length = tape_length
        self.tape = [0] * tape_length
        self.pointer = 0
        self.cell_size = cell_size

    def move_pointer_forwards(self):
        self.pointer += 1
        if self.pointer >= self.tape_length:
            raise SegmentationFault

    def move_pointer_backwards(self):
        self.pointer -= 1
        if self.pointer < 0:
            raise SegmentationFault

    def get_value_at_pointer(self):
        return self.tape[self.pointer]

    def set_value_at_pointer(self, value):
        self.tape[self.pointer] = value % self.cell_size

    def increment_value_at_pointer(self):
        self.set_value_at_pointer(self.get_value_at_pointer() + 1)

    def decrement_value_at_pointer(self):
        self.set_value_at_pointer(self.get_value_at_pointer() - 1)


class BrainfuckInterpreter(TuringMachine):
    def __init__(self, program_string, character_set: CharacterSet):
        super(BrainfuckInterpreter, self).__init__()

        self.commands = {">": self.move_pointer_forwards,
                         "<": self.move_pointer_backwards,
                         "+": self.increment_value_at_pointer,
                         "-": self.decrement_value_at_pointer,
                         ".": self.output_value_at_pointer,
                         ",": self.input_value_at_pointer,
                         "[": self.while_value_at_pointer_is_non_zero,
                         "]": self.end_while}

        self.program_string = program_string
        self.program_position = 0

        # Generate mappings to lookup location of matching braces.
        self.find_opening_brace, self.find_closing_brace = self._find_braces()

        self.character_set = character_set
        self.cell_size = character_set.size

    def output_value_at_pointer(self):
        sys.stdout.write(self.character_set.get_char(self.get_value_at_pointer()))

    def input_value_at_pointer(self):
        while True:
            user_input = input("Enter a single character:")
            if len(user_input) == 1:
                self.set_value_at_pointer(self.character_set.get_value(user_input))
                break

    def while_value_at_pointer_is_non_zero(self):
        if self.get_value_at_pointer() == 0:
            self.program_position = self.find_closing_brace[self.program_position]

    def end_while(self):
        if self.get_value_at_pointer() != 0:
            self.program_position = self.find_opening_brace[self.program_position]

    def run(self):
        while True:
            try:
                instruction = self.program_string[self.program_position]
            except IndexError:
                break  # We've reached the end of the program.

            try:
                self.commands[instruction]()
            except KeyError:
                pass  # Brainfuck ignores characters not in its operator set.
            except SegmentationFault:
                break  # Treat this as a valid way to trigger program exit.

            self.program_position += 1

    def _find_braces(self):
        find_opening_brace = {}
        find_closing_brace = {}

        opening_braces = []
        for (position, character) in enumerate(self.program_string):
            if character == "[":
                opening_braces.append(position)

            elif character == "]":
                try:
                    opening_brace_position = opening_braces.pop()
                except IndexError:
                    raise InvalidBrainfuck  # No matching opening brace

                find_opening_brace[position] = opening_brace_position
                find_closing_brace[opening_brace_position] = position

        if len(opening_braces) != 0:
            raise InvalidBrainfuck  # Missing closing brace(s)

        return find_opening_brace, find_closing_brace


if __name__ == "__main__":
    bf_interpreter = BrainfuckInterpreter(program_string=sys.argv[1],
                                          character_set=AsciiCharacterSet())
    bf_interpreter.run()
