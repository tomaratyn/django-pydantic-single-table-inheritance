# Creating type safe extensions without using multitable inheritance.

## Problem

I have encountered a case where I needed to store a variety of types in a single table. All the types have a common 
base type, but some will have additional attributes that need to be stored. Different types can have different 
attributes.

## Solution

This repo contains a few solutions:

- `multitable` - A solution that uses multitable inheritance.
- `onetable_with_pydantic` - A solution that uses a single table with pydantic models to validate the data.



