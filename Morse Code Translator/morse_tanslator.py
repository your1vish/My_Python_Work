from MORSE import MORSE_DATA

entry = input("Enter the text:\n").upper()

en_split = entry.split(" ")
en_split_2 = [list(word) for word in en_split]

sentence_list = []

for word in en_split_2:
    word_list = []
    for character in word:
        if character in MORSE_DATA:
            word_list.append(MORSE_DATA[character])
    sentence_list.append(word_list)

sentence = [" ".join(words) for words in sentence_list]
sentence_ ="  ".join(sentence)

print(sentence_)