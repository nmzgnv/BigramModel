import random
import re

sentence = 'fish two fish two fish tree fish red fish blue fish red fish red fish two fish red fish red yellow red red red green'
sentence = input('Input your sentence: ')

words = sentence.replace('.', '').replace(',', '').split(' ')
markov_model = dict()
model_dimension = 2

markov_model[tuple(['*START*', words[0]])] = {words[model_dimension - 1]: 1}

for i in range(len(words) - model_dimension):
    window = tuple(words[i: i + model_dimension])
    next_word = words[i + model_dimension]
    if window in markov_model.keys():
        if next_word in markov_model[window].keys():
            markov_model[window][next_word] += 1
        else:
            markov_model[window][next_word] = 1
    else:
        markov_model[window] = {next_word: 1}

markov_model[tuple(words[-2:])] = {'*END*': 1}


def generate_start_words(markov_model):
    return random.choice(list(markov_model.keys()))


def generate_sentence(length, markov_model):
    start_words = generate_start_words(markov_model)
    sentence = list(start_words)
    for j in range(length):
        if not start_words in markov_model.keys():
            break
        word_frequency = markov_model[start_words]
        frequency_sum = 0
        for word, frequency in word_frequency.items():
            frequency_sum += frequency
        random_float = random.random()
        previous_probability = 0
        for word, frequency in word_frequency.items():
            current_probability = frequency / frequency_sum
            if previous_probability <= random_float <= previous_probability + current_probability:
                generated_word = word
                break
            previous_probability = current_probability
        start_words = tuple([start_words[1], generated_word])
        sentence.append(generated_word)
    if '*START*' in sentence:
        sentence = sentence[1:]
    if '*END*' in sentence:
        sentence = sentence[:-1]
    sentence[0] = sentence[0].capitalize()
    return ' '.join(sentence) + '. '


print(generate_sentence(len(words), markov_model))
