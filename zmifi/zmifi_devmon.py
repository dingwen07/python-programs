from zmifi import zmifi
import time

l = zmifi('192.168.21.1', 'admin', 'password', login=True)
old_dev_data = l.device_data()

while True:
    time.sleep(30)
    new_dev_data = l.device_data()
    newconn_devices = []
    for new_device in new_dev_data['known_devices_list']:
        flag = True
        for old_device in old_dev_data['known_devices_list']:
            if new_device['mac'] == old_device['mac']:
                flag = False
        if flag:
            newconn_devices.append(new_device)
    disconn_devices = []
    for old_device in old_dev_data['known_devices_list']:
        flag = True
        for new_device in new_dev_data['known_devices_list']:
            if old_device['mac'] == new_device['mac']:
                flag = False
        if flag:
            disconn_devices.append(old_device)
    if len(newconn_devices) > 0:
        print('CONNECTED:')
        print(newconn_devices)
    if len(disconn_devices) > 0:
        print('DISCONNECTED:')
        print(disconn_devices)
    old_dev_data = new_dev_data
