# Function Definition Compiler — Parser Test Plan

## Purpose

Use these cases to check whether the parser accepts valid source programs and rejects malformed syntax.

**Important:** The expected results below are not a record of executed tests. Run each test with the current `parser.py` and replace the actual-result column with the observed output. Parser behavior can differ if the lexer/parser in the repository has changed.

## Test cases

| ID | Category | Input | Expected result | Actual result |
|---|---|---|---|---|
| T01 | Valid function | `def add(a, b): return a + b;` | Accept | Not run |
| T02 | Empty parameter list | `def main(): return 0;` | Accept | Not run |
| T03 | Valid call | `add(2, 3);` | Accept | Not run |
| T04 | Valid arithmetic precedence | `def calc(a, b): return a + b * 2;` | Accept | Not run |
| T05 | Missing closing parenthesis | `def add(a, b: return a + b;` | Reject | Not run |
| T06 | Missing colon | `def add(a, b) return a + b;` | Reject | Not run |
| T07 | Missing comma | `def add(a b): return a + b;` | Reject | Not run |
| T08 | Trailing parameter comma | `def add(a,): return a;` | Reject | Not run |
| T09 | Missing return semicolon | `def add(a): return a` | Reject | Not run |
| T10 | Missing call argument | `add(2,);` | Reject | Not run |
| T11 | Missing call closing parenthesis | `add(2, 3;` | Reject | Not run |
| T12 | Incomplete expression | `def add(a): return a + ;` | Reject | Not run |
| T13 | Unclosed expression parenthesis | `def add(a): return (a + 2;` | Reject | Not run |

## How to execute tests

1. Run the parser using the command documented in the project's README (for example, `python parser.py` or `py parser.py`).
2. Enter one test input in the exact input format expected by the program.
3. Record the output exactly as displayed.
4. Mark a case as passed only if the observed result matches the expected result.
5. Capture terminal screenshots for at least one valid and two invalid cases.

If the parser reads until an `END` marker, include `END` after the source program as required by that implementation. Do not include `END` as part of the language grammar unless the lexer/parser explicitly treats it as a source-language token.

## Suggested report format

For each test, record:
- Test ID
- Source input
- Expected result
- Actual result
- Pass/Fail
- Error message or screenshot filename

## Example report entry (fill in after running)

```text
Test ID: T05
Input: def add(a, b: return a + b;
Expected: Reject
Actual: [paste actual output]
Pass/Fail: [fill after comparing]
```
