# Advent of Code 2019
https://adventofcode.com/2019

This repo contains the Python code I used to solve the puzzles.

## Lessons learned

### Day 1
This was a nice introduction to Advent of Code, which I hadn't
heard of before. Part one was over quickly, part two had me
scratching my head a bit at the recursion part but it didn't
take too long.

### Day 2
I liked this one. Using a high level programming language to 
emulate a much simpler computer than I'm currently working on. 
I'm not sure why I like it. Reminds me of the time I learned Java
by making a calculator based on the Reverse Polish Notation.

Anyway, I was confronted again with the common pitfall of mutating
my base lists in a loop. Remember kids: _Python is pass by object
reference_! I also had to look up how to break out of a double 
for-loop in one go. Turns out that's easy but not trivial, but
maybe the double for-loop isn't very pythonic to begin with anyway.

### Day 3
Wow. I think I've spent an entire morning on this one, trying
to model the grid using 2d NumPy arrays. Part one was already
a struggle with the slicing syntax (I always forget how that's
supposed to work), the array dtype, and even memory errors on 
calculating the actual puzzle. Part two then required something
that I couldn't even handle with my model, so it took me even 
more time to figure out how to add numbers to every step. But
in the end, it worked.

And of course, once I finished it and rested my mind for a couple
of minutes, I had a much better idea. I could've just modeled 
the paths as lists of tuples of x,y coordinates for every single
step. Then:

- the intersections are simply the tuples appearing in both lists
- the Manhattan distance is simply `x+y`
- the path length to the intersection is simply the index of the
intersection tuple in its list

So: _take the time to think about your model_.

### Day 4
This was an interesting one. The first part was rather easy, 
especially when I came across using `np.diff()` to check for
any adjacent groups. Then part 2 had me reeling. The brute force
solution isn't very elegant, but it has early returns so it could
have been far worse I guess :')

It's very useful to test using simple assertions after defining your
methods, they get executed every time you run the module. Saves
you the hassle of an entire unit testing framework.

### Day 5
The intcode computer returns! And had me struggling. It wasn't until
I decided to convert all given test cases into separate unit tests 
that I would start to see the errors. The powers of unit testing
are displayed once again!

- I forgot to increment the offset in case of 'no jump', causing 
an infinite loop (which also led me to implement a simple but sane
'max number of iterations before halting' parameter)
- I forgot to use the parameter mode with opcode 4 (giving output)

### Day 6
I don't work with graphs often, but it was plain to see this was a
graph problem, so out came the `networkx` documentation. I even used
a directed graph first, until I realised in part 2 that I actually
didn't need that. Problem took me less than an hour which is less
than all other days so far :')

### Day 7
Intcoding again! Before tackling the problem I decided to implement
the IntcodeProgram as a formal class, as I expected it to return 
for a lot more days in this advent. Part 1 then was easily done; 
I could just reuse the same instance over and over again. After
re-learning the difference between combinations and permutations 
the answer rolled out quickly.

Then part 2 came and I had to redesign the interface of my fancy
new class. Separate functions for starting and receiving input, 
using a ProgramState `Enum`, and other fancy things. Sure, the
code could still be refactored to be more elegant, but I'm pretty
satisfied, and with the new design the solution to part 2 just 
instantly worked!

### Day 8
In my mind this puzzle quickly became a 3d NumPy **mess**. Then I
remembered an earlier lesson, so I simply sliced up the string to
layers and parsing each layer. Then printing to a monospaced
terminal works pretty nicely. Not too hard this one.

### Day 9
I've been reading parts of the book Clean Code and decided to do
some refactoring on the intcode computer first. By introducing
proper enums I could remove now-redundant comments and unnecessary
custom exception raising. The unit testing suite still saved me in
the debugging process, as I had first wrongly implemented the 
'getting parameters in relative mode' method. Luckily part 2 was
as simple as changing an input.

When the next challenge for my intcode computer arrives, I'll 
refactor to use a mapping dict for the opcode handling.

### Day 10
This one was a nice challenge again. I quickly figured to use
linear functions to determine if two asteroids are on the same
line, but of course that ran into problems with vertical lines
and with direction. Still wasn't too hard. Then part 2 forced me
to abandon my initial approach and resort to calculating angles
and looping through these. The toughest part was figuring out
how to transform the coordinate system to start at 'up' which is
the negative y-axis. After that, smooth sailing.

### Day 11
Started off with the promised refactoring for the intcode computer
again relying heavily on my existing test suite. Cannot stress
the importance of testing enough! Thing back on day 3, I decided
to forgo NumPy and model using a simple list of pane objects. 
This got through part 1 relatively quickly but had me figuring
out how to transpose the coordinate system for printing to grid
properly. 

### Day 12
Wow. I used to be a physicist, so this should be easy, right?
Well part 1 was, definitely. Then part 2 stumped me. First time
I went to the official subreddit for help. With the explanation
provided there it went from troublesome to trivial. But darn...

### Day 13
Arcade gaming! Brilliant. Part 1 was a breeze; I printed the game
but that wasn't even necessary. Part 2 had me look into Python's
`curses` library to make it an interactive game, which actually
worked! Then the problem arose: I couldn't beat the game by hand
:')  as I visited the subreddit the first suggestion popping up
there was to make an auto player... easy enough. And fun to watch!
