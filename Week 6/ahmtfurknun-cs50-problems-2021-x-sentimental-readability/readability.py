text = input("Text: ")

letter = sentence = 0
word = 1

for i in range(len(text)):
    if text[i].isalpha():
        letter += 1
        
    elif text[i] == " " and text[i+1] != " ":
        word += 1
        
    elif text[i] == "." or text[i] == "?" or text[i] == "!":
        sentence += 1
        
L = 100 * float(letter) / word
S = 100 * float(sentence) / word
index = 0.0588 * L - 0.296 * S - 15.8

if index < 1:
    print("Before Grade 1")
    
elif index >= 16:
    print("Grade 16+")

else:
    print("Grade", round(index))