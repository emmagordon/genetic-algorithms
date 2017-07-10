class CharacterSet(object):
    def __init__(self):
        self.size = 0
        self.char_to_value = {}
        self.value_to_char = {}

    def get_value(self, character):
        return self.char_to_value[character]

    def get_char(self, value):
        return self.value_to_char[value]


class CharacterSetFromString(CharacterSet):
    def __init__(self, character_set_string):
        super(CharacterSetFromString, self).__init__()
        self.size = len(character_set_string)
        character_values = enumerate(character_set_string)
        self.char_to_value = {char: val for val, char in character_values}
        self.value_to_char = {val: char for val, char in character_values}


class AsciiCharacterSet(CharacterSet):
    def __init__(self):
        super(AsciiCharacterSet, self).__init__()
        self.size = 256
        self.char_to_value = {chr(val): val for val in xrange(self.size)}
        self.value_to_char = {val: chr(val) for val in xrange(self.size)}
