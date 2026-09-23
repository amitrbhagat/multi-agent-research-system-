import logging
import pandas as pd

logger = logging.getLogger(__name__)

DATABASE_PATH = "./data/sample_dataset.csv"


def load_dataset() -> pd.DataFrame:
    return pd.read_csv(DATABASE_PATH)


def answer_data_question(query: str) -> dict:

    try:
        df = load_dataset()
        query_lower = query.lower()


        if "average" in query_lower or "mean" in query_lower:
            column = _guess_numeric_column(df, query)
            if column:
                value = df[column].mean()
                return {"answer": f"The average {column} is {value:.2f}" ,"value": value} 


        if "total" in query_lower or "sum" in query_lower:
            column = _guess_numeric_column(df, query) 
            if column:
                value = df[column].sum()
                return {"answer": f"The total {column} is {value:.2f}" ,"value": value}  


        if "max" in query_lower or "highest" in query_lower:
            column = _guess_numeric_column(df, query) 
            if column:
                value = df[column].max()
                return {"answer": f"The highest {column} is {value:.2f}" ,"value": value}  

        return {"answer": "I couldn't map this question to a supported dataset operation.", "value": None}

    except Exception as e:
        logger.error(f"data analyst query failed {e}")
        return {"answer": "Data analysis failed due to an internal error.", "value": None}



def _guess_numeric_column(df: pd.DataFrame, query_lower: str) -> str | None:
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        if col.lower() in query_lower:
            return col
    return numeric_cols[0] if len(numeric_cols) else None     
