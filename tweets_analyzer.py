import pandas as pd
import numpy as np
from helper_functions import clean_tweet, extract_locations
from matplotlib import pyplot as plt


def BTC():
    btc_df = pd.read_json('data/bitcoin.json', orient='records')
    btc_df['clean_tweet'] = btc_df['tweet'].apply(lambda x: clean_tweet(x))
    btc_df['item'] = 'Bitcoin'
    btc_df.drop_duplicates(subset=['name'], keep='first', inplace=True)
    return btc_df


def DOGECOIN():
    doge_df = pd.read_json('data/dogecoin.json', orient='records')
    doge_df['clean_tweet'] = doge_df['tweet'].apply(
        lambda x: clean_tweet(x))
    doge_df['item'] = 'Dogecoin'
    doge_df.drop_duplicates(subset=['name'], keep='first', inplace=True)
    return doge_df


def ETHER():
    ether_df = pd.read_json('data/ethereum.json', orient='records')
    ether_df['clean_tweet'] = ether_df['tweet'].apply(lambda x: clean_tweet(x))
    ether_df['item'] = 'Ethereum'
    ether_df.drop_duplicates(subset=['name'], keep='first', inplace=True)
    return ether_df


def SHIVA():
    shiva_df = pd.read_json('data/shiva.json', orient='records')
    shiva_df['clean_tweet'] = shiva_df['tweet'].apply(
        lambda x: clean_tweet(x))
    shiva_df['item'] = 'Shiva'
    shiva_df.drop_duplicates(subset=['name'], keep='first', inplace=True)
    return shiva_df


def XRP():
    xrp_df = pd.read_json('data/XRP.json', orient='records')
    xrp_df['clean_tweet'] = xrp_df['tweet'].apply(lambda x: clean_tweet(x))
    xrp_df['item'] = 'XRP'
    xrp_df.drop_duplicates(subset=['name'], keep='first', inplace=True)
    return xrp_df


def join_dfs():
    btc_df = BTC()
    doge_df = DOGECOIN()
    ether_df = ETHER()
    shiva_df = SHIVA()
    xrp_df = XRP()

    frames = [btc_df, doge_df, ether_df, shiva_df, xrp_df]

    housemates_df = pd.concat(frames, ignore_index=True)
    return housemates_df


def analyze():
    housemates_df = join_dfs()

    # Number of Fans
    fans_by_housemate = housemates_df.groupby(
        'item')['name'].count().reset_index()
    fans_by_housemate.columns = ['item', 'no_of_fans']

    # Locations
    housemates_df['location'] = housemates_df['location'].apply(
        lambda location: extract_locations(location))
    fans_by_location = pd.DataFrame(housemates_df.groupby('item')[
                                    'location'].value_counts().rename('count')).reset_index()

    # Average
    followers_of_fans_by_hm = housemates_df.groupby(
        'item')['followers'].mean().reset_index()
    followers_of_fans_by_hm.columns = [
        'item', 'promedio']

    return (fans_by_housemate, fans_by_location, followers_of_fans_by_hm)


def plot_graphs():
    analysis_details = analyze()
    fans_by_housemate, fans_by_location, _ = analysis_details

    # Bar Chat for numbers of fans of housmates
    fig1, ax1 = plt.subplots()
    ax1.bar(fans_by_housemate['item'],
            fans_by_housemate['no_of_fans'], label='fans by item')
    ax1.set_xlabel('item')
    ax1.set_ylabel('twitter Fans')
    ax1.set_title(' Twitter Fans  item')

    # Bar Chart for locations of fans of housemates
    ax2 = fans_by_location.pivot(index='item', columns='location', values='count').T.plot(
        kind='bar', label='fans by location')
    ax2.set_xlabel('Locations')
    ax2.set_ylabel('Twitter Fans')
    ax2.set_yticks(np.arange(0, 300, 15))
    ax2.set_title('Location of Twitter Fans of Housemates')
    ax2.figure.set_size_inches(10, 17)

    list_of_figures = [plt.figure(i) for i in plt.get_fignums()]
    return list_of_figures


if __name__ == "__main__":
    plot_graphs()
