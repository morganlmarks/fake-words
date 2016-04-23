import random


class WordGenerator(object):

    def __init__(self, filename):
        self.filename = filename
        self.letter_transitions = {}
        self.letter_counts = {}
        self.transitions_probabilities = {}

    def process_words(self, verbose=True):
        word_count = 0
        with open(self.filename, 'rU') as f:
            for line in f:
                word_count += 1
                word = line.strip()
                prev = ' '
                for char in word:
                    self._record_transition(prev, char)
                    prev = char
                self._record_transition(prev, ' ')
                if verbose:
                    if word_count % 1000 == 0:
                        print "On word #{}: {}".format(word_count, word)
        if verbose:
            print "Finished processing {} words.".format(word_count)
        print "Building probabilities..."
        self.build_probabilities()

    def _record_transition(self, char, next):
        if self.letter_transitions.has_key(char):
            self.letter_transitions[char][next] = self.letter_transitions[char].get(next, 0) + 1
        else:
            self.letter_transitions[char] = {next: 1}
        self.letter_counts[char] = self.letter_counts.get(char, 0) + 1

    def build_probabilities(self):
        for letter, next_letters in self.letter_transitions.iteritems():
            self.transitions_probabilities[letter] = []
            x = 0
            for next_letter, count in next_letters.iteritems():
                x += count
                self.transitions_probabilities[letter].append((next_letter, x))

    def _get_next(self, letter):
        total = self.letter_counts.get(letter)
        rand = random.randint(1, total)
        prev_number = 0
        for next, number in self.transitions_probabilities[letter]:
            if prev_number < rand <= number:
                return next
            prev_number = number
        print 'Could not find next letter )='
        return ''

    def generate_word(self, verbose=True):
        word = ''
        letter = None
        while letter != ' ':
            if not letter:
                letter = ' '
            next = self._get_next(letter)
            word += next
            letter = next

        print word

    def generate_words(self, num):
        for i in range(num):
            self.generate_word()