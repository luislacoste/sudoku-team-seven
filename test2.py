def func1(avr):
  avr.append(1)
  return True

def func2():
  avr = []
  func1(avr)
  print(avr)

func2()

