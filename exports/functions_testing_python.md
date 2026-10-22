---
title: Functions Testing Python
marimo-version: 0.25.1
width: medium
layout_file: layouts/functions_testing_python.slides.json
css_file: css/custom.css
---

```python {.marimo hide_code="true"}
import marimo as mo
import pandas as pd
import altair as alt
import polars as pl
import numpy as np
app = mo.App(css_file="css.custom.css")
```

# Writing Better Code Using **Functions** & **Tests**
- Faizan Imran
- Data Science Intern - __Modeling Team__ - Department of Finance (2026)
- Current grad student at UChicago - majors: **Computer Science & Public Policy**

---
Shout out and thanks to Claire Boyd (Data Scientist @ DOF), James Turk (Assistant Clinical Professor @ UChicago) & Tara Sullivan (Director Data Science @ OTI) for their feedback on the material!
<!---->
## Agenda:
- What are functions?
    - Types of functions
- Why write functions at all?
- When to write functions?
- Database Connection - Case Study
- Good practices for writing functions
- How functions facilitate testing
- Try/Except in Python
- Unit Testing

```python {.marimo hide_code="true"}
mo.md(
    """
    "A function is a callable unit of some software logic that has a pre-defined behavior and can be invoked any number of times"[^1].

    It helps to think of functions as a machine that receives as input and processes that input in some predetermined way and returns some/expected output.

    [^1]: [Functions - Wiki](https://en.wikipedia.org/wiki/Function_(computer_programming))
    """
).callout(kind="info", title="What is a function?")
```

### Example: Let's Write a Function

For example the function below prints 😲 and takes an integer as as input that determines how many times the emoji is printed.

```python {.marimo hide_code="true"}
def print_astonished(n: int) -> str:
    """Function that prints an emoji n times"""
    return "#" + "😲" * n

slider = mo.ui.slider(start=0, stop=25, label="##Astonishment Level:")
```

```python
def print_astonished(n :int) -> str:
    """Function that prints an emoji n times"""
    return "#" + "😲" * n
```

```python {.marimo}
slider  # Play around with this slider to see how our function reacts to different input
```

Instead of having to manually type in the emojis repeatedely - I can just write a function that does that for me!

```python {.marimo hide_code="true"}
mo.md(
    print_astonished(slider.value)
)  # We are feeding the slider's current value to our print function!
```

## Types of Functions:
### Pure Functions:
Functions that for a given input return the same output everytime and have no side effects[^1].

Following is an example of a pure function:

```python
def add_list(numbers: [int]) -> int:
    '''Take a list of integers and return their sum'''
    total = 0 # total here is a Local Variable
    for i in numbers:
        total += i
    return total # ouput with same input will never change
```

### Impure Functions:
Functions that alter something outside of their scope or that have any side effects.

An example of impure function:

```python
count = 0 # count is a global variable

def increase_count():
    global count
    count += 1
    return count # will return a different value each time called
```

[^1]: A side effect is anything that has an observable effect other than its primary effect of reading the value of its arguments and returning a value. Side effects include: modification of non-local variables, doing I/O operations etc.

```python {.marimo hide_code="true"}
def add_list(numbers: list[int]) -> int:
    "Take a list of integers and return their sum"
    total = 0  # total here is a local variable
    for i in numbers:
        total += i
    return total  # same input -> same output, every time

numbers_input = mo.ui.text(value="1, 2, 3", label="Numbers (comma-separated):")
pure_function = mo.ui.button(label="Call add_list() again")
mo.hstack([numbers_input, pure_function])
```

```python {.marimo hide_code="true"}
pure_function  
_nums = [int(x) for x in numbers_input.value.split(",") if x.strip()]
mo.md(f"`add_list({_nums})` → **{add_list(_nums)}**")
```

```python {.marimo hide_code="true"}
count = 0  # count is a global variable

def increase_count():
    global count
    count += 1
    return count  # different value each time it's called

impure_function = mo.ui.button(label="Call increase_count()")
impure_function
```

```python {.marimo hide_code="true"}
impure_function
mo.md(f"`increase_count()` → **{increase_count()}**")
```

## Why Functions?
Functions are a great way to streamline work as Data Scientists/Analysts/Engineers - writing functions allows us to name processes, avoid redundancies and work on our organizational/team specific code base incrementally.

