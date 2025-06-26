import marimo

__generated_with = "0.14.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # New Zealand Weka Hills Leapfrog Demo Project

    Weka Hills is a ficticious location in New Zealand that is used in Leapfrog Works training. The data relevant to this ficticious project can be downloaded from here:  
    https://files.seequent.com/training/Data/Works/Weka_Hills.zip

    The Ground Investigation (GI) data as CSV's can be found here:  
    https://github.com/bedrock-engineer/bedrock-ge/tree/main/examples/nz_weka_hills_leapfrog
    """
    )
    return


@app.cell
def _(mo):
    nb_dir = mo.notebook_location()
    gi_csvs = [file.name for file in nb_dir.iterdir() if (file.is_file() and file.suffix.lower() == ".csv")]
    gi_csvs
    return


if __name__ == "__main__":
    app.run()
