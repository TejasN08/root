import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
   
    distance_matrix = df.copy()

    for start in df.index:
        for end in df.index:
            if start != end:
                distance = df.loc[start, 'AB'] + df.loc[end, 'AB']
                distance_matrix.at[start, end] = distance
                distance_matrix.at[end, start] = distance

    return distance_matrix


print(calculate_distance_matrix(df))


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    unrolled_data = []

    for start in distance_matrix.index:
        for end in distance_matrix.columns:
            if start != end:
                distance = distance_matrix.at[start, end]
                unrolled_data.append({'id_start': start, 'id_end': end, 'distance': distance})

    unrolled_df = pd.DataFrame(unrolled_data, columns=['id_start', 'id_end', 'distance'])
    return unrolled_df



def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    reference_average = df[df['id_start'] == reference_value]['distance'].mean()
    threshold_min = reference_average * 0.9
    threshold_max = reference_average * 1.1

    within_threshold_ids = df[(df['id_start'] != reference_value) & (df['distance'] >= threshold_min) & (df['distance'] <= threshold_max)]['id_start'].unique()
    
    return sorted(within_threshold_ids)

# Assuming unrolled_df is the DataFrame created in Question 2
reference_value = 1  # You can choose any ID as the reference value
threshold_ids = find_ids_within_ten_percentage_threshold(unrolled_df, reference_value)
print(f"IDs within 10% threshold of {reference_value}: {threshold_ids}")

    


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Create new columns for each vehicle type and calculate toll rates
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df

toll_rates_df = calculate_toll_rate(df)
print("Toll Rates DataFrame:")
print(toll_rates_df)



def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Convert 'start_time' and 'end_time' columns to datetime.time objects
    df['start_time'] = pd.to_datetime(df['start_time']).dt.time
    df['end_time'] = pd.to_datetime(df['end_time']).dt.time

    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        for start_time, end_time, discount_factor in [(time(0, 0, 0), time(10, 0, 0), 0.8),
                                                     (time(10, 0, 0), time(18, 0, 0), 1.2),
                                                     (time(18, 0, 0), time(23, 59, 59), 0.8)]:
            mask = (df['start_day'] == day) & (df['end_day'] == day) & (df['start_time'] >= start_time) & (df['end_time'] <= end_time)
            df.loc[mask, ['moto', 'car', 'rv', 'bus', 'truck']] *= discount_factor

        mask_weekend = (df['start_day'].isin(['Saturday', 'Sunday'])) & (df['end_day'].isin(['Saturday', 'Sunday']))
        df.loc[mask_weekend, ['moto', 'car', 'rv', 'bus', 'truck']] *= 0.7

    return df

