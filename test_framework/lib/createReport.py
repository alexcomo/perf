# -*- coding: utf-8 -*-
import sys, os
import pickle

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from bokeh.plotting import figure
from bokeh.io import output_file, show, vplot
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from connection import *


class Graphs:
    def __init__(self, log_directory):
        self.log_directory = log_directory

    def table(self, data, name, builds):
        values = []
        for i in range(len(data)):
            temp_list = []
            for j in range(2,len(data[i])):
                temp_list.append(data[i][j])
            values.append(temp_list)
        if name == 'Battery usage (%)'or name == 'Battery temp.':
            col = ["Max", "Min", "Diff"]
        else:
            col = ["Max", "Min", "Average"]
        data_tab = dict(
            data=col,
            value1=values[0],
            value2=values[1] if len(values) >= 2 else ['-', '-', '-'],
            value3=values[2] if len(values) >= 3 else ['-', '-', '-'],
            value4=values[3] if len(values) >= 4 else ['-', '-', '-'],
            value5=values[4] if len(values) == 5 else ['-', '-', '-'],
        )
        source = ColumnDataSource(data_tab)
        columns = [
            TableColumn(field="data", title=name),
            TableColumn(field="value1", title="Build: %s" % builds[0]),
            TableColumn(field="value2", title="Build: %s" % builds[1] if len(builds) >= 2 else 'No build'),
            TableColumn(field="value3", title="Build: %s" % builds[1] if len(builds) >= 3 else 'No build'),
            TableColumn(field="value4", title="Build: %s" % builds[1] if len(builds) >= 4 else 'No build'),
            TableColumn(field="value5", title="Build: %s" % builds[1] if len(builds) == 5 else 'No build'),
        ]
        data_table = DataTable(source=source, columns=columns, width=650, height=175)
        return data_table

    def graph(self, data, name, devicename, build, legend=None, color=None):
        values = []
        for i in range(len(data)):
            temp_list = []
            for j in range(0, 2):
                temp_list.append(data[i][j])
            values.append(temp_list)

        tools = 'box_zoom,crosshair,reset'
        hover = HoverTool(tooltips=[(name, '$y'), ('Time (sec)', '$x'), ])
        p = figure(plot_width=1000, plot_height=400, title=name + ' - Build: ' + build[0] + ' - ' + devicename[0], logo=None,
                   tools=[hover, tools])

        if isinstance(values[0][0][0], list):
            for i in range(0, len(values[0][0])):
                p.line(values[0][1], values[0][0][i], line_width=2, color=color[i], legend=legend[i])
        else:
            p.line(values[0][1], values[0][0], line_width=2, color='red')

        p.title_text_color = "olive"
        p.title_text_font = "times"

        p.xaxis.axis_label = "Time line (sec)"
        p.xaxis.axis_label_text_color = "olive"

        p.yaxis.axis_label = name
        p.yaxis.axis_label_text_color = "olive"
        return p


    def events_table(self, events, name_events):
        data = dict(data=events[0][0], downloads=events[0][1],)
        source = ColumnDataSource(data)
        columns = [TableColumn(field="data", title=name_events),TableColumn(field="downloads", title="Number"),]
        data_table = DataTable(source=source, columns=columns, width=400, height=280)
        return data_table

    def last_report(self):
        device_dir = self.log_directory
        self.folder = Folders().all_subdirs_of(device_dir)
        self.devicename = []
        self.build = []
        memory = []
        cpu = []
        bat_usage = []
        bat_temp = []
        data_usage = []
        events = []
        if len(self.folder) < 5:
            rng = len(self.folder)
        else:
            rng = 5
        for i in range(0, rng):
            report_filename = self.folder[i][0] + "/" + Config().reportFilename
            try:
                with open(report_filename, 'rb') as f:
                    obj = pickle.load(f)
                    f.close()
                    self.devicename.append(obj[0])
                    self.build.append(obj[1])
                    memory.append(obj[2])
                    cpu.append(obj[3])
                    bat_usage.append(obj[4])
                    bat_temp.append(obj[5])
                    data_usage.append(obj[6])
                    events.append(obj[7])
            except IOError:
                print('cannot open %s' % Config().reportFilename)
        name_freemem = 'Free Memory (kB)'
        freemem_table = self.table(memory, name_freemem, self.build)
        freemem_graph = self.graph(memory, name_freemem, self.devicename, self.build)

        name_cpu = 'CPU usage(%)'
        cpu_table = self.table(cpu, name_cpu, self.build)
        cpu_graph = self.graph(cpu, name_cpu, self.devicename, self.build)

        name_bat = 'Battery usage (%)'
        name_temp = 'Battery temp.'
        bat_table = self.table(bat_usage, name_bat, self.build)
        temp_table = self.table(bat_temp, name_temp, self.build)
        bat_graph = self.graph(bat_usage, name_bat, self.devicename, self.build)
        temp_graph = self.graph(bat_temp, name_temp, self.devicename, self.build)

        name_data = 'Data usage'
        data_graph = self.graph(data_usage, name_data, self.devicename, self.build, ['background_rx', 'background_tx', 'foreground_rx',
                    'foreground_tx'], ['red', 'blue', 'green', 'black'])

        name_events = 'Events'
        events_table = self.events_table(events, name_events)

        return freemem_graph, freemem_table, cpu_graph, cpu_table, bat_graph, bat_table, temp_graph, temp_table, data_graph, events_table

    def start(self):
        freemem_graph, freemem_table, cpu_graph, cpu_table, bat_graph, bat_table, temp_graph, temp_table, data_graph, events_table = self.last_report()
        graph = vplot(events_table, freemem_graph, freemem_table, cpu_graph, cpu_table, bat_graph, bat_table, temp_graph, temp_table, data_graph)
        s = self.folder[0][0] + '/' + 'report_%s.html' % self.build[0].replace('.', '_')
        output_file(s, title=self.build[0] + '-' + self.devicename[0] + 'Report')
        return show(graph)
