# Autocomplete System (Search Suggestions)

This project implements a basic autocomplete search suggestion system in Python.

## Features

- Insert words with a frequency count
- Real-time updates (insert or update frequency)
- Retrieve top-k suggestions for a given prefix

## Structure

- `src/autocomplete.py` - core implementation using a Trie
- `src/test_autocomplete.py` - unit tests demonstrating the functionality

## Usage

Run the module directly to see a simple demo:

```bash
python src/autocomplete.py
```

Run tests:

```bash
python -m unittest src/test_autocomplete.py
```

Feel free to extend with a CLI or web interface as needed.
