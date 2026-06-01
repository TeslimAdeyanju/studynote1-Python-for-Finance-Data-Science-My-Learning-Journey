# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a personal Python learning journey repository — a structured collection of Jupyter notebooks documenting progress from Python fundamentals through data science. It is not a deployable application; work here is primarily adding or editing notebooks.

## Common Commands

```bash
# Launch Jupyter Notebook server
jupyter notebook

# Install all dependencies
pip install pandas numpy matplotlib seaborn jupyter scikit-learn

# Run a single notebook non-interactively (useful for testing)
jupyter nbconvert --to notebook --execute path/to/notebook.ipynb
```

The VS Code settings configure conda as the default Python environment manager (`ms-python.python:conda`).

## Repository Structure

Modules are numbered to reflect the intended learning sequence:

| Directory | Content |
|---|---|
| `1_python_datacamp_tutorial_note/` | DataCamp course notes (chapters 1–12), each subfolder maps to one course |
| `2_python_main_language/` | Core Python: introduction → data structures → control flow → functions → OOP → modules → exceptions → file handling |
| `3_python_numpy_modules/` | NumPy: array creation and manipulation notebooks |
| `4_python_pandas_data_analysis/` | Pandas deep-dives: `1_series_df_series/` covers Series in ~16 sequentially numbered notebooks; `2_dataframe/` covers DataFrames |
| `5_python_visualisation_modules/` | Matplotlib and Seaborn plotting notes |
| `6_python_exercise_projects/` | Free-form practice notebooks (OOP, OpenML, pandas, functions) |

### Notebook naming conventions

- Within a topic folder, notebooks are prefixed with a number (`1_`, `2_`, `8_`, etc.) that indicates the progression order.
- `note.ipynb` or `code_note.ipynb` are general chapter notes for a DataCamp course.
- `*_practice.ipynb` / `*_revise.ipynb` are personal reinforcement exercises.

## Notion Integration

A Notion MCP connection is configured in `.vscode/settings.json`. The workspace has two key pages:

- **StudyHub** — main learning tracker (`261807ec796380239114f266425fe29c`)
- **Data Science Database** — structured notes database (`261807ec796380898cf1d03946fd8c6a`)

Credentials live in `.env.notion` (git-ignored). Do not commit that file.

## Data Files

Several notebooks depend on local data files kept alongside them (CSV, Excel, SQLite, HDF5, SAS, Stata, MATLAB formats). When editing or executing a notebook, ensure the working directory is set to the notebook's own folder so relative paths resolve correctly.
