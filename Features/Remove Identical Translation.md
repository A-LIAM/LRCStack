# Problem
Sometimes a translation line end up identical to the main line as result of the song being multilingual. for example in some Japanese song the singer sing multiple lines in English. so the English and Romanized Japanese translation lines end up identical.

# Objective
Remove lines repeated lines with identical timestamps. It should also be compatible with `--enclose` argument. it should detect repeated line even if the line is enclosed by parenthesis.

# Usage
`-i` or `--remove-identical`
