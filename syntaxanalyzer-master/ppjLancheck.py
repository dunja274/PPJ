import pickle as serializer

with open('enka_states.txt', 'rb') as f:
    enka_states: set = serializer.load(f)

#print(enka_states)

# for k in enka_states:
#     print(k)
print(enka_states[0])