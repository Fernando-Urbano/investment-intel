# investment-intel-br

# d3.js
A library for manipulating documents based on data.

Allows to automatically render and rerender HTML.

After we reference the d3 in our links script, we start to manipulate the objec `d3` inside of the js code:

```
d3.select('div');
```

It uses `select` to select the div which will be used to add a data.

```
d3.select('div')
    .selectAll('p');
```

Now, inside of the div, we select all paragraphs.

If there are no paragraphs inside of the div, that is not a problem.

```
d3.select('div')
    .selectAll('p')
    .data([1, 2, 3]);
```

Finally, we put data inside of the elements selected. In this case, in each of the paragraphs.

```
d3.select('div')
    .selectAll('p')
    .data([1, 2, 3])
    .enter();
```

The method enter than is used to binds the data to the object.

```
d3.select('div')
    .selectAll('p')
    .data([1, 2, 3])
    .enter()
    .append('p');
```

The append actually creates the paragraphs if it does exist.

```
d3.select('div')
    .selectAll('p')
    .data([1, 2, 3])
    .enter()
    .append('p')
    .text(dta => dta);
```

Finally, we add a text to each of the paragraphs. We can do that with plain HTML or using a function.