import json
import queue
import requests
requests.packages.urllib3.disable_warnings()
 
class AwvsScan(object):
    def __init__(self):
        self.scanner = 'https://172.16.0.13:3443'   #Modify URL
        self.api = '1986ad8c0a5b3df4d7028d5f3c06e936c18af8a8998154d1c8bb4d9c40573f477'  #Modify API
        self.ScanMode = '11111111-1111-1111-1111-111111111111'  #ScanMode
        self.headers = {'X-Auth': self.api, 'content-type': 'application/json'}
        self.targets_id = queue.Queue()
        self.scan_id = queue.Queue()
        self.site = queue.Queue()
 
    def main(self):
        print(' ______                                   ____              __           __         ')
        print('/\  _  \                                 /\  _`\           /\ \__       /\ \        ')
        print('\ \ \L\ \  __  __  __  __  __    ____    \ \ \L\ \     __  \ \ ,_\   ___\ \ \___    ')
        print(" \ \  __ \/\ \/\ \/\ \/\ \/\ \  /',__\    \ \  _ <'  /'__`\ \ \ \/  /'___\ \  _ `\  ")
        print("  \ \ \/\ \ \ \_/ \_/ \ \ \_/ |/\__, `\    \ \ \L\ \/\ \L\.\_\ \ \_/\ \__/\ \ \ \ \ ")
        print('''   \ \_\ \_\ \___x___/'\ \___/ \/\____/     \ \____/\ \__/.\_\\ \__\ \____\\ \_\ \_\ ''')
        print('    \/_/\/_/\/__//__/   \/__/   \/___/       \/___/  \/__/\/_/ \/__/\/____/ \/_/\/_/')
        print('              ______                                     __      ')
        print('             /\__  _\                                   /\ \__   ')
        print('             \/_/\ \/     ___ ___   _____     ___   _ __\ \ ,_\  ')
        print("                \ \ \   /' __` __`\/\ '__`\  / __`\/\`'__\ \ \/  ")
        print('                 \_\ \__/\ \/\ \/\ \ \ \L\ \/\ \L\ \ \ \/ \ \ \_ ')
        print('                 /\_____\ \_\ \_\ \_\ \ ,__/\ \____/\ \_\  \ \__\ ')
        print('                 \/_____/\/_/\/_/\/_/\ \ \/  \/___/  \/_/   \/__/')
        print('                                      \ \_\                      ')
        print('                                       \/_/                      ')
        print('='*80)
        print('Github：https://github.com/BetterDefender/AwvsBatchImport.git')
        print('Author：BetterDefender')
        print('')
        print("""1、Add scan task using awvs.txt\n2、Delete all tasks""")
        print('='*80)
        choice = input(">")
        if choice == '1':
            self.scans()
        if choice == '2':
            self.del_targets()
        self.main()
 
    def openfile(self):
        with open('awvs.txt') as cent:
            for web_site in cent:
                web_site = web_site.strip('\n\r')
                self.site.put(web_site)
 
    def targets(self):
        self.openfile()
        while not self.site.empty():
            website = self.site.get()
            try:
                data = {'address':website,
                        'description':'awvs-auto',
                        'criticality':'10'}
                response = requests.post(self.scanner + '/api/v1/targets', data=json.dumps(data), headers=self.headers, verify=False)
                cent = json.loads(response.content)
                target_id = cent['target_id']
                self.targets_id.put(target_id)
            except Exception as e:
                print('Target is not website! {}'.format(website))
 
    def scans(self):
        self.targets()
        while not self.targets_id.empty():
            data = {'target_id' : self.targets_id.get(),
                    'profile_id' : self.ScanMode,
                    'schedule' : {'disable': False, 'start_date': None, 'time_sensitive' : False}}
 
            response = requests.post(self.scanner + '/api/v1/scans', data=json.dumps(data), headers=self.headers, allow_redirects=False, verify=False)
            if response.status_code == 201:
                cent = response.headers['Location'].replace('/api/v1/scans/','')
                print(cent)
 
    def get_targets_id(self):
        response = requests.get(self.scanner + "/api/v1/targets", headers=self.headers, verify=False)
        content = json.loads(response.content)
        for cent in content['targets']:
            self.targets_id.put([cent['address'],cent['target_id']])
 
    def del_targets(self):
        while True:
            self.get_targets_id()
            if self.targets_id.qsize() == 0:
                break
            else:
                while not self.targets_id.empty():
                    targets_info = self.targets_id.get()
                    response = requests.delete(self.scanner + "/api/v1/targets/" + targets_info[1], headers=self.headers, verify=False)
                    if response.status_code == 204:
                        print('delete targets {}'.format(targets_info[0]))
 
if __name__ == '__main__':
    Scan = AwvsScan()
    Scan.main()
