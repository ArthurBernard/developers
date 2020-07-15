# Arthur Bernard answeres

## 1. How to get indices of N maximum values in a NumPy array?

```python
>>> np.argsort(_array)[-n:]
```

## 2. Mention the use of // operator in Python?

n // i is equivalent to int(n / i)

## 3. What is the difference between a list and a tuple?

A list is mutable (hash method not allowed) and a tuple is immutable (hash method allowed).

## 4. What would be the output of the following?

### 1

```python
a = [1,2,3]
b = a
c = [1,2,3]

-- 1
>>> print(a == b)
True
>>> print(a == c)
True

-- 2
>>> print(a is b)
True
>>> print(a is c)
False
```

### 2 Looking at the below code, write down the final values of A0, A1, ...An.

```python
A0 = dict(zip(('a','b','c','d','e'),(1,2,3,4,5))) # => {'a': 1, ..., 'e': 5}
A1 = range(10)                                    # => [0, ..., 9]
A2 = sorted([i for i in A1 if i in A0])           # => []
A3 = sorted([A0[s] for s in A0])                  # => [1, ..., 5]
A4 = [i for i in A1 if i in A3]                   # => []
A5 = {i:i*i for i in A1}                          # => {0: 0, ..., 9: 81}
A6 = [[i,i*i] for i in A1]                        # => [[0, 0], ..., [9, 81]]
```

If you don't know what zip is don't stress out. No sane employer will expect you to memorize the standard library. Here is the output of help(zip).

zip(...)
zip(seq1 [, seq2 [...]]) -> [(seq1[0], seq2[0] ...), (...)]

Return a list of tuples, where each tuple contains the i-th element
from each of the argument sequences. The returned list is truncated
in length to the length of the shortest argument sequence.
If that doesn't make sense then take a few minutes to figure it out however you choose to.

## 5. Define a class named car with 2 attributes, “color” and “speed”. Then create an instance and return speed.

```python
>>> class Car:
>>>     def __init__(self, color, speed):
>>>         self.color = color
>>>         self.speed = speed if color != red else speed * 2
>>>
>>>     def __repr__(self):
>>>         return 'The car drive at {:.2f} km/h'.format(self.speed)
>>>
>>> mycar = Car('red', 30)
>>> mycar
The car drive at 30 km/h
```

## 6. Write a regular expression that will accept an email id. Use the re module.

```python
>>> import re
>>>
>>> _input = ""
>>> while re.search('^[a-zA-Z0-9_.]+[@][a-z.]+$'):  # or something like that
>>>     _input = input('Enter an email address')
```

## 7. If you have to choose between a list, set, and a dictionary to store 10 million integers, what will you use? Bear in mind that you would later like to query the frequency of a number within the dataset.

I will not recommend to use a set because it will drop every duplicate elements. If you don't need ordered data, then you should use a dictionary such that the integer is stored as the key and the frequency of this integer is stored as the value. Otherwise you should use a list.

