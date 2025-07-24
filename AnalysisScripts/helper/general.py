import pandas as pd
import os

def aggregate_by_date(df, date_col, aggregation_column, aggregation_function):
    """
    Aggregate a single column by date.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        date_col (str): The column containing date values.
        aggregation_column (str): The column to aggregate.
        aggregation_function (str or callable): Aggregation function (e.g., 'mean', 'sum', etc.).

    Returns:
        pd.DataFrame: A DataFrame aggregated by date.
    """
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce", utc=True)
    
    # Drop invalid dates
    df = df.dropna(subset=[date_col])
    
    df[date_col] = df[date_col].dt.date
    aggregated_df = df.groupby(date_col)[aggregation_column].agg(aggregation_function).reset_index()
    aggregated_df["count"] = df.groupby(date_col).size().values
    
    column_order = [date_col, "count", aggregation_column]
    return aggregated_df[column_order]

def aggregate_by_category(df, category_col, aggregation_column, aggregation_function):    
    """
    Aggregate a single column by category.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        category_col (str): The column containing category values.
        aggregation_column (str): The column to aggregate.
        aggregation_function (str or callable): Aggregation function (e.g., 'mean', 'sum', etc.).

    Returns:
        pd.DataFrame: A DataFrame aggregated by category.
    """
    aggregated_df = df.groupby(category_col)[aggregation_column].agg(aggregation_function).reset_index()
    aggregated_df["count"] = df.groupby(category_col).size().values
    
    column_order = [category_col, "count", aggregation_column]
    return aggregated_df[column_order]

