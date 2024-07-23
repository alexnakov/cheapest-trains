def number_generator(limit):
    number = 0
    while number < limit:
        yield number
        number += 1

# Create a generator object
gen = number_generator(5)


print(list(gen))
# Iterate over the generator
for value in gen:
    print(value)
