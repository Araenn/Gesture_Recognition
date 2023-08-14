import csv

def reading_into_csv(path):
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        timestamp_subject01_gesture09 = []
        normalised_timestamp = []
        x_accel = []
        y_accel = []
        z_accel = []

        x_gyros = []
        y_gyros = []
        z_gyros = []

        line_count = 0
        
        for row in csv_reader:
            timestamp_subject01_gesture09.append(row[0])
            normalised_timestamp.append(float(timestamp_subject01_gesture09[line_count]) - float(timestamp_subject01_gesture09[0]))
            
            x_accel.append(float(row[4]))
            y_accel.append(float(row[5]))
            z_accel.append(float(row[6]))

            x_gyros.append(float(row[1]))
            y_gyros.append(float(row[2]))
            z_gyros.append(float(row[3]))
        
            line_count += 1

        diff_timestamps = (normalised_timestamp[-1] - normalised_timestamp[0]) / len(normalised_timestamp)
        fs = 1 / diff_timestamps

    return normalised_timestamp, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros, fs

def labelise_data(path):
    normalised_timestamp, x_accel, y_accel, z_accel, x_gyros, y_gyros, z_gyros, fs = reading_into_csv(path)
    true_start = []
    true_end = []

    starting_timestamp = float(2 * normalised_timestamp[1] - normalised_timestamp[2])
    true_start.append(0)
    for i in range(1, len(normalised_timestamp)):
        if normalised_timestamp[i] == 0:
            true_start.append(((normalised_timestamp[i + 1] + normalised_timestamp[i - 2]) / 2) - starting_timestamp)
        if normalised_timestamp[i] == -1:
            true_end.append(((normalised_timestamp[i + 1] + normalised_timestamp[i - 2]) / 2) - starting_timestamp)

    true_end.append(((normalised_timestamp[-1] + normalised_timestamp[-2]) / 2) - starting_timestamp)
    return [true_start, true_end]
