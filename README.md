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

It's very useful test using simple assertions after defining your
methods, they get executed every time you run the module. Saves
you the hassle of an entire unit testing framework.