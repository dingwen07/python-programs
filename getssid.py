import os

def get_ssid():
    wlan_intfa = os.popen('netsh wlan show interfaces').read()
    ssid_index = wlan_intfa.find('SSID')
    bssid_index = wlan_intfa.find('BSSID')
    ssid = wlan_intfa[ssid_index:bssid_index].split('\n')[0].split(':', 1)[1][1:]
    return ssid

if __name__ == "__main__":
    pass