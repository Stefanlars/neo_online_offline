import time
import requests
import re
import paramiko
from paramiko import SSHClient
import insightly

def check_node_peerbook(node_list):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname='137.184.151.218', port=22, username='root', password='WidePutin2015s')

    for item in node_list:
        helium_id = item['info']['helium_id']
        opp_id = item['info']['opp_id']
        name = item['info']['name']
        r = requests.request(
            'GET', url=f'https://api.helium.io/v1/hotspots/{helium_id}'
        )
        helium_data = f"{r.json()}"
        helium_re = re.search('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/tcp/(\d{5})', helium_data)
        try:
            ip_address = helium_re.group(1)
            port = helium_re.group(2)
            stdin, stdout, stderr = client.exec_command(f"telnet {ip_address} {port}")
            telnet_response = f'{stdout.readlines()}'
            # print(telnet_response)
            client.exec_command("^C")
            telnet_re = re.search('(Connected)', telnet_response)

            if telnet_re.group(1) == "Connected":
                print(f"{name} is online and unchanged")
        except:
            print(f"Unable to connect to {name} via ip address, trying p2p network...")
            client.exec_command(
                f"docker exec miner miner peer ping /p2p/{helium_id}"
            )
            stdin, stdout, stderr = client.exec_command(
                f"docker exec miner miner peer book /p2p/{helium_id}"
            )

            peer_book_look = (f"{stdout.readlines()}")
            peer_book_fail_re = re.search("( failed)", peer_book_look)
            try:
                if peer_book_fail_re.group(1) == ' failed':
                    insightly.put_opp_fields(opp_id=opp_id, node_status='offline')
                    insightly.del_tag(oppor_id=opp_id, tag_name='Online')
                    insightly.post_tag(oppor_id=opp_id, tag_name='Offline')
                    insightly.add_note(opp_id=opp_id, node_status='offline', node_type='rak')
                    print(f"\n!!!!{name} is offline and changed in insightly!!!!\n")
                    # f = open('output.txt', 'a')
                    # f.write(f'\n!!!{name} is offline and is updated in insightly!!!')
                    # f.close()
            except:
                print(f"{name} is online and unchanged in insightly")
def check_hotspot(helium_url):
    id_re = re.compile('(https://explorer.helium.com/hotspots/)(.+)')
    helium_id = f"{id_re.search(helium_url).group(2)}"
    helium_r= requests.get(f"https://api.helium.io/v1/hotspots/{helium_id}")
    time.sleep(1)
    hotspot_data = helium_r.json()
    if hotspot_data['data']['status']['online'] == 'offline':
        return 'offline'
    if hotspot_data['data']['status']['online'] == 'online':
        return 'online'

def verify_nodes():
    start_time = time.time()

    my_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Authorization' : 'Basic ZWFiOTY2NTY0NTk1NDQzY2IzOTkzODM1NWMzYTcwZDE6', 'Accept-Encoding': 'gzip','Cookie':
        'AWSALB=ZzLr88p2bX5pDMu+HciCYLfXzA+DkD052gLVUJitHSETUaEbbUjUr = 1U1L0kLLefonHdWZ6NV0Bu6Q9RN75LdEAaW+ebqBYSsgT/9YZleO9neezS5OuZ6tn4V8k/un; AWSALBCORS=ZzLr88p2bX5pDMu+HciCYLfXzA+DkD052gLVUJitHSETUaEbbUjU1U1L0kLLefonHdWZ6NV0Bu6Q9RN75LdEAaW+ebqBYSsgT/9YZleO9neezS5OuZ6tn4V8k/un; snaptid=sac1prdc01wut07',
        'Accept':'*/*','Connection':'keep-alive'}

    r = requests.get("https://api.insightly.com/v3.1/Opportunities/SearchByTag?tagName=Offline&brief=false&top=300&count_total=false", headers=my_headers)

    r2 = requests.get("https://api.insightly.com/v3.1/Opportunities/SearchByTag?tagName=Online&brief=false&top=300&count_total=false", headers=my_headers)

    Offline_nodes = r.json()

    Online_nodes = r2.json()

    online_list = []
    offline_list = []
    changed_list_online = []
    changed_list_offline= []
    offline_node_list = []
    offline_nebra = []
    num_offline = 0
    num_online = 0
    for item in Offline_nodes: num_offline = num_offline+1
    for item in Online_nodes: num_online = num_online+1

    for item in Offline_nodes:
        hotspot = item["OPPORTUNITY_NAME"]
        OPP_ID = item["OPPORTUNITY_ID"]
        print(f"{hotspot} is now being verified")
        hardware = ''
        for field in item['CUSTOMFIELDS']:
            if field['FIELD_VALUE']== 'Nebra Outdoor Unit':
                hardware = 'Nebra'
                node_dict1 = {}
                node_dict1['info'] = {'name': hotspot, 'opp_id': OPP_ID, 'helium_id': ''}
                offline_nebra.append(node_dict1)
            else:
                pass
        for field in item['CUSTOMFIELDS']:
            if field['FIELD_NAME']== 'Explorer_Link__c':
                hotspot_url=field['FIELD_VALUE']
                time.sleep(.7)


                try:
                    NODE_STATUS=check_hotspot(hotspot_url)
                except:
                    NODE_STATUS = 'offline'
    #TODO: 2/22/2022: IN PROGRESS: adding nebra function so that nebras are online and up to date
                if NODE_STATUS == 'online':
                    changed_list_online.append(f'{hotspot} is now online and updated in hotspotty')
                    insightly.put_opp_fields(opp_id=OPP_ID, node_status=NODE_STATUS)
                    insightly.del_tag(oppor_id=OPP_ID, tag_name='Offline')
                    insightly.post_tag(oppor_id=OPP_ID, tag_name='Online')
                    insightly.add_note(opp_id=OPP_ID, node_status=NODE_STATUS, node_type='rak')

                if NODE_STATUS == 'offline':
                    offline_list.append(f'{hotspot}')


            else:
                pass
    #
    # #TODO: online node update in insightly
    print("\nNow verifying online nodes.....")
    for item in Online_nodes:
        hotspot = item["OPPORTUNITY_NAME"]
        opp_id = item["OPPORTUNITY_ID"]
        print(f"{hotspot} is now being verified")
        for field in item['CUSTOMFIELDS']:
            if field['FIELD_NAME']== 'Explorer_Link__c':
                hotspot_url=field['FIELD_VALUE']
                time.sleep(.7)
                try:
                    node_status=check_hotspot(hotspot_url)
                except:
                    node_status = 'online'

                if node_status == 'online':
                    online_list.append(f'{hotspot}')
                if node_status == 'offline':
                    changed_list_offline.append(f'{hotspot}')
                    id_re = re.compile('(https://explorer.helium.com/hotspots/)(.+)')
                    helium_id = f"{id_re.search(hotspot_url).group(2)}"
                    node_dict = {}
                    node_dict['info'] = {'name':hotspot,'opp_id':opp_id,'helium_id':helium_id}
                    offline_node_list.append(node_dict)

            else:
                pass

    # check_node_peerbook(node_list=offline_node_list)

    print(changed_list_online)

    print("All nodes successfully verified in --- %s seconds ---" % (time.time() - start_time))
