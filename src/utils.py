# AUTONA - UI automation server (Python 3)
# Copyright (C) 2021 Marco Alvarado
# Visit http://qaware.org



class Integer:

  def __init__(self, value):
    self.value = value

  def __repr__(self):
    return str(self.value)

  def __add__(self, value):
    self.value += value
    return self