import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import csv
import sys
from datetime import datetime

csv.field_size_limit(sys.maxsize)

burn_address = "0x0000000000000000000000000000000000000000"
sea_token = "0x26193c7fa4354ae49ec53ea2cebc513dc39a10aa"

def get_per_user_spending():
    user_transaction_volume_dict = {}
    with open("in-game-token-transfers.csv", "r") as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader)
        for row in data_reader:
            if len(row) < 7:
                continue
            token = row[0]
            if token != sea_token:
                continue
            user_address = row[1]
            if user_address == burn_address:
                continue
            transaction_value = int(row[3]) / 1000000000000000000
            if user_address in user_transaction_volume_dict:
                user_transaction_volume_dict[user_address] += transaction_value
            else:
                user_transaction_volume_dict[user_address] = transaction_value

    return user_transaction_volume_dict
    #return dict(filter(lambda elem: elem[1] < 100, user_transaction_volume_dict.items()))

def get_spending_distribution(user_transaction_volume_dict):
    spending_distribution = {}
    for user_address, user_transaction_volume in user_transaction_volume_dict.items():
        if user_transaction_volume in spending_distribution:
            spending_distribution[user_transaction_volume] += 1
        else:
            spending_distribution[user_transaction_volume] = 1
    print("spending_distribution: ", spending_distribution)
    #print("sorted spending distribution")
    #for key, value in sorted(spending_distribution.items(), key=lambda item: item[1]):
    #    print(key, value)
    #print("sorted spending distribution end")
    total_frequency = sum(spending_distribution.values())
    #print("total_frequency: ", total_frequency)

    user_transaction_volume_arr = sorted(spending_distribution.keys())
    user_transaction_volume_frequency_arr = [0] * len(user_transaction_volume_arr)
    for i, user_transaction_volume in enumerate(user_transaction_volume_arr):
        #print("frequency: ", spending_distribution[user_transaction_volume])
        user_transaction_volume_frequency_arr[i] = float(spending_distribution[user_transaction_volume])/total_frequency
    return [user_transaction_volume_arr, user_transaction_volume_frequency_arr]




def visualize_curve_line(spending_2d_matrix):
    print(spending_2d_matrix)
    fig, ax = plt.subplots()

    x = np.array(spending_2d_matrix[0])
    y = np.array(spending_2d_matrix[1])

    print("x range: ", x.min(), x.max())

    model=make_interp_spline(x, y)

    x_smooth = np.linspace(x.min(), x.max(), 10000)
    y_smooth = model(x_smooth)
    #ax.plot(x_smooth, y_smooth)
    ax.plot(x, y)

    plt.ylim()
    plt.show()

def main():
    user_transaction_volume_dict = get_per_user_spending()

    #for user_address, user_transaction_volume in user_transaction_volume_dict.items():
    #    if user_transaction_volume > 100:
    #        print("user_address, user_transaction_volume", user_address, user_transaction_volume)
    spending_2d_matrix = get_spending_distribution(user_transaction_volume_dict)
    visualize_curve_line(spending_2d_matrix)

if __name__ == "__main__":
    main()
