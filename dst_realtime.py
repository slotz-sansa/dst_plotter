"""

Read DST quicklook file.


"""

# IMPORTS
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

# CONSTANTS
yyyy = dt.datetime.now().year
mm=dt.datetime.now().month
yy = yyyy - int(yyyy/100)*100
hours_perday = 24
number_length = 4
na_val = 9999

dst_url = f"https://wdc.kugi.kyoto-u.ac.jp/dst_realtime/presentmonth/"

dst_filename = f"dst{yy}{mm :02d}.for.request"


def main():

    getfile(url=dst_url + dst_filename, local_path=dst_filename)

    with open(dst_filename, "r") as file:
        lines = file.readlines()

    date_str = []
    data_str = []
    data_list = []
    df_list = []

    for line in lines:
        line = line.strip()
        if len(line)==120:
            date_str.append(line[3:7] + line[8:10])
            data_str.append(line[20:-4])

    print(len(data_str))

    data_matrix = np.zeros((len(data_str),hours_perday))


    for i,text in enumerate(data_str):
        df = pd.DataFrame()
        # chunks = textwrap(data,4)
        chunks = np.array([int(text[j:j+number_length]) for j in range(0, len(text), number_length)])
        # print(chunks.shape)
        data_matrix[i,:] = chunks
        start_time = dt.datetime.strptime('20'+date_str[i], '%Y%m%d')
        df['pdate'] = pd.date_range(start=start_time, periods=hours_perday, freq='1H')
        df['dst'] = chunks
        df_list.append(df)

        # data_list.append([int(text[j:j+k]) for j in range(0, len(text), k)])

    df = pd.concat(df_list)
    df.set_index('pdate',inplace=True)
    df.dst.mask(df.dst==na_val, inplace=True)

    # make plot
    plt.figure()
    df.dst.plot()
    plt.xlabel("Universal Date / Time")
    plt.ylabel("Dst [nT]")
    plt.title(f"Quicklook Dst from WDC Kyoto for {yyyy}/{mm}")
    plt.tight_layout()

    return df


def getfile(url, local_path):

    import requests

    print(f"Downloading file from {url}")
    response = requests.get(url)

    # Save file
    with open(local_path, "wb") as f:
        f.write(response.content)

    print(f"File saved to {local_path}")

    return 