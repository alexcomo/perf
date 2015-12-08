import os, datetime, json


class Config:
    def __init__(self):
        self.config_dir = 'config'
        f_config = open(self.config_dir).read()
        self.pars_json = json.loads(f_config)
        # OutputFiles settings
        self.memFilename = self.pars_json['outputFiles'][0]['memFilename']
        self.cpuFilename = self.pars_json['outputFiles'][0]['cpuFilename']
        self.btyFilename = self.pars_json['outputFiles'][0]['btyFilename']
        self.dtuFilename = self.pars_json['outputFiles'][0]['dtuFilename']
        self.reportFilename = self.pars_json['outputFiles'][0]['reportFilename']

        # Global settings
        self.reportFolder = self.pars_json['reportFolder']
        self.package = self.pars_json['package']
        self.adb = self.pars_json['adb']
        self.devices = self.pars_json['devices']
        self.apk = self.pars_json['apk']
        self.startapp = self.pars_json['startapp']
        self.downloadLink = self.pars_json['downloadLink']
        self.events_dir_name = self.pars_json['events_dir_name']
        self.events_list = self.pars_json['events_list']

        self.memName = self.pars_json['usageInfo'][0]['procName']
        self.memAdb = self.pars_json['usageInfo'][0]['adbCommand']

        self.cpuName = self.pars_json['usageInfo'][1]['procName']
        self.cpuAdb = self.pars_json['usageInfo'][1]['adbCommand']

        self.batName = self.pars_json['usageInfo'][2]['procName']
        self.batAdb = self.pars_json['usageInfo'][2]['adbCommand']

        self.dataName = self.pars_json['usageInfo'][3]['procName']
        self.dataAdb = self.pars_json['usageInfo'][3]['adbCommand']

        self.logName = self.pars_json['usageInfo'][4]['procName']
        self.logAdb = self.pars_json['usageInfo'][4]['adbCommand']
        # ADB Shell commands
        self.device_manufacture = self.pars_json['adbShell'][0]['device_manufacture']
        self.device_model = self.pars_json['adbShell'][0]['device_model']
        self.android_build = self.pars_json['adbShell'][0]['android_build']


# class Devices:
#     def __init__(self):
#         self.devises_dir = "devices"
#         f_devises = open(self.devises_dir).read()
#         self.pars_json = json.loads(f_devises)
#
#         # TODO: Add switcher between devices
#         # Phone settings
#         self.totalDevices = self.pars_json['totalDevices']
#         self.device = self.pars_json['devices'][0]['device']
#         self.ip = self.pars_json['devices'][0]['ip']
#         self.port = self.pars_json['devices'][0]['port']
#         self.duration = float(self.pars_json['duration'])


class Folders:
    def __init__(self):
        pass


    def folders_creation(self, build, device):
        device_dir = Config().reportFolder + device
        dir_name = build + '_' + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d_%H-%M')
        report_dir = device_dir + '/' + dir_name
        if not os.path.exists(Config().reportFolder):
            os.mkdir(Config().reportFolder)
        if not os.path.exists(device_dir):
            os.mkdir(device_dir)
        if not os.path.exists(report_dir):
            os.mkdir(report_dir)
        return report_dir


    def events_folders_creation(self, log_directory):
        events_dir = log_directory + "/" + Config().events_dir_name
        if not os.path.exists(events_dir):
            os.mkdir(events_dir)
        return events_dir

    def all_subdirs_of(self, report_folder):
        b = report_folder
        result = []
        for d in os.listdir(b):
            bd = os.path.join(b, d)
            if os.path.isdir(bd):
                result.append([bd, os.path.getctime(bd)])
        result = sorted(result, key=lambda st: st[1], reverse=True)
        return result