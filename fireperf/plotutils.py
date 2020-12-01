
def make_plot_title(df):
    """Return a string containing all of the constant columns 
       of the DataFrame."""
    const_cols = {}
    for col in df.columns:
        if df[col].nunique() == 1:
            const_cols[col] = df[col][0]

    return str(const_cols)
