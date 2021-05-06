![PyPI version badge](https://img.shields.io/pypi/v/streamfig)

# streamfig
Python class to generate describe stream graphs in fig format.

Documentation is in `doc/`, and some code examples are in `examples/`. The PNG output from all the examples is in `images/` . Below is the result from all the examples.

![Example of output of the streamfig package](./images/ex-ref-1.png)

## Get started 

First, write some python code:

```python
import streamfig

s = streamfig.StreamFig()
s.addNode("u")
s.addNode("v")
s.addLink("u", "v", 1, 3)
s.save("my_first_stream.fig")
```
Then, generate your image:

```zsh
python3 my_first_stream.py; fig2dev -Lpng my_first_stream.fig > my_first_stream.png
```
