import pandas as pd

# Read Datasets
df1 = pd.read_csv('datasets/dataset-1.csv')
df2 = pd.read_csv('datasets/dataset-2.csv')

def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    car_matrix = pd.pivot_table(df1,values='car',index='id_1',columns='id_2',fill_value=0)
    
    return car_matrix


def get_type_count(value):
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    if value <= 15:
        return 'low'
    elif 15 < value >= 25:
        return 'medium'
    else:
        return 'high'

# Apply the 'get_type_count' function to create a new 'car_type' column 
df1['car_type']=df1['car'].apply(get_type_count)
print(df1)


def get_bus_indexes(df1)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    mean_bus=df1[df1['bus'] > 2 * (df1['bus'].mean())].index
    
    return list(mean_bus)


def filter_routes(df):
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    group_route=df1.groupby('route')
    avg_truck=group_route['truck'].mean()
    route=avg_truck[avg_truck > 7].tolist()
    
    return sorted(route)

# Generate the car matric
matrix=generate_car_matrix(df1)

def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    modified_matrix=matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    return modified_matrix


def time_check(df2)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
     # Extract relevant columns
    df2 = df2[["id", "id_2", "startDay", "startTime", "endDay", "endTime"]]

    # Convert timestamps to datetime
    df2["startTime"] = pd.to_datetime(df2["startTime"])
    df2["endTime"] = pd.to_datetime(df2["endTime"])

    # Calculate duration
    df2["duration"] = df2["endTime"] - df2["startTime"]

    # Check for incorrect timestamps
    incorrect_timestamps = (
        (df2["duration"] != pd.to_timedelta("24 hours")) |
        (df2["startTime"].dt.dayofweek.nunique() != 7)
    )

    # Create a boolean series with multi-index (id, id_2)
    result_series = df2.groupby(["id", "id_2"]).apply(lambda x: any(incorrect_timestamps[x.index]))

    return result_series

# Call the function and print the results
result = time_check(df2)
print("Incorrect timestamps:")
print(result)
