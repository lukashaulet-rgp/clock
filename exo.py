def count_occcurences(s: str, char: str)⇾ int:
count = 0
for c in s :
    if c == char:
        count +=1
        return count
    
    count_occcurences("Bonjour", "o")