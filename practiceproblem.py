import names
counter = 0
with open('words','r') as f:
    for word in f:
        
        if len(word.strip('\n')) == 25:
            counter += 1
            
            if counter == 10:
                    print(word)

        


