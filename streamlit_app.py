import streamlit as st
from lexer import tokenize
from parser import parse_source
from semantic import analyze, SemanticError
from ast_tools import lines as ast_lines

st.set_page_config(page_title="Function Definition Compiler", page_icon="🧩", layout="wide")
st.title("Function Definition Compiler")
st.caption("Group 7 • Compiler Design Mini Project")
st.write("Enter a program using the supported function-definition syntax, then select **Run Compiler**.")

example = """def add(a, b): return a + b;
add(2, 3);"""

source = st.text_area("Source code", value=example, height=220,
                      help="Each function definition and function call must end with a semicolon.")
run = st.button("▶ Run Compiler", type="primary")

if run:
    if not source.strip():
        st.warning("Please enter a program first.")
    else:
        try:
            tokens = tokenize(source)
            program = parse_source(source)
            analyze(program)

            st.success("Compiler front end: SUCCESS")
            tab_tokens, tab_syntax, tab_semantic, tab_ast = st.tabs(
                ["Lexical Analysis", "Syntax Analysis", "Semantic Analysis", "AST"]
            )
            with tab_tokens:
                st.subheader("Generated tokens")
                st.dataframe(
                    [{"Type": kind, "Lexeme": value, "Line": line, "Column": col}
                     for kind, value, line, col in tokens],
                    use_container_width=True,
                    hide_index=True,
                )
            with tab_syntax:
                st.success("Syntax Analysis: SUCCESS")
                st.write("The source code follows the supported grammar.")
            with tab_semantic:
                st.success("Semantic Analysis: SUCCESS")
                st.write("No semantic errors were found.")
            with tab_ast:
                st.subheader("Abstract Syntax Tree (AST)")
                st.code("\n".join(ast_lines(program)), language="text")
        except (SyntaxError, SemanticError) as exc:
            st.error("Compiler front end: FAILED")
            st.code(str(exc), language="text")
            st.info("Correct the error in the source code and run the compiler again.")

with st.expander("Supported syntax and example"):
    st.code(example, language="python")
    st.write("This educational compiler checks tokens, grammar, and semantic rules. It does not execute the entered program or generate machine code.")
