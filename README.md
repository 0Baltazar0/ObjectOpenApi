# ObjectOpenApi

Python wrapper for object oriented openapi manipulation

# Not Doing

## Resolving ambiguity

Structures like oneOf, anyOf,allOf are source of ambiguity, as their order of items is not determined

Example

> in a structure of [A,B,C] 'A' turns into the shape of 'B' -> you have to try and match [B,B,C] with [A,B,C], which B is matched with the other B.

## Webhooks

I am focusing on standard API definitions first, will be focused after achieving full coverage on those areas.
