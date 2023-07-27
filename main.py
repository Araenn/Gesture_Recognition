import readingsUtils.csv_reading.csvUtils as CSV
import signalUtils as SIGNAL

if __name__ == "__main__":

        #seq_to_read = "data/our_datas/non_gesture/Non-gesture_8_Lea.csv"
        seq_to_read = "data/our_datas/gestures/processed/last.csv"
        seq_to_labelise = "data/our_datas/gestures/raw/last.csv"
        normalised_timestamp_acc, x_gyros, y_gyros, z_gyros, x_accel, y_accel, z_accel, fs = CSV.reading_into_csv(
                seq_to_read)

        """
        ATTENTION PROBLEME TOUJOURS EN MOUVEMENT
        """

        # PARAMETERS FOR THE REST OF THE CODE
        #seq9 : sigma = 1, threshold = 0.3
        #seq8 : sigma = 1, threshold = 0.3
        #seq7 : sigma = 47, threshold = 0.3
        #seq6 : sigma = 47, threshold = 0.3
        #seq5 : sigma = 70, threshold = 0.4
        #seq4 : sigma = 46, threshold = 0.3
        #seq3 : sigma = 11, threshold = 0.3
        #seq2 : sigma = 50, threshold = 0.21
        #seq1 : sigma = 50, threshold = 0.2
        threshold_multiplier = 0.1 # if low (<0.2), detection is very harsh, else, detection is more smooth (overlapping gestures)

        sigma = 0.001


        # SEGMENTATION
        true_mvmt = CSV.labelise_data(seq_to_labelise)

        start_xaccel, end_xaccel, start_yaccel, end_yaccel, start_zaccel, end_zaccel = SIGNAL.all_calculations(
                x_accel, y_accel, z_accel,
                normalised_timestamp_acc, sigma, threshold_multiplier, true_mvmt, fs)

        
