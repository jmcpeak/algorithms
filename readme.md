# Learning algorithms! <!-- omit in toc -->

## About coding style
In my code you will see the way I declare lot of helper functions. The top level function usually does nothing but returns dictionary with bunch of function. (I wish there was dot ooperator to access values of dictionary but it is what it is.) The primary reason for this is that I don't like globals, even within function, that any other function can modify within. Therefore the top level function there creates a closure enviroment and the inner functions are just an API to mutate this closed environment. This is my style but you can do it without such helper functions. 

## [Breadth First Search](./1.bfs/readme.md)

## [Depth First Search](./2.dfs/readme.md)
- Topological Sort
