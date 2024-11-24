import random

def generateContactColor():
   """
    this function constructs an random RGB color when a contact is created
    which is used as contact background color

   Return: RGB color
   """
   
   r_Channel = random.randint(0, 255)
   g_Channel = random.randint(0,  255)
   b_Channel = random.randint(0, 255)
   randomColor = f"rgba({r_Channel}, {g_Channel}, {b_Channel})"
   return randomColor

