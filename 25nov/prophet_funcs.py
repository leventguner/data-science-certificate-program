def make_verif(forecast, data_train, data_test):
    """
    Put together the forecast (coming from fbprophet)
    and the overved data, and set the index to be a proper datetime index,
    for plotting

    Parameters
    ----------
    forecast : pandas.DataFrame
        The pandas.DataFrame coming from the `forecast` method of a fbprophet
        model.

    data_train : pandas.DataFrame
        The training set, pandas.DataFrame

    data_test : pandas.DataFrame
        The training set, pandas.DataFrame

    Returns
    -------
    forecast :
        The forecast DataFrane including the original observed data.

    """

    forecast.index = pd.to_datetime(forecast.ds)

    data_train.index = pd.to_datetime(data_train.ds)

    data_test.index = pd.to_datetime(data_test.ds)

    data = pd.concat([data_train, data_test], axis=0)

    forecast.loc[:,'y'] = data.loc[:,'y']

    return forecast

def plot_verif(verif):
    """
    plots the forecasts and observed data, the `year` argument is used to visualise
    the division between the training and test sets.

    Parameters
    ----------
    verif : pandas.DataFrame
        The `verif` DataFrame coming from the `make_verif` function in this package

    year : integer
        The year used to separate the training and test set. Default 2017

    Returns
    -------
    f : matplotlib Figure object

    """

    f, ax = plt.subplots(figsize=(14, 8))

    train = verif.loc[:"2020-06-01",:]

    ax.plot(train.index, train.y, 'ko', markersize=3)

    ax.plot(train.index, train.yhat, color='steelblue', lw=0.5)

    ax.fill_between(train.index, train.yhat_lower, train.yhat_upper, color='steelblue', alpha=0.3)

    test = verif.loc["2020-06-02":,:]

    ax.plot(test.index, test.y, 'ro', markersize=3)

    ax.plot(test.index, test.yhat, color='coral', lw=0.5)

    ax.fill_between(test.index, test.yhat_lower, test.yhat_upper, color='coral', alpha=0.3)

    ax.axvline("2020-06-02", color='0.8', alpha=0.7)

    ax.grid(ls=':', lw=0.5)

    return f


def add_regressor(data, regressor, varname=None):

    """
    adds a regressor to a `pandas.DataFrame` of target (predictand) values
    for use in fbprophet

    Parameters
    ----------
    data : pandas.DataFrame
        The pandas.DataFrame in the fbprophet format (see function `prepare_data` in this package)
    regressor : pandas.DataFrame
        A pandas.DataFrame containing the extra-regressor
    varname : string
        The name of the column in the `regressor` DataFrame to add to the `data` DataFrame

    Returns
    -------
    verif : pandas.DataFrame
        The original `data` DataFrame with the column containing the
        extra regressor `varname`

    """

    data_with_regressors = data.copy()

    data_with_regressors.loc[:,varname] = regressor.loc[:,varname]

    return data_with_regressors

def add_regressor_to_future(future, regressors_df):
    """
    adds extra regressors to a `future` DataFrame dataframe created by fbprophet

    Parameters
    ----------
    data : pandas.DataFrame
        A `future` DataFrame created by the fbprophet `make_future` method

    regressors_df: pandas.DataFrame
        The pandas.DataFrame containing the regressors (with a datetime index)

    Returns
    -------
    futures : pandas.DataFrame
        The `future` DataFrame with the regressors added
    """

    futures = future.copy()

    futures.index = pd.to_datetime(futures.ds)

    df_w=df_weather.copy()

    data_regressor=pd.merge(df_w,data,how='left',on='ds')
    data_regressor.head()



    data_regressor =  data_regressor.reset_index(drop = True)

    return data_regressor
