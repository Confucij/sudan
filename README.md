# sudan
C call graph visualizer with stack sizes

# Basic usage

* code should be compiled with `-fdump-rtl-expand -fstack-usage`. This will generate `.expand` and `.su` file for each object file in project
* all `.su` and `.expand` files should be combined in one file each respectively;
* run `egupt` on `.expand` file:
```
egypt COMBINED.expand > COMBINED.egypt
```
* And finally run `sudan`:
```
python3 sudan.py --su COMBINED.su --exp COMBINED.egypt -d 30 -e stop_function_name -f function_to_analyze | dot -Tpdf -o output.pdf
```
arguments are:
--su - combined su file
--exp - combined egypt file
-e - stop function. Analyzer would not go inside this function
-d - 
