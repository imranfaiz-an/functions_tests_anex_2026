import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt
    import polars as pl
    import numpy as np

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Writing Better Code Using **Functions** & **Tests**
    - Faizan Imran
    - Data Science Intern - __Modeling Team__ - Department of Finance (2026)
    - Current grad student at UChicago - majors: **Computer Science & Public Policy**

    ## Agenda:
    - What are functions?
        - Types of functions
            - Pure Functions
            - Impure Functions
    - Why write functions at all?
    - When to write functions?
    - Database Connection - Case Study
    - How functions facilitate testing
    - Unit Testing
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        Some of us might remember functions from Maths - they are formally defined as: _"A function from a set X to a set Y assigns to each element of X exactly one element of Y"_

        The same can logic can be applied to computer functions! A function can be thought of as a "reusable block of code that performs __a specific task__".

        It helps to think of functions as a machine that receives as input and processes that input in some predetermined way and returns some output.
        """
    ).callout(kind="info", title="What is a function?")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why Functions?
    Functions are a great way to streamline work as Data Scientists/Analysts/Engineers - writing functions allows us to name processes, avoid redundancies and work on our organizational/team specific code base incrementally.

    Some immediately useful features of writing code in functions are[^1][^2]:
    - __Modularity__: Functions help remove redundancies and improve efficiency by making code modular.
    - __Memory__: Function names are easy to remember and communicate. And the variable/objects defined inside of functions are not stored in memory aftear the function runs - saving computer memory!
    - __Maintainability__: Functions are easy to update; to make changes we would need to only update the code in one place. This makes our codebase much more easier to maintain and expand in the long run.
    - __Tests & Checks__: We can explicitly handle issues and edge cases when writing functions and they also make it much easier to write tests.

    [^1]: [Hadley Wickham - R for Data Science](https://r4ds.hadley.nz/functions.html)
    [^2]: [Why Write Functions?](https://www.pyopensci.org/lessons/write-better-code/optimize-code/about-python-functions.html)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(f"""
    ### Example 1: Let's Look at a Function

    For example the function below prints 😲 and takes an integer as as input that determines how many times the emoji is printed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    def print_astonished(n: int) -> str:
        """Function that prints an emoji n times"""
        return "#" + "😲" * n

    slider = mo.ui.slider(start=0, stop=25, label="##Astonishment Level:")
    return print_astonished, slider


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ```python
    def print_astonished(n :int) -> str:
        "\""Function that prints an emoji n times"\""
        return "#" + "😲" * n
    ```
    """)
    return


@app.cell
def _(slider):
    slider  # Play around with this slider to see how our function reacts to different input
    return


@app.cell(hide_code=True)
def _(mo, print_astonished, slider):
    mo.md(
        print_astonished(slider.value)
    )  # We are feeding the slider's current value to our print function!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Instead of having to manually type in the emojis repeatedely - I can just write a function that does that for me!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    print_tab = mo.md("""
    ```python
    print("Hello!")
    ```
    `print()` shows text on the screen.

    Fun fact: The _print()_ function doesn't actually *return* anything, so if we store it's output in an object it will just be `None`.
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

        df = pd.DataFrame()

        df.isna() # Detect missing values for an array-like object.

        df.unique() # Return unique values based on a hash table.

        df.pivot() # Return reshaped DataFrame organized by given index / column values.
        ```
        and many many more. These functions do task that most of us working with data need to do. Simply importing a library that has functions that perform tasks we need to do make our life much easier!
        ---
        ### Combining Functions into a Package
        Once we get comfortable with writing and managing our own functions we can also bundle them up in a package and publish them for others to use. My team at DOF did just that with the package [AssessNYC](https://github.com/nycdepartmentoffinance/assessNYC). This package contains a bunch of functions that helps our team do all sorts of modelling/EDA work and it also speaks to the value of investing in functions early in local government because our workflows require (for the most part) having a base set of utilities/tasks that the Data Scientists/Engineers work on to improve and expand on over time!
        """
         )
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## When to Write Functions
    A good rule of thumb to have when considering writing functions is to ask whether the piece of code that we have would need to copy/paste some lines of code while changing nothing or changing very little of the original structure.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Example 2:
    While at DOF our team was accessing data by connecting to a database and since the database connection was a central part of everyone's work almost all the scripts that everyone was writing had 8-10 lines of code that established the database connection.

    So I wrote a function that built the connection for them! Instead of manually writing 10 lines of code in every script this function allowed a single line access.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ```python
    def connect_db(db_name: str):
        "\""
        This function takes in the name of the database and establishes a connection
        with that database.

        Input:
        - db_name: (str) the name of the database to connect to

        Returns:
        - A pyodbc.Connection object which we can use to query our database
        "\""

        # the following line just loads in the .Renviron file that contains sensitive information
        # like passwords needed to connect to the database

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
        return pyodbc.connect(connection_string)
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Below is an example of code before the function was implemented - below we are establishing a connection to 2 different databases and it is obvious why this is such a strong case to implement a function!

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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    By adding this function one could get the connection the the database by just calling:

    ```python
    test_connection = connect_db("test")
    prod_connection = connect_db("test")
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Pending on Functions
    - Defining inputs & outputs
    - Functions should do one thing and do them well!
    - Functions should assume no existing state - the only thing that matters is the input to the function
    - Other examples of cases to write functions for - add charts!
    - Why a function for do_analysis() is not scaleable!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Testing

    - Go over what testing is - while building on the database connection example
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### In-Code Exception Handling
    Writing functions in such a way does not just reduce redundancies it also helps consolidate processes and a well written function can catch an input errors upfront. And adding useful `try` `except` statements in our function we can easily avoid some expected mistakes.

    Going back to the earlier example if I know that we only have 3 available databases namely **test, prod, & staging** I can add this to my code:

    ```python
    try:
        if db_name not in ["test", "prod", "staging"]:
            raise ValueError(
                f"{db_name} is not a valid database that our team has access to!"
                "Try one of the following: 'test', 'staging', 'prod'"
            )
    ```

    This update would make our function look like this:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ```python
    def connect_db(db_name: str = "test"):
        "\""
        This function takes in the name of the database and establishes a connection
        with that database.

        Input:
        - db_name: (str) the name of the database to connect to

        Returns:
        - A pyodbc.Connection object which we can use to query our database
        "\""

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
        connection_string = "\".join(connection_args)
        return pyodbc.connect(connection_string)
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Building functions in such a way makes sure that the same processes are being followed by everyone on the team and it also allows us to raise try/except errors that are useful - this comes in super handy for code that interactes with the database since the errors one encounters there are often not helpful.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Unit Testing
    - Go over simple unit testing here using pytest - keep it super simple - within 5 minutes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summarizing & Final Thoughts
    """)
    return


if __name__ == "__main__":
    app.run()
