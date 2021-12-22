import pandas as pd
import math
import csv
import datetime as dt
from tkinter.filedialog import askopenfilename, asksaveasfilename
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as tck
from matplotlib.ticker import MultipleLocator

steps = ["", "sfcr", "cfcr", "tr", "cab1", "cab2", "cab3", "cab4", "cab5", "cab6"]
summary_data = {}


def run():

    data_filename = choose_load_file()
    # save_filename = choose_save_file()

    data = pd.read_csv(data_filename)
    for index, row in data.iterrows():

        current_date = create_date(row["sr_start_time"])

        if not (current_date in summary_data):
            summary_data[current_date] = {"sfcr": 0, "cfcr": 0, "tr": 0, "cab1": 0, "cab2": 0, "cab3": 0, "cab4": 0, "cab5": 0, "cab6": 0}

        count_step_occurence(summary_data, row, current_date)

    output_data, xy_data = get_output_data(summary_data)
    plot_data(xy_data)
    # print_to_csv(output_data, save_filename, ["date", "most frequent", "highest step"])
    # summary_array = format_summary_to_array(summary_data)
    # print_to_csv(summary_array, "summary_data.csv", ["date", "sfcr", "cfcr", "tr", "cab1", "cab2", "cab3", "cab4", "cab5", "cab6"])


def plot_data(xy_data):
    # x_data = [row[0].strftime('%m-%d-%y') for row in xy_data]
    x_data = []
    for row in xy_data:
        x_data.append(row[0].strftime('%m-%d-%y'))
    y_data = [row[1] for row in xy_data]
    fig, ax = plt.subplots()
    ax.set_ylim(0, len(steps)-1)
    plt.yticks(range(len(steps)), steps)
    plt.ylabel('SBT Step')
    plt.xlabel('Date (mm/dd/yyyy)')
    plt.title('Progression with Skills Based Treatment (SBT)')
    # ax.xaxis.set_minor_locator(mdates.DayLocator())
    # ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m-%d-%y'))
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%y'))
    # plt.xticks(rotation=45, ha='right') # This will align the right side of the date with the tick
    ax.tick_params(axis="x", which="both", rotation=90) # This will align the center of the date to the tick

    ax.bar(x_data, y_data, width=0.5)
    plt.show()


def choose_load_file():
    filename = askopenfilename(initialdir='~/Desktop',
                               message="Choose a data file",
                               multiple=False,
                               title="File Selector",
                               filetypes=[("CSV Files", "*.csv")])

    return filename


def choose_save_file():
    filename = asksaveasfilename(initialdir='~/Desktop',
                                 title="Save the output data file",
                                 filetypes=[("CSV Files", "*.csv")])

    return filename
    

def format_summary_to_array(summary_data):
    summary_array = []
    for day in summary_data:
        temp = [day]
        for step in summary_data[day]:
            temp.append(summary_data[day][step])

        summary_array.append(temp)

    return summary_array

def get_output_data(summary_data):
    output = []
    xy_data = []

    for day in summary_data:
        most_freq = get_most_freq(summary_data[day])

        val = 0
        if most_freq == 'sfcr':
            val = 1
        elif most_freq == 'cfcr':
            val = 2
        elif most_freq == 'tr':
            val = 3
        elif most_freq == 'cab1':
            val = 4
        elif most_freq == 'cab2':
            val = 5
        elif most_freq == 'cab3':
            val = 6
        elif most_freq == 'cab4':
            val = 7
        elif most_freq == 'cab5':
            val = 8
        elif most_freq == 'cab6':
            val = 9

        output.append([day, val, most_freq, get_highest_step(summary_data[day])])
        xy_data.append([day, val])

    xy_data.sort()
    return output, xy_data


def count_step_occurence(summary_data, row, current_date):
    if not (math.isnan(row["cab6_result"]) or row["cab6_result"] == 0):
        if row["cab6_r1_count"] == 0 and row["cab6_r2_count"] == 0:
            summary_data[current_date]["cab6"] = summary_data[current_date]["cab6"] + 1
            return

    if not (math.isnan(row["cab5_result"]) or row["cab5_result"] == 0):
        if row["cab5_r1_count"] == 0 and row["cab5_r2_count"] == 0:
            summary_data[current_date]["cab5"] = summary_data[current_date]["cab5"] + 1
            return

    if not (math.isnan(row["cab4_result"]) or row["cab4_result"] == 0):
        if row["cab4_r1_count"] == 0 and row["cab4_r2_count"] == 0:
            summary_data[current_date]["cab4"] = summary_data[current_date]["cab4"] + 1
            return

    if not (math.isnan(row["cab3_result"]) or row["cab3_result"] == 0):
        if row["cab3_r1_count"] == 0 and row["cab3_r2_count"] == 0:
            summary_data[current_date]["cab3"] = summary_data[current_date]["cab3"] + 1
            return

    if not (math.isnan(row["cab2_result"]) or row["cab2_result"] == 0):
        if row["cab2_r1_count"] == 0 and row["cab2_r2_count"] == 0:
            summary_data[current_date]["cab2"] = summary_data[current_date]["cab2"] + 1
            return

    if not (math.isnan(row["cab1_result"]) or row["cab1_result"] == 0):
        if row["cab1_r1_count"] == 0 and row["cab1_r2_count"] == 0:
            summary_data[current_date]["cab1"] = summary_data[current_date]["cab1"] + 1
            return

    if not (math.isnan(row["tr_result"]) or row["tr_result"] == 0):
        if row["tr_r1_count"] == 0 and row["tr_r2_count"] == 0:
            summary_data[current_date]["tr"] = summary_data[current_date]["tr"] + 1
            return

    if not (math.isnan(row["cfcr_result"]) or row["cfcr_result"] == 0):
        if row["cfcr_r1_count"] == 0 and row["cfcr_r2_count"] == 0:
            summary_data[current_date]["cfcr"] = summary_data[current_date]["cfcr"] + 1
            return

    if not (math.isnan(row["sfcr_result"]) or row["sfcr_result"] == 0):
        if row["sfcr_r1_count"] == 0 and row["sfcr_r2_count"] == 0:
            summary_data[current_date]["sfcr"] = summary_data[current_date]["sfcr"] + 1
            return


def get_highest_step(data):
    highest = "sfcr"
    for step in data:
        # now compare with the previous highest value
        if data[step] != 0:
            highest = step

    return highest


def create_date(old_date):
    year = int(old_date[:4])
    month = int(old_date[5:7])
    day = int(old_date[8:10])
    new_date = dt.date(year, month, day)
    return new_date


def print_to_csv(data, filename, header):

    # write to csv by row
    with open(filename, mode="w") as file:
        file_writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(header)
        for row in data:
            file_writer.writerow(row)


def get_most_freq(data):
    highest = "sfcr"
    for step in data:
        # now compare with the previous highest value
        if data[step] >= data[highest]:
            highest = step

    return highest


if __name__ == "__main__":
    run()
