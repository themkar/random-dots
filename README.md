# Random Dot Patterns

## Creating Patterns
A template for how to create a patterns object can be found in ```my_patterns.py```.

To generate some random dots with the default settings:
```bash
python randomdots.py
```

## Loading Patterns
To load some random dots from a file:
```bash
python randomdots.py my_file.pkl
```

## Documentation
To understand how the code works, I have included highly descriptive comments in [```randomdots.py```](https://github.com/oliviaguest/random-dots/blob/master/randomdots.py).
Also running the following will return the docstring for creating, initialising, saving, etc., a random dot pattern:
```python
import randomdots
help(randomdots)
```

## 286_random_dots directory
```my_randomdots286.py```,```randomdots.py``` : generating 286 random dots, which fall into 18 categories
```my_randomdots286_ver2.py```,```randomdots_ver2.py``` : generating 286 random dots patterns falling in 18 categories and with each item distorted from the prototype based on its prototypicality judgement


