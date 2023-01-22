import names

diff_names = []


def generate_diff_names():
    for i in range(5):
        name = names.get_full_name()
        diff_names.append(name) #creating list of names

generate_diff_names() #initial names list

while (len(set(diff_names)) != len(diff_names)): #making sure there are no duplicates
    generate_diff_names()

for j in range(5): #printing
    print(diff_names[j])
    print(len(diff_names[j]) - 1)
