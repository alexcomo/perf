from soak import *


def test_case_hub2():
    real_time("Start Soak Test on Hub 2 and 3 at ")
    user_name = config['hub2and3_username']
    password = config['hub2and3_password']
    hub='hub2and3'
    # devices_connected_names()
    download_apk()
    print('START RESTART HUB 2 AND 3')
    Connection().kill_server()
    Connection().usb_off(sensor=2)
    Connection().usb_off(sensor=3)
    Connection().power_off(sensor=2)
    Connection().power_off(sensor=3)
    time.sleep(10)
    Connection().usb_on(sensor=2)
    Connection().usb_on(sensor=3)
    time.sleep(2)
    Connection().power_on(sensor=2)
    Connection().power_on(sensor=3)
    time.sleep(2)
    Connection().start_server()
    time.sleep(5)
    connect_all_devices(hub=hub)
    # devices_connected_names()
    print('All devices Uninstall app')
    all_devices_id(target=Connection().uninstall)
    print('All devices Install app')
    all_devices_id(target=Connection().install)
    time.sleep(5)
    all_devices_id(target=Connection().install)
    time.sleep(5)
    print('All devices Start Reboot')
    all_devices_id(target=reboot_device)
    print('All devices Rebooted')
    time.sleep(10)
    all_devices_id(target=open_port_5555)
    print('All devices tcpip 5555')
    time.sleep(5)
    print('All devices unlock')
    all_devices_id(target=unlock_device)
    time.sleep(5)
    all_devices_id(target=unlock_device)
    time.sleep(10)
    Connection().kill_server()
    time.sleep(1)
    Connection().usb_off(sensor=2)
    Connection().usb_off(sensor=3)
    time.sleep(2)
    Connection().power_off(sensor=2)
    Connection().power_off(sensor=3)
    time.sleep(2)
    Connection().start_server()
    time.sleep(5)
    print ('Connecting all devices over WiFi ...')
    connect_devices_wifi(hub=hub)
    time.sleep(5)
    multi_soak()
    time.sleep(20)
    Process(target=usb_and_power_on, args=((config['duration']*60+300), 2)).start()
    Process(target=usb_and_power_on, args=((config['duration']*60+310), 3)).start()
    Process(target=create_report, args=((config['duration']*60+200), hub)).start()
    all_devices_ip(target=start_app)
    all_devices_login(target=run_cut, user_name=user_name, password=password)
    exit_app_all_devices(times=2, delay=20)
    time.sleep(20)
    Process(target=exit_app_all_devices, args=(3, (config['duration']*55))).start()
    all_devices_ip(target=start_app)
    all_devices_ip(target=run_1hour_video)

if __name__ == "__main__":
    test_case_hub2()
