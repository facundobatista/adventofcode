# Advent of Code

Solutions (and all attempts to get to the solutions) for the Advent of Code exercises.

What is Advent of Code? I wouldn't say it better than Eric Wastl, the author, in the site's About:

> [Advent of Code](https://adventofcode.com/) is an Advent calendar of small programming puzzles for a variety of skill levels that can be solved in any programming language you like. People use them as interview prep, company training, university coursework, practice problems, a speed contest, or to challenge each other.


## What is inside this repo?

**Of course, all these are spoilers!**

These are all very dirty scripts, with a lot of prints, some of them possibly in Spanish. In some cases they don't even work ok (it's not that they all reach to the correct answer).

Always separated by day inside each year, normally it's just `proc1.py` and `proc2.py`, but you may find also `b` (or `c`, etc) versions of those files, for the cases where I just copied the script and continued in the copy for a very different approach. And maybe even other files with half attempts.

For the first years you just run the script in each directory. As years went by I made the final output more clear, but which one is the "final answer" may not be crystal clear in all cases.

For 2025 I formalized "a runner" that receives the file to run and `test`/`real` parameters, to avoid code duplication, and even separated a couple of helpers. The way to use the runner from this year is to get into the day's directory, and run it, for example:

```
.../adventofcode/2025/12$ ../run.py proc1.py test
```

You need to be inside a virtual environment with the requeriments specified in the corresponding file.


## What about unit testing?

Normally all this code is quick and dirty, hacked around until the proper response is given (which is validated in the site itself).

However, there are cases where a particular small function needs to be tested to be used safely and not have a silly mistake there.

There is support for that from 2025 onwards, you just pass `unit` to `run.py`. For an example where this is used, see `2025/01/proc2.py`.

```
../run.py proc2.py unit -v
```

(any extra parameters go to pytest)
