from collections import deque

conversation_history = deque(maxlen=5)

list1= [1,2,3,4,5, 6, 7, 8, 9, 10]

for i in list1:
    conversation_history.append(i)
    print(conversation_history)

print(conversation_history)