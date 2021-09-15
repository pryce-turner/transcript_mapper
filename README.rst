Overview
--------

This is a simple and fairly naive mapping utility for converting transcript positions
to genomic positions. Functionality is split into 2 modules, a core utility and a CLI that calls it. The `mapper.py` module exposes
a Mapper class which loads the transcript definitions and exposes the translation utility. The `cmd_map.py` module 
uses Click to parse arguments, provide sensible defaults, and perform error-handling.
This project uses Poetry for dependency and venv management - the CLI can be invoked
with `poetry run map` after running `poetry install`. Tests can be run with `poetry run pytest tests`.

Considerations
--------------

In keeping with the spirit of the exercise, outside production tools were not consulted in
coming up with a solution. As such, a number of assumptions were made which may be vulnerable to edge-cases
if this were used on a more diverse dataset. However, a few key strengths should be highlighted:

1. The most expensive operation, making the mapping, is only called when the specific transcript is
   first requested, and then cached for subsequent requests.
2. While the transcripts file is loaded using a context manager and kept in memory, the actual translation
   is done using a lazy-reader and append-only writer. As such, neither are kept in memory and an interruption
   will not fail the entire run, to better accomodate very large files.
3. The CLI and core functionality are decoupled to more easily integrate with other interfaces, e.g. a Django backend app.
4. The bulk of the error-handling is done in the CLI so issues can bubble-up. A number of specific and common errors are handled here.
5. Robust logging and testing are included as a baseline should functionality need to be extended. 

