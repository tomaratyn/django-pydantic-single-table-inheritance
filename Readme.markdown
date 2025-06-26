# Creating type safe extensions without using multitable inheritance.

## Problem

I have encountered a case where I needed to store a variety of types in a single table. All the types have a common base type,
but some will have additional attributes that need to be stored. Different types will have different attributes.