def generate_value_in_buckets(df, date_column, aggregation_column, aggregation_settings='mean', bucket_size=7, bucket_value_prefix='', create_empty_buckets=True):
    """
    Generate aggregated values in buckets based on a date column.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        date_column (str): The name of the date column in the DataFrame.
        aggregation_column (str): The column to aggregate.
        aggregation_settings (str or callable): Aggregation function (e.g., 'mean', 'sum', etc.).
        bucket_size (int): The size of each bucket in days.
        bucket_value_prefix (str): The prefix for the bucket labels.

    Returns:
        pd.DataFrame: A DataFrame with aggregated values for each bucket.
    """
    # Ensure the date column is in datetime format
    df.loc[:, date_column] = pd.to_datetime(df[date_column], errors="coerce", utc=True)
    df = df.dropna(subset=[date_column])  # Drop rows with invalid dates

    # Create a bucket column based on the date difference
    df["bucket"] = (df[date_column] - df[date_column].min()).dt.days // bucket_size

    # Add the prefix to the bucket labels
    df["bucket"] = df["bucket"].apply(lambda x: f"{bucket_value_prefix}{x}")
    
    # if the aggregation column doesnt exist, create it with NaN values
    if (aggregation_column not in df.columns and create_empty_buckets):
        df[aggregation_column] = pd.NA
        print(f"Warning: {aggregation_column} not found in DataFrame. Creating it with NaN values.")

    # Aggregate values within each bucket
    aggregated_df = df.groupby("bucket")[aggregation_column].agg(aggregation_settings).reset_index()

    # Calculate start and end dates for each bucket
    aggregated_df["start_date"] = df[date_column].min() + pd.to_timedelta(
        aggregated_df["bucket"].astype(str).str.replace(bucket_value_prefix, "").astype(int) * bucket_size, unit="days"
    )
    aggregated_df["end_date"] = aggregated_df["start_date"] + pd.to_timedelta(bucket_size, unit="days")

    if df.empty:
        return pd.DataFrame(columns=['bucket', aggregation_column, 'start_date', 'end_date'])

    # Ensure all buckets are included, even if empty
    all_buckets = pd.DataFrame({
        "bucket": [f"{bucket_value_prefix}{i}" for i in range((df[date_column].max() - df[date_column].min()).days // bucket_size + 1)]
    })
    aggregated_df = pd.merge(all_buckets, aggregated_df, on="bucket", how="left")

    return aggregated_df
    
def split_by_date(df, introduction_date, date_column):
    """
    Split the DataFrame into two parts: one with data before the introduction date and one after.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        introduction_date (datetime or str): The date to split the DataFrame on.
        date_column (str): The name of the date column in the DataFrame.

    Returns:
        tuple: Two DataFrames, one with data before the introduction date and one with data after.
    """
    # Ensure the date column is in datetime format
    df[date_column] = pd.to_datetime(df[date_column], errors="coerce", utc=True)
    df = df.dropna(subset=[date_column])  # Drop rows with invalid dates

    # Convert introduction_date to datetime if it's a string
    introduction_date = pd.to_datetime(introduction_date, errors="coerce", utc=True)

    # Split the DataFrame
    before_intro = df[df[date_column] < introduction_date]
    after_intro = df[df[date_column] >= introduction_date]

    return before_intro, after_intro
    
    
def truncate_to_same_length(df, introduction_date, date_col, direction='both', start_date=None, end_date=None):
    """
    Truncate the DataFrame to ensure equal time ranges before and/or after the introduction date.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        introduction_date (datetime or str): The date to truncate around.
        date_col (str): The name of the date column in the DataFrame.
        direction (str): The direction to truncate ('both', 'before', 'after', 'defined').

    Returns:
        pd.DataFrame: The truncated DataFrame.
    """
    # Ensure the date column is in datetime format 
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce", utc=True)
    df = df.dropna(subset=[date_col])  # Drop rows with invalid dates

    # Convert introduction_date to datetime if it's a string
    introduction_date = pd.to_datetime(introduction_date, errors="coerce", utc=True)
    if pd.isna(introduction_date):
        raise ValueError("Invalid introduction_date provided.")

    # Calculate the time range for truncation
    min_date = df[date_col].min()
    max_date = df[date_col].max()
    time_before = (introduction_date - min_date).days
    time_after = (max_date - introduction_date).days

    if direction == 'defined':
        if not start_date or not end_date:
            start_date = pd.to_datetime(os.getenv("START_DATE"), errors="coerce", utc=True)
            end_date = pd.to_datetime(os.getenv("END_DATE"), errors="coerce", utc=True)
        else:
            start_date = pd.to_datetime(start_date, errors="coerce", utc=True)
            end_date = pd.to_datetime(end_date, errors="coerce", utc=True)

        if pd.isna(start_date) or pd.isna(end_date):
            raise ValueError("Invalid START_DATE or END_DATE environment variables provided.")

        if start_date > end_date:
            raise ValueError("START_DATE cannot be after END_DATE.")

        df = df[(df[date_col] >= start_date) & (df[date_col] <= end_date)]
    
    elif direction == 'both':
        truncate_days = min(time_before, time_after)
        start_date = introduction_date - pd.Timedelta(days=truncate_days)
        end_date = introduction_date + pd.Timedelta(days=truncate_days)
    elif direction == 'before':
        start_date = introduction_date - pd.Timedelta(days=time_after)
    elif direction == 'after':
        truncate_days = time_before
        end_date = introduction_date + pd.Timedelta(days=truncate_days)

    # # Truncate the data
    # truncated_start_date = introduction_date - pd.Timedelta(days=truncate_days)
    # truncated_end_date = introduction_date + pd.Timedelta(days=truncate_days)
    df = df[(df[date_col] >= start_date) & (df[date_col] <= end_date)]
        
    return df

def get_repository_paths(repository_directories):
    repositories = []
    for directory in repository_directories:
        if os.path.exists(directory):
            first_level_subdirs = [
                os.path.join(directory, subfolder)
                for subfolder in os.listdir(directory)
                if os.path.isdir(os.path.join(directory, subfolder)) and not subfolder.startswith('.')
            ]
            repositories.extend(first_level_subdirs)
    return repositories

def validate_path(path):
    if not os.path.exists(path) or os.stat(path).st_size == 1:
        print(f"File not found or empty: {path}. Skipping repository.")
        return False
    return True