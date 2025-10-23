# Deep Learning AI

This project contains a series of Jupyter notebooks for learning about Google's Agent Development Kit (adk).

## Environment Setup

These instructions use `uv` for environment management.

### 1. Create the Virtual Environment

This will create a `.venv` directory in your project root.

```bash
uv venv
source .venv/bin/activate
```

### 2. Install Dependencies

Install all the required packages from `requirements.txt`.

```bash
uv pip install -r requirements.txt
```

## Updating the Notebooks

To use the `helper.py` module in your notebooks, you can now simply import it at the beginning of each notebook:

```python
import helper
```

You no longer need to manipulate `sys.path`. You should remove any existing code in the notebooks that looks like this:

```python
import sys
sys.path.append('../')
```
