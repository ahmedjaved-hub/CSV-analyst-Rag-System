import pandas as pd 
import io

def build_csv_context(df:pd.DataFrame) -> str:
    """Build a context string from CSV bytes"""
    
    
    lines = []

    #1. Basic shape
    lines.append(f"Dataset: {df.shape[0]} rows x {df.shape[1]} columns")


    #2. Column names and types
    lines.append("Columns  (name | dtype | null count)")
    for col in df.columns:
        dtype = str(df[col].dtype)
        null_count = int(df[col].isnull().sum())
        lines.append(f"  - {col!r} | {dtype} | {null_count}")
    
    lines.append(" ")
    
    
    #3 .numeric  summary statistics
    numeri_cols = df.select_dtypes(include='number') 
    if not numeri_cols.empty:
        lines.append("Summary Statistics (numeric columns):")
        stats = numeri_cols.describe().round(2)
        lines.append(stats.to_string())
        lines.append(" ")

    #4. Categorical summary
    catogorical_cols = df.select_dtypes(include=["object","category"])
    if not catogorical_cols.empty:
        lines.append("Categorical Columns (top 5 frequent values)")
        for col in catogorical_cols.columns:
            top5 = df[col].value_counts().head(5).to_dict()
            lines.append(f"  - {col!r}: {top5}")
        lines.append(" ")

    #5 sample rows
    lines.append("Sample rows (first 20):")
    lines.append(df.head(20).to_string(index=False))
    return "\n".join(lines)
    