Some immediately useful features of writing code in functions are[^1][^2]:
- __Modularity__: Functions help remove redundancies in code and allow reuse of code
- __Decomposition__: We can break a complex task into more managable steps - where each function builds on the prior. This also allows different team members to work on a different part of the same problem in parallel
- __Memory__: Descriptive function names are easy to remember and communicate. And the variable/objects defined inside of functions are not stored in memory aftear the function runs - saving computer memory as well!
- __Maintainability__: Functions are easy to update; to make changes we would need to only update the code in one place. This makes our codebase much more easier to maintain and expand in the long run
- __Tests & Checks__: We can explicitly handle issues and edge cases when writing functions and they also make it much easier to write tests

[^1]: [Hadley Wickham - R for Data Science](https://r4ds.hadley.nz/functions.html)
[^2]: [Why Write Functions?](https://www.pyopensci.org/lessons/write-better-code/optimize-code/about-python-functions.html)

````python {.marimo hide_code="true"}
print_tab = mo.md("""
```python
print("Hello!")
```
`print()` shows text on the screen.

Fun fact: The _print()_ function doesn't actually *return* anything, so if we store it's output in an object it will just be `None`.
Print is also a very commonly used _impure_ function!
""")

sum_tab = mo.md(f"""
```python
sum([3, 1, 4, 1, 5])
```
`sum()` add things up.

**Returns:** `{sum([3, 1, 4, 1, 5])}`
""")

list_tab = mo.md(f"""
```python
list("hello")
```
`list()` turns things into a list. A word becomes a list of its letters!

**Returns:** `{list("hello")}`
""")

builtin_tabs = mo.ui.tabs({
    "print()": print_tab,
    "sum()": sum_tab,
    "list()": list_tab,
})

mo.vstack([
    mo.md("""
### Most of us already use functions all the time!

Both Python & R have tons of **built-in functions** that we use all the time.
On top of that, both languages give us access to **libraries/packages**, where
someone else already wrote a bunch of functions and published them for us to use!

Here are some common built-in functions in Python:
"""),
    builtin_tabs,
    mo.md("""
    ---
    When we install a library like Pandas and import it in our code it comes with a lot of functions that it's creators built for our use, for example:
    ```python
    import pandas as pd

    df = pd.DataFrame({"dept":["dof", "dot", "dcp"], "city": ["nyc", "nyc", "nyc"]})

    df.isna() # Detect missing values for an array-like object.
    df.head() # Return reshaped DataFrame organized by given index / column values.
    ```
    and many many more. These functions do task that most of us working with data need to do. Simply importing a library that has functions that perform tasks we need to do make our life much easier!
    """
     )
])
````

### Combining Functions into a Package
Once we get comfortable with writing and managing our own functions we can also bundle them up in a package and publish them for others to use. My team at DOF did just that with the package [AssessNYC](https://github.com/nycdepartmentoffinance/assessNYC). This package contains a bunch of functions that helps our team do all sorts of modelling/EDA work and it also speaks to the value of investing in functions early in local government because our workflows require (for the most part) having a base set of utilities/tasks that the Data Scientists/Engineers work on to improve and expand on over time!
<!---->
---
break - Questions?
---
<!---->
## When to Write Functions
A good rule of thumb to have when considering writing functions is to ask whether the piece of code that we have would need to copy/paste some lines of code while changing nothing or changing very little of the original structure.
<!---->
#### Code we used at DOF to connect to our databases
The code chunk below was how database connections were being made in almost all scripts - let's discuss why this is such a strong case to implement a function!

```python
db_name = "test"
load_dotenv(find_dotenv(f"C:/Users/{os.getlogin()}/.Renviron"))

connection_args = ["Driver={Oracle in OraClient19Home1};",
                   f"DBQ={os.environ[f'{db_name}_path']};",
                   f"DATABASE={os.environ[f'{db_name}_schema']};",
                   f"UID={os.environ[f'{db_name}_username']};",
                   f"PWD={os.environ[f'{db_name}_password']};",
                   "Trusted_Connection=no;",
                   "Port=1433"
]
connection_string = "\".join(connection_args)
connection = pyodbc.connect(connection_string)

db_name_prod = "production"

connection_args_production = ["Driver={Oracle in OraClient19Home1};",
                   f"DBQ={os.environ[f'{db_name_prod}_path']};",
                   f"DATABASE={os.environ[f'{db_name_prod}_schema']};",
                   f"UID={os.environ[f'{db_name_prod}_username']};",
                   f"PWD={os.environ[f'{db_name_prod}_password']};",
                   "Trusted_Connection=no;",
                   "Port=1433"
]
connection_string_prod = "\".join(connection_args_production)
connection_prod = pyodbc.connect(connection_string_prod)
```
<!---->
#### Functionalizing:

The function below achieves a lot of what we discussed above on the advantages of functionalizing code!
<!---->
```python
def connect_db(db_name: str):
    """
    This function takes in the name of the database and establishes a connection
    with that database.

    Input:
    - db_name: (str) the name of the database to connect to

    Returns:
    - A pyodbc.Connection object which we can use to query our database
    """

    load_dotenv(find_dotenv(f"C:/Users/{os.getlogin()}/.Renviron"))

    connection_args = ["Driver={Oracle in OraClient19Home1};",
                       f"DBQ={os.environ[f'{db_name}_path']};",
                       f"DATABASE={os.environ[f'{db_name}_schema']};",
                       f"UID={os.environ[f'{db_name}_username']};",
                       f"PWD={os.environ[f'{db_name}_password']};",
                       "Trusted_Connection=no;",
                       "Port=1433"
    ]
    connection_string = "".join(connection_args)

    return pyodbc.connect(connection_string)
```
<!---->
By adding this function one could get the connection the the databases by just calling:

```python
test_connection = connect_db("test")
prod_connection = connect_db("test")
```
<!---->
## Practices to Keep in Mind When Writing Functions
### Define the purpose of the function clearly

**Functions should ideally do one thing and do it well!** It does not really help to have a function that is doing many different things - at that point there really isn't an advantage of using functions over imperative programming.

For instance say we want to work on getting some analysis done for a new tax system being proposed on high value properties. One way to do this would be to just start writing code line by line and hope it works. What the functional approach would argue for is a clear breakdown of tasks.

For instance we could break this problem down by writing the following functions:

1- `get_high_valued_data()`

2- `clean_high_valued_data()`

3- `save_cleaned_data()`

This approach would allow one to divide and overcome any task that at first might feel daunting.

On the other hand writing a function for everything might not make a lot of sense either. From our example above a function like `analyze_high_valued_data()` might not work as well as the others because our goals/parameters for the analysis might keep changing. A function for analysis would not be as scalable as the rest!
<!---->
### Determining the input parameters to our function
Once we define broadly what our function needs to do that can also help determine what input parameters it should take to perform the task.

I like to use the bare minimum number of parameters that will get the job done. Adding more and more parameters can make the function confusing and that can also indicate the need to break the function down further.
<!---->
### Other things to keep in mind:
- **Use descriptive function names.** A function's name should say what it does, ideally starting with a verb (`clean_high_valued_data()` rather than `process()`). If you struggle to name a function, it may be doing too much.
- **Write docstrings.** A short docstring right below the definition should explain what the function does, what it takes in, and what it returns. This helps others, and future you, understand the code without reading every line.
- **Focus on writing pure functions at first.** Pure functions are easier to test, debug, and reuse because they don't depend on or change anything outside themselves.
- **Use default arguments (especially for optional parameters).** Defaults like `def get_high_valued_data(file_path: "your/file/path"):` let the function handle the common case without extra arguments, while still allowing changes when needed.
- **Keep functions short!** If a function no longer fits on one screen, it's probably doing more than one thing. Splitting it into smaller functions makes each piece easier to read and test.
- (optional) **Use type hints.** Type hints like ```def clean_high_valued_data(df: pd.DataFrame) -> pd.DataFrame:``` make inputs and outputs clear at a glance. Python doesn't enforce them, but they serve as built-in documentation.
<!---->
##break - Questions?
<!---->
## Testing & Exception Handling

Functions lend themselves well into the testing paradigm because functions have clearly designed input and output space and when we write functions we have a general idea about the kind of input our code inside the function expects. This is super helpful as it allows us to add some additional lines that can catch some errors that we might expect. And outside of the function we can use something called **Unit Testing** to make up some cases that make sure that the code is returning the output we expect!
<!---->
### In-Code Exception Handling

We can encounter errors when running codes even though the code we write has the correct syntax. Such errors are called **Exceptions** and many programming language allow us to handle these errors.

Let's look at an example where we use Try/Except:

```python
def add(a:int, b:int) -> int:
    '''add two numbers and return their sum'''
    return a + b
```

The function above takes two integers as inputs and returns an output and is syntactically correct but what if we provide it with an input that is a string and the other an int?

We get a `TypeError` which might throw someone new to Python and programming in general off. Adding exception handling allows us to add helpful error messages! We can add the following to the above:

#### `Try/Except`

`Try/Except` is used to notify the user when our program catches something but it does not cause the program to stop running
```python
def add(a:int, b:int) -> int:
    try:
        return a + b
    except TypeError:
        return f"Can't add a {type(a)} to {type(b)}"
```

This comes in super handy when working with messy data, connecting to APIs etc.

#### `raise`

We can instead also use `raise` in case we want to halt execution

```python
def add(a:int, b:int) -> int:
    if type(a) != type(b):
        raise TypeError(f"We cannot add {type(a)} to {type(b)}")
    return a + b
```

`raise` statements can be paired with `try` or used on their own.
<!---->
### Modifying connect_db`

```python
try:
    if db_name not in ["test", "prod", "staging"]:
        raise ValueError(
            f"{db_name} is not a valid database that our team has access to!"
            "Try one of the following: 'test', 'staging', 'prod'"
        )
```

It makes sense when connecting to a database to halt execution if the input is not correct!
<!---->
```python
def connect_db(db_name: str = "test"):
    """
    This function takes in the name of the database and establishes a connection
    with that database.

    Input:
    - db_name: (str) the name of the database to connect to

    Returns:
    - A pyodbc.Connection object which we can use to query our database
    """

    try:
        if db_name not in ["test", "prod", "staging"]:
            raise ValueError(
                f"{db_name} is not a valid database that our team has access to!"
                "Try one of the following: 'test', 'staging', 'prod'"
            )

    load_dotenv(find_dotenv(f"C:/Users/{os.getlogin()}/.Renviron"))

    connection_args = ["Driver={Oracle in OraClient19Home1};",
                       f"DBQ={os.environ[f'{db_name}_path']};",
                       f"DATABASE={os.environ[f'{db_name}_schema']};",
                       f"UID={os.environ[f'{db_name}_username']};",
                       f"PWD={os.environ[f'{db_name}_password']};",
                       "Trusted_Connection=no;",
                       "Port=1433"
    ]
    connection_string = "".join(connection_args)
    return pyodbc.connect(connection_string)
```
<!---->
Building functions in such a way makes sure that the same processes are being followed by everyone on the team and it also allows us to raise try/except errors that are useful - this comes in super handy for code that interactes with the database since the errors one encounters there are often not helpful.
<!---->
### Software Testing - Unit Testing

Software testing is used to answer one main question: _Does the code that we have written do what it is supposed to?_

We will be focusing on Unit Testing and discuss how having a few tests can go a long way in building trust in the code that we write.

Unit tests are easy to implement and understand and that makes them super accessible early on in our programming journey! Writing test early on also helps make sure that our programs keep working as things are added to them over time.

```python {.marimo}
def _add_list(numbers: list[int]) -> int:
    total = 0
    for i in numbers:
        total += i
    return total

def test_add_list():
    assert _add_list([1, 2, 3]) == 6
    assert _add_list([]) == 0          # edge case: empty list
    assert _add_list([-1, 1]) == 0     # edge case: negatives

test_add_list()
```

```python {.marimo}
# Python also comes with some packages that allow for testing
import pytest
def add(a, b):
    return a + b
```

```python {.marimo}
class TestBlock:
    @staticmethod
    def test_negatives():
        assert add(-2, -3) == -5, "This test fails"

    @staticmethod
    def test_one_zero():
        assert add(0, 4) == 4, "This test passes"

    @staticmethod
    def test_both_zero():
        assert add(0, 0) == 0, "This test passes"
```

## Summary & Final Thoughts
- Functions should do one thing and do it well
- Avoid copy/pasting code with minimal changes and consider writing a function instead
- Wrting good functions with a well-defined purpose and input sapce makes testing super convenient!
- Using functions, writing tests and having in-code exception handling makes the overall quality of our code much better and it also makes things easy to maintain in the long run
- Using these tools can also help someone new to your org understand what different components are doing and how everything works togther!
<!---->
---

## Thank you!
##Questions?

In case of other questions please feel free to email me at: imranfaiz@uchicago.edu

```python
def goodluck():
    return "happy coding"
```

---