# Creating type safe extensions without using multitable inheritance.

## Problem

I have encountered a case where I needed to store a variety of types in a single table. All the types have a common 
base type, but some will have additional attributes that need to be stored. Different types can have different 
attributes.

## Solution

This repo contains a few solutions:

- `multitable` - A solution that uses multitable inheritance.
- `onetable_with_pydantic` - A solution that uses a single table with pydantic models to validate the data.

## Tradeoffs

### Multitable Inheritance

#### Pros

 - The default solution for Django / easy and understandable.
 - [`select_subclasses`](https://django-model-utils.readthedocs.io/en/latest/managers.html#inheritancemanager) works out of the box.

#### Cons

- Requires a separate table for each type.
- Can lead to a large number of tables if there are many types, each coupled to an integration.
- In a sense, less type safe as developers/operators might assume that all constraints are enforced by the database, 
but they are not.
- Requires a join to get the full object, which may or may not be an issue.

### Single Table with Pydantic

#### Pros

 - Only one table is needed.
 - Very type safe: All constraints are enforced by the Pydantic model.
 - No joins are needed to get the full object.

#### Cons

- Requires some custom code to handle the Pydantic models and subclassing.
- Not very django-like, as it does not use the ORM in the same way.
- Difficult to query inside the "bin" field.

