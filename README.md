# ATLAS
My contribution to the ATLAS v4 project, a categorisation of finite simple groups.

## About ATLAS v4
This is a digitisation of the [ATLAS of finite simple groups](https://en.wikipedia.org/wiki/ATLAS_of_Finite_Groups) written by Conway et al. written in 1985. There have been 3 previous digitisations, but the aim of this is twofold:

- Fix any previous errors in ATLAS v1-3 (which are now not regularly maintained)
- The backend is now json based, which makes other supplementary information eg generating Magma/GAP code far easier.

This has been part of a summer project I worked on with [David Craven](https://www.birmingham.ac.uk/staff/profiles/maths/craven-david), and any information in this repository is my own contribution (unless otherwise indicated).

## Using the programs
The program is designed to scrape a html program saved locally. Specifically, take one of the group pages on [ATLAS v3](http://atlas.math.rwth-aachen.de/) (it must have a conjugacy class table, if not the information can be generated seperately from Magma). Save this in a folder with your group name and running `class-scraper.py` (with appropriate touches as indicated on the comments at the top of the file) should generate the appropriate group.

There is also a program called `class_formula.py` that acts as a sanity check program - it works on the property that adding up each conjugacy class length yields the order of the group. 

## Acknowledgments
I would like to give credit to my friend [Reily](https://github.com/kraken05doo/) for helping me with some data storage issues - in particular relating to the use of the `Fraction` data type as seemingly the only data type that can work with division on very large numbers.
