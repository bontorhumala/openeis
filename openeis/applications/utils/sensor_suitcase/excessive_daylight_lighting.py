"""
Copyright (c) 2014, The Regents of the University of California, Department
of Energy contract-operators of the Lawrence Berkeley National Laboratory.
All rights reserved.

1. Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are met:

   (a) Redistributions of source code must retain the copyright notice, this
   list of conditions and the following disclaimer.

   (b) Redistributions in binary form must reproduce the copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

   (c) Neither the name of the University of California, Lawrence Berkeley
   National Laboratory, U.S. Dept. of Energy nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

2. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
   ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
   (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
   LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
   ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
   THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

3. You are under no obligation whatsoever to provide any bug fixes, patches,
   or upgrades to the features, functionality or performance of the source code
   ("Enhancements") to anyone; however, if you choose to make your Enhancements
   available either publicly, or directly to Lawrence Berkeley National
   Laboratory, without imposing a separate written license agreement for such
   Enhancements, then you hereby grant the following license: a non-exclusive,
   royalty-free perpetual license to install, use, modify, prepare derivative
   works, incorporate into other computer software, distribute, and sublicense
   such enhancements or derivative works thereof, in binary and source code
   form.

NOTE: This license corresponds to the "revised BSD" or "3-clause BSD" license
and includes the following modification: Paragraph 3. has been added.
"""


import datetime

def excessive_daylight(light_data, operational_hours, area, elec_cost):
    """
    Excessive Daylight checks to see a single sensor should be flagged.
    Parameters:
        - light_data: a 2d array with datetime and data
            - lights are on (1) or off (0)
            - assumes light_data is only for operational hours
        - operational_hours: building's operational in hours a day
        - elec_cost: The electricity cost used to calculate savings.
    Returns: True or False (true meaning that this sensor should be flagged)
    """
    # Grabs the first time it starts logging so we know when the next day is
    first_time = light_data[0][0]
    # counts times when lights go from on to off
    on_to_off = 0
    # counts the seconds when the lights are on
    time_on = datetime.timedelta(0)
    # counts flagged days
    day_flag = 0
    # counts the total number of days
    day_count = 0

    # accounts for the first point, checks if the lights are on, sets when
    # lights were last set to on to the first time
    if (light_data[0][1] == 1):
        lights_on = True
        last_on = first_time
    else:
        lights_on = False

    # iterate through the light data
    i = 1
    while (i < len(light_data)):
        # check if it's a new day
        if (light_data[i][0].time() == first_time.time()):
            # check if it should be flagged, time delta is in seconds so / 3600
            # to get hours
            if (light_data[i][1] == 1):
                time_on += (light_data[i][0] - last_on)
            # turn days into hours to be compared to operational hours per day
            if (time_on.days != 0):
                time_on_hours = (24 * time_on.days) + time_on.seconds/3600
            else:
                time_on_hours = time_on.seconds/3600
            if ((on_to_off < 2) and \
                    ((time_on_hours / operational_hours) > 0.5)):
                day_flag += 1
            day_count += 1
        # check lights were turned off, if so, increment on_to_off, lights
        # are now off, add time on to timeOn
        if ((lights_on) and (light_data[i][1] == 0)):
            on_to_off += 1
            lights_on = False
            time_on += (light_data[i][0] - last_on)
        # check if lights were turned on, set last_On to the current time
        elif ((not lights_on) and (light_data[i][1] == 1)):
            on = True
            last_On = light_data[i][0]
        i += 1

    # if more than half of the days are flagged, there's a problem.
    if (day_flag / day_count > 0.5):
        percent_l, percent_h, percent_c, med_num_op_hrs, per_hea_coo, \
                 percent_HVe = get_CBECS(area)
        total_time = light_data[len(light_data - 1)][0] - first_time
        total_weeks = ((total_time.days * 24) + (total_time.seconds / 3600)) \
                / 168
        avg_week = ((total_time.days * 24) + (total_time.seconds / 3600)) \
                / total_weeks
        return {
            'Problem': "Excessive lighting during occupied/daytime hours.",
            'Diagnostic': "Even though these spaces are not continuously \
                    occupied, for more than half of the monitoring period, the \
                    lights were switched off less than three times a day.",
            'Recommendation': "Install occupancy sensors in locations with \
                    intermittent occupancy, or engage occupants to turn the \
                    lights off when they leave the area.",
            'Savings': elec_cost * percent_l * 0.6 * 0.1 * \
                            (avg_week/med_num_op_hrs)
        }
    else:
        return False
