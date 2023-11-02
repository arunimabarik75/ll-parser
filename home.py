import streamlit as st
import pandas as pd
from process_input import process_user_input, print_dictionary
from left_recursion import removeLeftRecursion
from left_factoring import removeLeftFactoring
from first import computeAllFirsts
from follow import computeAllFollows
from parse_table import createParseTable
from parse_string import parsingUsingStack

print("---------------------------------------------------------------------")
st.set_page_config(layout="wide")

# Header
st.title("LL Parser Visualisation")
st.divider()
print("Loading Header....")

# Take user input
st.header("Grammar")
st.text("Starting Symbol")
start_symbol = st.text_input("Starting Symbol", label_visibility="collapsed")
st.text("Productions (Example: S -> aA | bcD)")
prods = st.text_area("Example", height=200, label_visibility="collapsed")
print("Input taken....")

# Process input
processed_input = process_user_input(prods)
print("Processed Input: ", processed_input)
print("Input processed....")

# Remove left recursion and left factoring
productions_1 = removeLeftRecursion(processed_input)
productions = removeLeftFactoring(productions_1)
print("Productions: ", productions)
print("Left recursion and factoring removed....")

# Find first and follow sets
first_set = computeAllFirsts(productions)
follow_set = computeAllFollows(start_symbol, productions)

terminals = list(first_set.keys())
first_list = [" , ".join(first_set[non_terminal]) for non_terminal in first_set]
follow_list = [" , ".join(follow_set[non_terminal]) for non_terminal in follow_set]

first_follow_df = pd.DataFrame(
    {"First": first_list, "Follow": follow_list}, index=pd.Series(terminals)
)
print("First and follow sets computed....")

# Parsing table
print("Parsing Table")

parse_table, ll_grammar, non_terminals = createParseTable(
    productions, first_set, follow_set
)

parsing_table_df = pd.DataFrame(parse_table, index=pd.Series(non_terminals))
print("Parsing table created....")

# ------------------------------------------------------------------------------

st.header("Left Recursion")
if st.button("Remove Left Recursion"):
    print = print_dictionary(productions_1)
    for line in print:
        st.text(line)

st.header("Left Factoring")
if st.button("Remove Left Factoring"):
    print = print_dictionary(productions)
    for line in print:
        st.text(line)

st.header("First Follow Set")
if st.button("Find First and Follow Sets"):
    st.table(first_follow_df)

st.header("Parsing Table")
if st.button("Generate Parsing Table"):
    st.table(parsing_table_df)
    if ll_grammar:
        st.text("Grammar is LL 1")
    else:
        st.text("Grammar is not LL 1")

# -------------------------------------------------------------------------------

# String tracing
st.header("Parse String")

st.text("String")
try:
    string = st.text_input("String", label_visibility="collapsed")
    print("Input string: ", string)
except:
    pass


if st.button("Parse String"):
    return_string, dataframe = parsingUsingStack(
        productions, parse_table, ll_grammar, string, start_symbol
    )

    st.text(return_string)
    if dataframe is not None:
        st.table(dataframe)

webpage_details = """
<h6> 
An LL parser, which stands for "Left-to-Right, Leftmost Derivation," is a type of top-down parsing technique used in computer science and compiler design to analyze and parse the structure of a context-free grammar. LL parsers are commonly employed in the process of transforming source code into an abstract syntax tree (AST) or other data structures, making them a crucial component in the development of compilers and interpreters for programming languages.
</h6>
"""

developer_details = """
<h6> Arunima Barik (20BCE016) </h6>
<h6> Gaurav Golchha (20BCE079) </h6>
"""

# Add a footer to your Streamlit app
st.sidebar.markdown(
    f"""
    <div style="background-color:#f4f4f4;padding:10px;border-top:1px solid #ccc;text-align:center;">
        <div style="display:flex;justify-content:space-between;">
            <div style="text-align:left; width: 49%;">
                {webpage_details}
            </div>
            <div style="text-align:right; width: 49%;">
                {developer_details}
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)