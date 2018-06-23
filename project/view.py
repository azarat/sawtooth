import project.controller as dt
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
import os
from scipy import signal as signal_processor

# IMPORTANT to be declared for 3d plots
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, rc
from matplotlib.ticker import LinearLocator, FormatStrFormatter


class ViewData:
    processing = dt.PreProfiling()

    def __init__(self):
        print("Please input V1 or V2 \r\n"
              + "V1 - old version where code modification required \r\n"
              + "V2 - new version in dev \r\n"
              + "Input: V2")

        # run_program = input()
        # if run_program == "V1":
        #     self.main_v1()
        # elif run_program == "V2":
        self.main_v2()

    def main_v2(self):
        """ -----------------------------------------
            version: 0.2
            desc: build 3d plots
            :return 1

            status: IN DEV
        ----------------------------------------- """
        channel_from = 0
        channel_to = 48
        window_width_val = 181
        window_func = 'triang'

        for dis in range(25, 26):

            print(dis)

            if dis == 31:
                continue

            """ Extract data from MATLAB database """
            data = dt.Profiling(discharge=dis, source='real')
            # data_public = dt.Profiling(discharge=55, source='public')
            # # # # # # # # # # # # # # # # # # # # # # # #

            """ Sort R_maj index and time lists by R_maj value """
            # r_maj = [channel[1] for channel in sorted(data.channels_pos.items(), key=itemgetter(1))][channel_from:channel_to]
            channel_order_list = {index: channel[0] for index, channel in enumerate(sorted(data.channels_pos.items(), key=itemgetter(1)))}
            # time_list = data.time_original
            """ Same vars in a.u. units """
            r_maj = range(channel_from, channel_to)
            time_list = range(0, len(data.time_original))

            # print(time_list)
            # print(str(dis) + ': ' + str(len(r_maj)) + ' = ' + str(r_maj))
            # print(str(dis) + ': ' + str(dict(list(channel_order_list.items())[channel_from:channel_to])) + ' = ' + str(r_maj))
            # print(r_maj)
            # print('_')

            """ Ordering by R_maj """
            temperature_list_original = data.order_by_r_maj(data.temperature_original)[channel_from:channel_to]
            # public_temperature_ordered_list = data.order_by_r_maj(data_public.temperature_original)[channel_from:channel_to]
            # # # # # # # # # # # # # # # # # # # # # # # #

            """
            Filtering T(t), i.e., smoothing 
            WARNING: do not smooth due to info losses in 3d 
            """
            # temperature_list = self.processing.filter(
            #     temperature_list_original, window_width_val, window_func)
            temperature_list = temperature_list_original  # skip filtration
            # # # # # # # # # # # # # # # # # # # # # # # #

            """ Calibrate (Normalization on 1) """
            # temperature_list_original = data.normalization(temperature_list_original, "start")
            temperature_list = data.normalization(temperature_list, "start")
            # # # # # # # # # # # # # # # # # # # # # # # #

            self.build_temperature_rmaj_time_3d_surface(temperature_list, r_maj, time_list, discharge=dis)
            self.build_temperature_rmaj_time_3d_surface_perspective(temperature_list, r_maj, time_list, discharge=dis)
            # self.build_temperature_rmaj_single_plot(
            #     temperature=temperature_list,
            #     temperature_original=temperature_list_original,
            #     channels_pos=r_maj,
            #     window_width=window_width_val,
            #     channel_to_compare=1,
            #     time_list=time_list,
            #     channel_order_list=channel_order_list,
            #     window_name=window_func)
            # plt.close("all")

        plt.show()

        return 1

    @staticmethod
    def build_filter_windows(wind_list):
        """ -----------------------------------------
            version: 0.1
            :return 1
        ----------------------------------------- """
        for index, name in enumerate(wind_list):
            fig, axes = plt.subplots()
            fig.set_size_inches(15, 8)

            window = signal_processor.get_window(name, 100)

            axes.plot(
                range(0, len(window)),
                window
            )

            axes.set(xlabel='', ylabel='',
                     title=name)
            axes.grid(alpha=0.2)
            plt.tight_layout()

            directory = 'results/filters/'

            if not os.path.exists(directory):
                os.makedirs(directory)

            # fig.savefig(directory + 'filters_' + name + '.png')

        return 1

    @staticmethod
    def build_temperature_rmaj_time_3d_surface(temperature_list, r_maj, time_list, **kwargs):
        """ -----------------------------------------
            version: 0.2
            desc: build plot of top view of temperature distribution
            :param temperature_list: 2d list of num
            :param r_maj: 1d list of num
            :param time_list: 1d list of num
            :return 1
        ----------------------------------------- """
        fig = plt.figure()
        fig.set_size_inches(15, 7)

        # Make data.
        x = time_list[0:len(temperature_list[0])]
        y = r_maj
        x, y = np.meshgrid(x, y)
        z = np.array(temperature_list)

        # COLORMAP HERE
        cs = plt.contourf(x, y, z, 50, corner_mask=True, cmap=cm.Reds)
        plt.title('Temperature evolution cross JET tokamak, discharge ' + str(kwargs['discharge']), fontsize=17)
        plt.xlabel('Time', fontsize=17)
        plt.ylabel('R_maj', fontsize=17)
        # END

        # Add a color bar which maps values to colors.
        cbs = fig.colorbar(cs)
        cbs.ax.set_ylabel('Temperature (eV)', fontsize=17)

        # fig.savefig('results/3d_au_0_48/tokamat_colormap_reds_dis' + str(kwargs['discharge']) + '.png')

        return 1

    @staticmethod
    def build_temperature_rmaj_time_3d_surface_perspective(temperature_list, r_maj, time_list, **kwargs):
        """ -----------------------------------------
            version: 0.2
            desc: build plot of movable 3d view of temperature distribution
            :param temperature_list: 2d list of num
            :param r_maj: 1d list of num
            :param time_list: 1d list of num
            :return 1
        ----------------------------------------- """
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        fig.set_size_inches(15, 7)

        # Make data.
        x = time_list[0:len(temperature_list[0])]
        y = r_maj
        x, y = np.meshgrid(x, y)
        z = np.array(temperature_list)

        # COLORMAP HERE
        plt.title('Temperature evolution cross JET tokamak, discharge ' + str(kwargs['discharge']), fontsize=17)
        plt.xlabel('Time')
        plt.ylabel('R_maj')
        # END

        # Plot the surface.
        surf = ax.plot_surface(x, y, z, cmap=cm.plasma,
                               linewidth=0, antialiased=False)

        # Customize the z axis.
        # ax.set_ylim(2.95, 3.1)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # fig.savefig('results/3d_au_0_48/tokamat_perspective_plasma_dis' + str(kwargs['discharge']) + '.png')

        return 1

    @staticmethod
    def build_temperature_rmaj_single_plot(
       temperature, temperature_original, window_name,
       channels_pos, window_width, time_list,
       channel_to_compare, channel_order_list):
        """ -----------------------------------------
            version: 0.2
            :param: temperature: 2d array of filtered and calibrated temperature (list of nums)
            :param: temperature_original: 2d of original ordered temperature (list of nums)
            :param: window_name: str value of window of recently wind. filtration
            :param: channels_pos: 1d array of channel position values
            :param: window_width: int width of window of recently wind. filtration
            :param: time_list: 1d array of nums
            :param: channel_to_compare: int index for array with channels
            :param: channel_order_list: 1d array with ordered channels by own value
            :return 1
        -----------------------------------------
        desc: Build single plot T(t) with fixed r_maj
        CAUTION: inverting plasma radius is near 48/49 channel (in ordered unit list)
        CAUTION: channel_to_check means temperature set, ordered by r_maj
        """

        fig, axes = plt.subplots()
        fig.set_size_inches(15, 7)

        axes.plot(
            # range(0, len(temperature_original[channel_to_compare])),
            time_list[0:len(temperature_original[channel_to_compare])],
            temperature_original[channel_to_compare],
            alpha=0.5,
            color='c'
        )

        axes.plot(
            # range(0, len(temperature[channel_to_compare])),
            time_list[0:len(temperature[channel_to_compare])],
            temperature[channel_to_compare],
            color='b'
        )

        axes.set(xlabel='Time (seconds)', ylabel='T (eV)',
                 title='Original signal vs filtered, "'
                       + window_name + '" wind. func., '
                       + str(channel_order_list[channel_to_compare]) + ' channel, 25 discharge, '
                       'wind. width ' + str(window_width) +
                       ', R_maj = ' + str(channels_pos[channel_to_compare]))

        for item in ([axes.title, axes.xaxis.label, axes.yaxis.label] +
                     axes.get_xticklabels() + axes.get_yticklabels()):
            item.set_fontsize(17)

        axes.grid()

        # self.align_axes(axes)

        directory = 'results/originals/d25/' \
                    'o' + str(channel_to_compare) + \
                    '_c' + str(channel_order_list[channel_to_compare]) + '/' + \
                    str(window_name) + '/'
        # if not os.path.exists(directory):
        #     os.makedirs(directory)
        #
        # fig.savefig(directory + 'single_d03_c' +
        #             str(channel_order_list[channel_to_compare]) +
        #             '_w' + str(window_width) +
        #             '_WF' + window_name +
        #             '.png')
        print(directory + 'single_d03_c' +
                    str(channel_order_list[channel_to_compare]) +
                    '_w' + str(window_width) +
                    '_WF' + window_name +
                    '.png')

        return 1

    def build_temperature_rmaj_single_plot_originals(self,
                                           temperature_original, channels_pos, time_list,
                                           channel_to_compare, channel_order_list):

        """ -----------------------------------------
            version: 0.1
            :return 1
        ----------------------------------------- """
        """
        Build single plot T(t) with fixed r_maj
        CAUTION: inverting plasma radius is near 48/49 channel (in ordered unit list)
        CAUTION: channel_to_check means temperature set, ordered by r_maj
        """

        fig, axes = plt.subplots()
        fig.set_size_inches(15, 8)

        axes.plot(
            # range(0, len(temperature_original[channel_to_compare])),
            time_list[channel_to_compare][0:len(temperature_original[channel_to_compare])],
            temperature_original[channel_to_compare]
        )

        axes.set(xlabel='Time (seconds)', ylabel='T (eV)',
                 title='Original signal, '
                       + str(channel_order_list[channel_to_compare]) + ' channel, 25 discharge, R_maj = '
                       + str(channels_pos[channel_to_compare]))
        axes.grid()

        # self.align_axes(axes)

        directory = 'results/originals/d25/' \
                    'o' + str(channel_to_compare) + \
                    '_c' + str(channel_order_list[channel_to_compare]) + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # fig.savefig(directory + 'single_d25_c' +
        #             str(channel_order_list[channel_to_compare]) +
        #             '.png')

        return 1

    def build_temperature_rmaj_series_plot(self, temperature_list, public_temperature_ordered_list, window_width, r_maj):
        """ -----------------------------------------
            version: 0.1
            :return 1
        ----------------------------------------- """
        """
        Build multiple plots T(r_maj)
        with various fixed time
        """

        fig, axes = plt.subplots()
        fig.set_size_inches(15, 7)

        # # # # # # # # # # # # # # # # # # # # # # # #
        for time, temperature in enumerate(np.transpose(temperature_list)):
            """ 
            Labeling each channel (in ordered range) 
            for T(R_maj) plot on the very beginning instant
            """
            if time == 0:
                labels = range(80)

                for label, x, y in zip(labels, r_maj[0:80], temperature[0:80]):
                    if label <= 23:
                        pos_offset = (-10, 10)
                    elif label in range(23, 50):
                        pos_offset = (10, 10)
                    else:
                        pos_offset = (-10, -10)

                    if label in range(0, 80, 2):
                        plt.annotate(
                            label,
                            xy=(x, y), xytext=pos_offset,
                            textcoords='offset points', ha='center', va='center',
                            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
                axes.plot(
                    r_maj[0:80],
                    # range(0, len(temperature[0:80])),
                    temperature[0:80]
                )

            if time in range(0, 4000, 100):
                axes.plot(
                    r_maj[0:80],
                    # range(0, len(temperature[0:80])),
                    temperature[0:80]
                )
        # # # # # # # # # # # # # # # # # # # # # # # #

        axes.set(ylabel='T (eV)', xlabel='R maj (m)',
                 title='Temperature changes inside toroid '
                       'in various time instants '
                       'with time smoothing, win. width ' + str(window_width))

        for item in ([axes.title, axes.xaxis.label, axes.yaxis.label] +
                     axes.get_xticklabels() + axes.get_yticklabels()):
            item.set_fontsize(17)

        axes.grid()

        # self.align_axes(axes)

        # directory = 'results/T_Rmaj/d25/'

        # if not os.path.exists(directory):
        #     os.makedirs(directory)
        #
        # fig.savefig(directory + 'd25_T_Rmaj_single_c0080_w' +
        #             str(window_width) + '_ti3500.png')

        return 1

    def info_losses_wind_func(self, **kwargs):
        """ -----------------------------------------
            version: 0.1
            :return 1
        ----------------------------------------- """
        """
        Compare all types of window function
        """

        temperature_original = kwargs['temperature_original']
        time = kwargs['time_list'][kwargs['channel_to_compare']]

        if temperature_original and type(temperature_original) is dict:
            temperature_original = self.processing.dict_to_list(temperature_original)

        sum_deviation = self.processing.calculate_deviation(
            kwargs['window_width'],
            temperature_original,
            kwargs['analyze_window'],
            kwargs['channel_to_compare'])

        """ Plot compare deviation """
        fig, axes = plt.subplots(2, 1)
        fig.set_size_inches(10, 8)

        y_pos = np.arange(len(kwargs['analyze_window']))

        axes[0].barh(y_pos, sum_deviation)
        axes[0].set_yticks(y_pos)
        axes[0].set_yticklabels(kwargs['analyze_window'])

        axes[0].set(xlabel='RMSD (eV)', ylabel='Window type',
                    title='RMSD, ' + str(kwargs['channel_order_list'][kwargs['channel_to_compare']])
                          + ' channel, 25 discharge, '
                            'wind. width ' + str(kwargs['window_width']) +
                          ', R_maj = ' + str(kwargs['channels_pos'][kwargs['channel_to_compare']]))
        axes[0].grid()
        axes[0].set_xlim(
            left=(min(sum_deviation) - min(sum_deviation) / 100),
            right=(max(sum_deviation) + min(sum_deviation) / 100))

        """ Plot compared T(t) """
        axes[1].plot(
            # range(0, len(temperature_original[kwargs['channel_to_compare'] - 1])),
            kwargs['time_list'][kwargs['channel_to_compare']],
            temperature_original[kwargs['channel_to_compare']]
        )

        custom_grid_time = [time[i] for i in range(len(time)) if (i % kwargs['window_width'] == 0)]

        axes[1].set_xticks(custom_grid_time, minor=True)
        axes[1].xaxis.grid(True, which='minor')

        axes[1].set(xlabel='Time (seconds)', ylabel='Temperature (eV)',
                    title='')

        # axes[1].grid()

        # self.align_axes(axes[0])
        # self.align_axes(axes[1])

        directory = 'results/RMSD/d25/' \
                    'o' + str(kwargs['channel_to_compare']) + \
                    '_c' + str(kwargs['channel_order_list'][kwargs['channel_to_compare']]) + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # fig.savefig(directory + 'RMSD_d25_c' +
        #             str(kwargs['channel_order_list'][kwargs['channel_to_compare']]) +
        #             '_w' + str(kwargs['window_width']) +
        #             '.png')
        return 1

    @staticmethod
    def align_axes(axes):
        """ -----------------------------------------
            version: 0.1
            :return 1
        ----------------------------------------- """
        label = axes.xaxis.get_label()
        x_lab_pos, y_lab_pos = label.get_position()
        label.set_position([1.0, y_lab_pos])
        label.set_horizontalalignment('right')

        label = axes.yaxis.get_label()
        x_lab_pos, y_lab_pos = label.get_position()
        label.set_position([x_lab_pos, .95])
        label.set_verticalalignment('top')

        return 1


class ViewOld(ViewData):

    def main_v1(self):
        channel_from = 1
        channel_to = 97
        window_width_val = 2
        public_window_width_val = 10
        window_func = 'triang'

        """ Parameters in which I interested """
        channel_to_compare = [2, 14, 23, 32, 45, 46, 48, 49, 50, 52, 60]
        window_to_compare = ['boxcar', 'triang', 'flattop']
        window_width_to_compare = [81, 200, 400]

        """ Extract data from MATLAB database """
        self.processing = dt.PreProfiling()
        data = dt.Profiling(discharge=25, channel=(channel_from, channel_to), source='real')
        data_public = dt.Profiling(discharge=25, channel=(channel_from, channel_to),
                                   source='public')
        # # # # # # # # # # # # # # # # # # # # # # # #

        """ Sort R_maj and time lists by R_maj value """
        r_maj = [channel[1] for channel in sorted(data.channels_pos.items(), key=itemgetter(1))]
        channel_order_list = {index: channel[0] for index, channel in enumerate(sorted(data.channels_pos.items(), key=itemgetter(1)))}
        time_list = [data.time_original[channel[1]] for channel in channel_order_list.items()]

        """ Ordering by R_maj """
        temperature_ordered_list = data.order_by_r_maj(
            data.temperature_original,
            channel_from, channel_to)
        public_temperature_ordered_list = data.order_by_r_maj(
            data_public.temperature_original,
            channel_from, channel_to)
        # # # # # # # # # # # # # # # # # # # # # # # #

        """ Calibrate """
        # calibrate_temperature_list = data.calibrate(
        #     temperature_ordered_list, public_temperature_ordered_list,
        #     window_width_val, public_window_width_val,
        #     channel_from, channel_to)
        calibrate_temperature_list = self.processing.list_to_dict(temperature_ordered_list)
        # # # # # # # # # # # # # # # # # # # # # # # #

        """
        CAUTION: for different channels losses could be VERY different
        so it would be preferable to check losses for each specific case

        Show difference, in RMSD, between
        original T(t) and smoothed, i.e., filtered T(t)
        with different window functions
        """
        # Multiple format
        # for channel, wind_w in itertools.product(channel_to_compare, window_width_to_compare):
        #     self.info_losses_wind_func(
        #         channels_pos=r_maj,
        #         window_width=wind_w,
        #         temperature_original=calibrate_temperature_list,
        #         analyze_window=data.win_list_names,
        #         channel_to_compare=channel,
        #         time_list=time_list,
        #         channel_order_list=channel_order_list)
        #
        # Original format
        # self.info_losses_wind_func(
        #     channels_pos=r_maj,
        #     window_width=window_width_val,
        #     temperature_original=calibrate_temperature_list,
        #     analyze_window=data.win_list_names,
        #     channel_to_compare=60,
        #     time_list=time_list,
        #     channel_order_list=channel_order_list)
        # # # # # # # # # # # # # # # # # # # # # # # #

        """
        Filtering T(t), i.e., smoothing
        triang          # minimum info save
        blackmanharris  # middle info save
        flattop         # maximum info save
        'boxcar', 'blackman', 'hamming', 'hann',
        'bartlett', 'parzen', 'bohman', 'nuttall', 'barthann'
        """
        temperature_list = self.processing.filter(
            calibrate_temperature_list, window_width_val, window_func)
        # # # # # # # # # # # # # # # # # # # # # # # #

        # self.build_filter_windows(data.win_list_names)

        """ Singe plot with one of window func """
        # Multiple format
        # for channel, wind, wind_w in itertools.product(channel_to_compare, window_to_compare, window_width_to_compare):
        #     temperature_list = self.processing.filter(
        #         calibrate_temperature_list, wind_w, wind)
        #
        #     self.build_temperature_rmaj_single_plot(
        #         temperature=temperature_list,
        #         temperature_original=calibrate_temperature_list,
        #         channels_pos=r_maj,
        #         window_width=wind_w,
        #         channel_to_compare=channel,
        #         time_list=time_list,
        #         channel_order_list=channel_order_list,
        #         window_name=wind)
        #
        # Multiple format
        # for channel in channel_to_compare:
        #     self.build_temperature_rmaj_single_plot_originals(
        #         temperature_original=calibrate_temperature_list,
        #         channels_pos=r_maj,
        #         channel_to_compare=channel,
        #         time_list=time_list,
        #         channel_order_list=channel_order_list)
        #
        # Original format
        # self.build_temperature_rmaj_single_plot(
        #     temperature=temperature_list,
        #     temperature_original=calibrate_temperature_list,
        #     channels_pos=r_maj,
        #     window_width=window_width_val,
        #     channel_to_compare=23,
        #     time_list=time_list,
        #     channel_order_list=channel_order_list,
        #     window_name=window_func)
        # # # # # # # # # # # # # # # # # # # # # # # #

        """ Filtering T(r_maj) WARNING: lose too many info """
        # temperature_list = self.processing.dict_to_list(temperature_list)
        # temperature_list_transpose = self.processing.list_to_dict(np.transpose(temperature_list))
        # temperature_list = self.processing.filter(temperature_list_transpose, 5, 'triang')
        # temperature_list = self.processing.dict_to_list(temperature_list)
        # temperature_list = self.processing.list_to_dict(np.transpose(temperature_list))
        # # # # # # # # # # # # # # # # # # # # # # # #

        temperature_list = self.processing.dict_to_list(temperature_list)

        # self.build_temperature_rmaj_series_plot(temperature_list, public_temperature_ordered_list,
        #                                         window_width_val, r_maj)
        self.build_temperature_rmaj_time_3d_surface(temperature_list, r_maj, time_list)

        plt.show()

