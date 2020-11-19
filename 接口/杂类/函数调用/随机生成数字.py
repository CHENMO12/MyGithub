import random

int = "".join(random.choice("0123456789") for i in range(16))

isinstance(int,str)



print(int)