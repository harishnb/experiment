# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 09:58:26 2018

@author: harisbha
"""

import pygal
import pandas as pd
from collections import defaultdict
from pygal.style import Style
from datetime import datetime
from flask import Flask


app = Flask(__name__)

var_screen_id_dict = defaultdict(list)

data_tf_idf = pd.read_csv('tf_idf_values.csv')
data_time_spent = pd.read_csv('time_spent.csv')
avg_time_spent = pd.read_csv('Avg_time_spent.csv')
var_full_data = pd.read_csv('data.csv')

def create_html_page():
    with open("stat_index.html", mode='w') as html:
        starting_lines = ["<!DOCTYPE html>",
                          '<html lang="en" dir="ltr">',
                          '<head>',
                          '<meta charset="utf-8">',
                          '<title>GUI Measurement</title>',
                          '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous">'
                          '</head>',
                          '<body>',
                          '<div class="container"> <h3>GUI Measurement</h3>',
                          '</div>',
                          '<div class="container">',
                          ]
        ending_lines = ['</div>',
                        '</body>',
                        '</html>',]
        html.writelines(starting_lines)
        body_lines = []
        body_lines.append('<h1 align="center">STB EPG screen Analytics</h1>')
        body_lines.append('<table><tr>')

#=====================================================================================================================
#***************************************** Table to Average uptime****************************************************
        body_lines.append('<td>')
        body_lines.append('<table><tr><th></th><th>Screen Id</th><th>Least used score</th></tr>')
        for idx in list(range(0,len(data_tf_idf))):
              body_lines.append('<tr><td>{}</td><td>{}  </td><td> {} </td></tr>'.format(idx+1, data_tf_idf.GUI[idx], data_tf_idf.Priority[idx]))
        body_lines.append('</table></td>')

# ****************************************** graph of least used screens***********************************
        body_lines.append('<td> <object type="image/svg+xml" data="static/images/tf_idf_chart.svg"> Your browser does not support SVG </object></td>')
        body_lines.append('</tr> </table>')
        body_lines.append('<td>')
        body_lines.append('<p>====================================================================================================================================================================================</p>')

#=====================================================================================================================
#***************************************** Table to Average uptime****************************************************
        body_lines.append('<table><tr><td>')
        body_lines.append('<table><tr><th>STB start Time </th><th> </th><th>STB End time </th><th> </th><th>STB UP time (In secs)</th></tr>')
        for idx1 in list(range(0,len(data_time_spent))):
            tmp_start_time = data_time_spent.Date_Time[idx1] - data_time_spent.Time_spent[idx1]
            var_start_time = datetime.utcfromtimestamp(int(tmp_start_time)).strftime('%Y-%m-%d %H:%M:%S')
            var_end_time = datetime.utcfromtimestamp(int(data_time_spent.Date_Time[idx1])).strftime('%Y-%m-%d %H:%M:%S')
            body_lines.append('<tr> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> </tr>'.format(var_start_time,"||",var_end_time," ===> ", data_time_spent.Time_spent[idx1]))
        body_lines.append('</table></td>')


#*************************************** Graph of Average uptime***********************************
        body_lines.append('<td> </td><td></td><td align="right" ><object type="image/svg+xml" data="static/images/bar_chart.svg" style="margin-top:10px; margin-left:100px;"> Your browser does not support SVG </object></td>')
        # body_lines.append('</tr></table>')
        # body_lines.append('<td>')
        # body_lines.append('<p>====================================================================================================================================================================================</p>')

#===================================================================================================================
#*************************************** Time series line chart ***********************************
        # body_lines.append('<td> </td><td></td><td align="right" ><object type="image/svg+xml" data="static/images/line_chart.svg" style="margin-top:10px; margin-left:100px;"> Your browser does not support SVG </object></td>')
        body_lines.append('</tr></table>')
        body_lines.append('<td>')
        body_lines.append('<p>====================================================================================================================================================================================</p>')

#********************************** Table of Average screen time***********************************
        body_lines.append('<table><tr><td>')
        body_lines.append('<table><tr><th>Screen ID </th><th> </th><th>Avg time (in secs)</th></tr>')
        for idx1 in list(range(0,len(avg_time_spent))):
            body_lines.append('<tr><td>{}</td><td>{}  </td><td> {} </td></tr>'.format(avg_time_spent.Screen_id[idx1],"         ",avg_time_spent.Avg_Time[idx1]))
        body_lines.append('</table></td>')

#********************************** Graph of Average screen time***********************************
        body_lines.append('<td> </td><td></td><td align="right"> <object type="image/svg+xml" data="static/images/screen_avg_chart.svg"> Your browser does not support SVG </object></td>')
        body_lines.append('</tr></table>')

#********************************** Statistics Average screen time***********************************
        var_data_frame = avg_time_spent.describe()
        var_col1 = []
        var_col2 = []
        for idx in var_data_frame.iterrows():
            var_col1.append(str(idx[0]))
            var_col2.append(str(round(idx[1][0],4)))


#***************************************** Doughnut Graph****************************************************
        body_lines.append('<table><tr><th>Statistics</th><th></th><th align="center">Values</th></tr>')
        for idx1 in list(range(0,len(var_col1))):
#            print (idx1,"-",var_col1[idx1],"-",var_col2[idx1])
            body_lines.append('<tr><td>{}</td><td>=</td><td align="center">{}</td></tr>'.format(var_col1[idx1],var_col2[idx1]))
        body_lines.append('</table></td>')
        body_lines.append('<object type="image/svg+xml" data="static/images/donut.svg" align="right"> Your browser does not support SVG </object>')
        body_lines.append('<p>====================================================================================================================================================================================</p>')

#********************************** Table of Screen Accessed pattern***********************************
        global var_screen_id_dict
        body_lines.append('<table><tr><td>')
        body_lines.append('<table><tr><th>Screen ID </th><th> </th><th>Set of screens Next entered</th><th>Total screens visited</th></tr>')
        for i in var_screen_id_dict:
            body_lines.append('<tr><td>{}</td>'.format(i))
            var_screen_set = []
            for j in var_screen_id_dict[i]:
                var_screen_set.append(j)

            ln = list(set(var_screen_set))

            body_lines.append('<td>{}</td><td align="left">{} </td><td>{}</td></tr>'.format("         ",ln,len(ln)))
        body_lines.append('</table></td>')

#=====================================================================================================================
#***************************************** Scatter plot sample****************************************************

#        body_lines.append('<td> </td><td></td><td> <object type="image/svg+xml" data="static/images/scatter.svg" align="right"> Your browser does not support SVG </object></td>')

#=====================================================================================================================
#***************************************** Write to HTML file****************************************************
        html.writelines(body_lines)
        html.writelines(ending_lines)

        html_lst = body_lines + ending_lines
        html_txt = ''.join(html_lst)
        return html_txt

#=====================================================================================================================
#***************************************** create_html_page **********************************************************
#=====================================================================================================================


@app.route("/")
def home():

#    print ("__xlabels__",var_x_labels)
#####################################Active session chart #####
    custom_style = Style(colors=('#351508', '#404040', '#9BC850'))
    title = 'STB Uptime'
    bar_chart = pygal.Bar(width=400, height=400,explicit_size=True, title=title,x_label_rotation=90,style=custom_style)
    var_x_labels = []
    var_data = []
    for idx1 in list(range(0,len(data_time_spent))):
        var_end_time = datetime.utcfromtimestamp(int(data_time_spent.Date_Time[idx1])).strftime('%Y-%m-%d %H:%M:%S')
        var_x_labels.append(var_end_time)
        var_data.append(data_time_spent.Time_spent[idx1])
#        print(data_time_spent.Time[idx1])

    bar_chart.x_labels = var_x_labels
    var_time_spent = var_data

    bar_chart.add('Active session time',var_time_spent)
    bar_chart.render_to_file('static/images/bar_chart.svg')
#####################################Active session line chart #####
    line_chart = pygal.Line()
    line_chart.title = 'Time series'
    # line_chart.x_labels = map(
    #     date.isoformat,
    #     rrule(DAILY, dtstart=date(2010, 8, 1), until=date.today())
    # )
    # line_chart.y_labels = map(str,range(1,25))
    var_date_series = []
    var_start_time_series = []
    var_end_time_series = []
    var_time_series_plot =[]
    for idx1 in list(range(0,len(data_time_spent))):
        tmp_start_time = data_time_spent.Date_Time[idx1] - data_time_spent.Time_spent[idx1]
        var_date_series.append(datetime.utcfromtimestamp(int(tmp_start_time)).strftime('%Y-%m-%d'))
        var_start_time_series.append(datetime.utcfromtimestamp(int(tmp_start_time)).strftime('%H:%M:%S'))
        var_end_time_series.append(datetime.utcfromtimestamp(int(data_time_spent.Date_Time[idx1])).strftime('%H:%M:%S'))
    line_chart.x_labels = var_date_series
    line_chart.x_labels = map(str, range(2002, 2013))
    print ("##########var date series####",var_date_series)
    print ("##########var start time series####",var_start_time_series)
    print ("##########var end time  series####",var_end_time_series)
    line_chart.add("start Time",[12,34,10,5,7])
    line_chart.add("End Time",[22,12,13,16,5])
    line_chart.render_to_file('static/images/line_chart.svg')

################################### Avg time spent chart #######
    title2 = 'Avg time spent on each screen'
    custom_style = Style(colors=('#059467','#9BC850','#E80080'))
    avg_bar_chart = pygal.Bar(width=1200, height=800,explicit_size=True, title=title2,x_label_rotation=70,style=custom_style)
    var_x_labels = []
    var_data = []
#    print ("__xlabels__",var_x_labels)
#    print ("avg time spent===",avg_time_spent)
    for idx1 in list(range(0,len(avg_time_spent))):
        var_x_labels.append(avg_time_spent.Screen_id[idx1])
        var_data.append(avg_time_spent.Avg_Time[idx1])
#        print(avg_time_spent.Avg_Time[idx1])

    avg_bar_chart.x_labels = var_x_labels
#    bar_chart.y_labels = var_y_labels
#    var_time_spent = [data_time_spent[x] for x in data_time_spent]
#    print ("_Time spent_",var_time_spent)
#    print ("_Time spent_0___",var_time_spent[0])
#    print ("_Time spent_1___",var_time_spent[1])
    var_time_spent = var_data
    avg_bar_chart.add('Avg time sec',var_data)
    avg_bar_chart.render_to_file('static/images/screen_avg_chart.svg')

###################################
    title2 = 'Least used screens'
    custom_style = Style(colors=('#1878f7','#404040','#E80080'))
    avg_bar_chart = pygal.Bar(width=1200, height=600,explicit_size=True, title=title2,x_label_rotation=90,style=custom_style)
    var_x_labels = []
    var_data = []
#    print ("__xlabels__",var_x_labels)

    for idx1 in list(range(0,len(data_tf_idf))):
        var_x_labels.append(data_tf_idf.GUI[idx1])
        var_data.append(data_tf_idf.Priority[idx1])
#        print(avg_time_spent.Avg_Time[idx1])

    avg_bar_chart.x_labels = var_x_labels
#    bar_chart.y_labels = var_y_labels
#    var_time_spent = [data_tf_idf[x] for x in data_tf_idf]
#    print ("_Time spent_",var_time_spent)
#    print ("_Time spent_0___",var_time_spent[0])
#    print ("_Time spent_1___",var_time_spent[1])
    var_time_spent = var_data
    avg_bar_chart.add('Least used screen',var_time_spent)
    avg_bar_chart.render_to_file('static/images/tf_idf_chart.svg')

#====================Donut chart of the screens used==================

    pie_chart = pygal.Pie(width=1200,height=600,explicit_size=True,inner_radius=.2)
    pie_chart.title = 'Time spent on each screen (in %)'
    var_x_labels = []
    var_data = []
    total_values = 0
    for idx1 in list(range(0,len(avg_time_spent))):
        total_values = total_values + avg_time_spent.Avg_Time[idx1]

#    print ("Total value===",total_values)
    for idx1 in list(range(0,len(avg_time_spent))):
        prcnt = round((avg_time_spent.Avg_Time[idx1]/total_values)*100,2)
#        print ("% = ",prcnt)
        pie_chart.add(avg_time_spent.Screen_id[idx1], prcnt)

    pie_chart.render_to_file('static/images/donut.svg')

#==================================Gauge chart==========
    gauge = pygal.SolidGauge(inner_radius=0.70)
    percent_formatter = lambda x: '{:.10g}%'.format(x)
    gauge.value_formatter = percent_formatter


#====Screen Pattern Table Info=====================================



    for idx in list(range(0,len(avg_time_spent))):
#        print (idx,"=>",avg_time_spent.Screen_id[idx])
        for idx2 in list(range(0,len(var_full_data))):
            if(avg_time_spent.Screen_id[idx]==var_full_data.ScreenName[idx2]):
#                print (idx2,"count=",var_full_data.ScreenName[idx2])
                if (idx2+1>=len(var_full_data)):
                    continue
                else:
                    var_screen_id_dict[avg_time_spent.Screen_id[idx]].append(var_full_data.ScreenName[idx2+1])
#                    print("screneid =",avg_time_spent.Screen_id[idx],"next id=",var_full_data.ScreenName[idx2+1])

#    print("The next screen list stored==========")
#    print (var_screen_id_dict)

#====scatter plot=====================================
#    xy_chart = pygal.XY(width=1200,height=600,explicit_size=True,stroke=False)
#    xy_chart.title = 'Scatter plot of the screen ID and time spent'
#    xy_chart.add('2', [(.1, .15), (.12, .23), (.4, .3), (.6, .4), (.21, .21), (.5, .3), (.6, .8), (.7, .8)])
#    xy_chart.add('3', [(.05, .01), (.13, .02), (1.5, 1.7), (1.52, 1.6), (1.8, 1.63), (1.5, 1.82), (1.7, 1.23), (2.1, 2.23), (2.3, 1.98)])
#    xy_chart.render_to_file('static/images/scatter.svg')

#======================================

    my_html = create_html_page()

    return my_html

#return html


#----------------------------------------------------------------------
if __name__ == '__main__':
    app.run()
