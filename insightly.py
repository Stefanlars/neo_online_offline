import requests
import json
import re
from datetime import datetime
import paramiko
from paramiko import SSHClient
import time


def del_tag(tag_name, oppor_id,):

  url = f"https://api.na1.insightly.com/v3.1/Opportunities/{oppor_id}/Tags"

  payload = json.dumps({
    "TAG_NAME": f"{tag_name}"
  })
  headers = {
    'Authorization': 'Basic ZWFiOTY2NTYtNDU5NS00NDNjLWIzOTktMzgzNTVjM2E3MGQxOg==',
    'Content-Type': 'application/json',
    'Cookie': 'snaptid=sac1prdc01wut07'
  }

  response = requests.request(f"DELETE", url, headers=headers, data=payload)

  return response
#function for posting tags in an opportunity


def post_tag(tag_name, oppor_id):
  url = f"https://api.na1.insightly.com/v3.1/Opportunities/{oppor_id}/Tags"

  payload = json.dumps({
    "TAG_NAME": f"{tag_name}"
  })
  headers = {
    'Authorization': 'Basic ZWFiOTY2NTYtNDU5NS00NDNjLWIzOTktMzgzNTVjM2E3MGQxOg==',
    'Content-Type': 'application/json',
    'Cookie': 'snaptid=sac1prdc01wut07'
  }

  response = requests.request(f"POST", url, headers=headers, data=payload)


  return response


def add_note(opp_id, node_status, node_type):
  url = f"https://api.na1.insightly.com/v3.1/Opportunities/{opp_id}/Notes"
  if node_type == 'nebra':
    payload = json.dumps({
    "TITLE":f"Node Status:{node_status}",
    "BODY":f"Node {node_status} in Nebra Portal: {datetime.now()}"
    })
  else:
    payload = json.dumps({
      "TITLE": f"Node Status:{node_status}",
      "BODY": f"Node {node_status} in explorer: {datetime.now()}"
    })
  headers={
    'Authorization': 'Basic ZWFiOTY2NTYtNDU5NS00NDNjLWIzOTktMzgzNTVjM2E3MGQxOg==',
    'Content-Type': 'application/json',
    'Cookie': 'snaptid=sac1prdc01wut07'
  }
  response = requests.request("POST", url, headers=headers, data=payload)

def put_opp_fields(opp_id,node_status):
  url = "https://api.na1.insightly.com/v3.1/Opportunities"
  id_int = int(opp_id)
  payload = json.dumps({
    "OPPORTUNITY_ID": id_int,
    "CUSTOMFIELDS": [
      {
        "FIELD_NAME": "Node_Status__c",
        "FIELD_VALUE": node_status,
        "CUSTOM_FIELD_ID": "Node_Status__c"
      }
    ]
  })
  headers = {
    'Authorization': 'Basic ZWFiOTY2NTYtNDU5NS00NDNjLWIzOTktMzgzNTVjM2E3MGQxOg==',
    'Content-Type': 'application/json',
    'Cookie': 'snaptid=sac1prdc01wut07'
  }

  response = requests.request("PUT", url, headers=headers, data=payload)


def hotspots_data():
    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Authorization': 'Basic ZWFiOTY2NTY0NTk1NDQzY2IzOTkzODM1NWMzYTcwZDE6', 'Accept-Encoding': 'gzip', 'Cookie':
            'AWSALB=ZzLr88p2bX5pDMu+HciCYLfXzA+DkD052gLVUJitHSETUaEbbUjUr = 1U1L0kLLefonHdWZ6NV0Bu6Q9RN75LdEAaW+ebqBYSsgT/9YZleO9neezS5OuZ6tn4V8k/un; AWSALBCORS=ZzLr88p2bX5pDMu+HciCYLfXzA+DkD052gLVUJitHSETUaEbbUjU1U1L0kLLefonHdWZ6NV0Bu6Q9RN75LdEAaW+ebqBYSsgT/9YZleO9neezS5OuZ6tn4V8k/un; snaptid=sac1prdc01wut07',
        'Accept': '*/*', 'Connection': 'keep-alive'}

    r = requests.get(
        "https://api.insightly.com/v3.1/Opportunities/SearchByTag?tagName=Offline&brief=false&top=300&count_total=false",
        headers=my_headers)

    r2 = requests.get(
        "https://api.insightly.com/v3.1/Opportunities/SearchByTag?tagName=Online&brief=false&top=300&count_total=false",
        headers=my_headers)

    offline_node_data = r.json()
    online_node_data = r2.json()

    node_list = []

    for item in offline_node_data:
        helium_address = ''
        node_status = ''
        city = ''
        hardware = ''
        wallet = ''
        level = ''
        name = item['OPPORTUNITY_NAME']
        opp_id = item['OPPORTUNITY_ID']
        for field in item['CUSTOMFIELDS']:
            if field['FIELD_NAME'] == 'Explorer_Link__c':
                id_re = re.compile('(https://explorer.helium.com/hotspots/)(.+)')
                explorer_link = field['FIELD_VALUE']
                helium_address = f"{id_re.search(explorer_link).group(2)}"
            # if field['FIELD_NAME'] == 'Node_Status__c':
            #     node_status = field['FIELD_VALUE']
            if field['FIELD_NAME'] == 'Account__c':
                wallet = field['FIELD_VALUE']
            if field['FIELD_NAME'] == 'City__c':
                city = field['FIELD_VALUE']
            if field['FIELD_NAME'] == 'Hardware_1__c':
                hardware = field['FIELD_VALUE']
            if field['FIELD_NAME'] == 'Node_Level__c':
                level = field['FIELD_VALUE']
            else:
                pass
            for tag in item['TAGS']:
                if tag['TAG_NAME'] == 'Offline':
                    node_status = 'Offline'
                if tag['TAG_NAME'] == 'offline':
                    node_status = 'offline'
                else:
                    pass
        node_list.append({
                    'name': name, 'address': helium_address, 'status': node_status, 'city': city, 'hardware': hardware,
                    'wallet': wallet, 'level': level, 'opp_id': opp_id
                            })

    for item in online_node_data:
        helium_address = ''
        node_status = ''
        city = ''
        hardware = ''
        wallet = ''
        level = ''
        name = item['OPPORTUNITY_NAME']
        opp_id = item['OPPORTUNITY_ID']
        for field in item['CUSTOMFIELDS']:
            if field['FIELD_NAME'] == 'Explorer_Link__c':
                id_re = re.compile('(https://explorer.helium.com/hotspots/)(.+)')
                explorer_link = field['FIELD_VALUE']
                helium_address = f"{id_re.search(explorer_link).group(2)}"
            # if field['FIELD_NAME'] == 'Node_Status__c':
            #     node_status = field['FIELD_VALUE']
            if field['FIELD_NAME'] == 'Account__c':
                wallet = field['FIELD_VALUE']
            if field['FIELD_NAME'] == 'City__c':
                city = field['FIELD_VALUE']
            if field['FIELD_NAME'] == 'Hardware_1__c':
                hardware = field['FIELD_VALUE']
            if field['FIELD_NAME'] == 'Node_Level__c':
                level = field['FIELD_VALUE']
            else:
                pass
            for tag in item['TAGS']:
                if tag['TAG_NAME'] == 'Online':
                    node_status = 'Online'
                if tag['TAG_NAME'] == 'online':
                    node_status = 'Online'
                else:
                    pass
        node_list.append({
                    'name': name, 'address': helium_address, 'status': node_status, 'city': city, 'hardware': hardware,
                    'wallet': wallet, 'level': level, 'opp_id': opp_id
                            })

    # hotspotData = pd.DataFrame(node_list)
    # print((training_set_df))
    # print(len(node_list))
    return node_list


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
                    put_opp_fields(opp_id=opp_id, node_status='offline')
                    del_tag(oppor_id=opp_id, tag_name='Online')
                    post_tag(oppor_id=opp_id, tag_name='Offline')
                    add_note(opp_id=opp_id, node_status='offline', node_type='rak')
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
                    node_status=check_hotspot(hotspot_url)
                except:
                    node_status = 'offline'
    #TODO: 2/22/2022: IN PROGRESS: adding nebra function so that nebras are online and up to date
                if node_status == 'online':
                    changed_list_online.append(f'{hotspot} is now online and updated in hotspotty')
                    put_opp_fields(opp_id=OPP_ID, node_status=node_status)
                    del_tag(oppor_id=OPP_ID, tag_name='Offline')
                    post_tag(oppor_id=OPP_ID, tag_name='Online')
                    add_note(opp_id=OPP_ID, node_status=node_status, node_type='rak')

                if node_status == 'offline':
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
                    node_dict = {'info': {'name': hotspot, 'opp_id': opp_id, 'helium_id': helium_id}}
                    offline_node_list.append(node_dict)

            else:
                pass

    check_node_peerbook(node_list=offline_node_list)

    print(changed_list_online)

    print("All nodes successfully verified in --- %s seconds ---" % (time.time() - start_time))

def offline_hotspot_data():
    my_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, '
                                'like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                  'Authorization': 'Basic ZWFiOTY2NTY0NTk1NDQzY2IzOTkzODM1NWMzYTcwZDE6', 'Accept-Encoding': 'gzip',
                  'Cookie':
                      'AWSALB=ZzLr88p2bX5pDMu+HciCYLfXzA+DkD052gLVUJitHSETUaEbbUjUr = '
                      '1U1L0kLLefonHdWZ6NV0Bu6Q9RN75LdEAaW+ebqBYSsgT/9YZleO9neezS5OuZ6tn4V8k/un; '
                      'AWSALBCORS=ZzLr88p2bX5pDMu+HciCYLfXzA+DkD052gLVUJitHSETUaEbbUjU1U1L0kLLefonHdWZ6NV0Bu6Q9RN75LdEAaW'
                      '+ebqBYSsgT/9YZleO9neezS5OuZ6tn4V8k/un; snaptid=sac1prdc01wut07',
                  'Accept': '*/*', 'Connection': 'keep-alive'}
    r = requests.get(
        "https://api.insightly.com/v3.1/Opportunities/SearchByTag?tagName=Offline&brief=false&top=300&count_total=false",
        headers=my_headers)
    offline_node_data = r.json()
    node_list = []
    for item in offline_node_data:
        helium_address = ''
        node_status = ''
        city = ''
        hardware = ''
        wallet = ''
        level = ''
        name = item['OPPORTUNITY_NAME']
        opp_id = item['OPPORTUNITY_ID']
        for field in item['CUSTOMFIELDS']:
            if field['FIELD_NAME'] == 'Explorer_Link__c':
                id_re = re.compile('(https://explorer.helium.com/hotspots/)(.+)')
                explorer_link = field['FIELD_VALUE']
                helium_address = f"{id_re.search(explorer_link).group(2)}"
            # if field['FIELD_NAME'] == 'Node_Status__c':
            #     node_status = field['FIELD_VALUE']
            if field['FIELD_NAME'] == 'Account__c':
                wallet = field['FIELD_VALUE']
            if field['FIELD_NAME'] == 'City__c':
                city = field['FIELD_VALUE']
            if field['FIELD_NAME'] == 'Hardware_1__c':
                hardware = field['FIELD_VALUE']
            if field['FIELD_NAME'] == 'Node_Level__c':
                level = field['FIELD_VALUE']
            else:
                pass
            for tag in item['TAGS']:
                if tag['TAG_NAME'] == 'Offline':
                    node_status = 'Offline'
                if tag['TAG_NAME'] == 'offline':
                    node_status = 'offline'
                else:
                    pass
        node_list.append({
                    'name': name, 'address': helium_address, 'status': node_status, 'city': city, 'hardware': hardware,
                    'wallet': wallet, 'level': level, 'opp_id': opp_id
                            })
    return node_list


#TODO: function needs to grab only the latest offline note. I think converting to epoch then comparing then back to conventional format
# is the best way to do this. This function will determine how long node has been offline

def neo_offline_report():
    my_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, '
                               'like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                  'Authorization': 'Basic ZWFiOTY2NTY0NTk1NDQzY2IzOTkzODM1NWMzYTcwZDE6', 'Accept-Encoding': 'gzip',
                  'Cookie':
                  'AWSALB=ZzLr88p2bX5pDMu+HciCYLfXzA+DkD052gLVUJitHSETUaEbbUjUr = '
                  '1U1L0kLLefonHdWZ6NV0Bu6Q9RN75LdEAaW+ebqBYSsgT/9YZleO9neezS5OuZ6tn4V8k/un; '
                  'AWSALBCORS=ZzLr88p2bX5pDMu+HciCYLfXzA+DkD052gLVUJitHSETUaEbbUjU1U1L0kLLefonHdWZ6NV0Bu6Q9RN75LdEAaW'
                  '+ebqBYSsgT/9YZleO9neezS5OuZ6tn4V8k/un; snaptid=sac1prdc01wut07',
                  'Accept': '*/*','Connection':'keep-alive'}
    node_list = offline_hotspot_data()
    offline_nodes = []
    for item in node_list:
        level = item['level']
        name = item['name']
        status = item['status']
        address = item['status']
        opp_id = f'{item["opp_id"]}'
        explorer_url = f"https://explorer.helium.com/hotspots/{address}"
        url = f'https://api.insightly.com/v3.1/Opportunities/{opp_id}/Notes?brief=false&count_total=false'
        response = requests.request('GET', url, headers=my_headers).json()
        # print(name)
        offline_time_list = []
        try:
            for note in response:
                if note['TITLE'].lower() == 'node status:offline':
                    year = int(re.search(pattern=r'(\d\d\d\d)-(\d\d)-(\d\d)', string=note['DATE_CREATED_UTC']).group(1))
                    month = int(re.search(pattern=r'(\d\d\d\d)-(\d\d)-(\d\d)', string=note['DATE_CREATED_UTC']).group(2))
                    day = int(re.search(pattern=r'(\d\d\d\d)-(\d\d)-(\d\d)', string=note['DATE_CREATED_UTC']).group(3))
                    offline_time_list.append(datetime(year, month, day, 0, 0).timestamp())
                if note['TITLE'].lower() == 'node status: offline':
                    year = int(re.search(pattern=r'(\d\d\d\d)-(\d\d)-(\d\d)', string=note['DATE_CREATED_UTC']).group(1))
                    month = int(re.search(pattern=r'(\d\d\d\d)-(\d\d)-(\d\d)', string=note['DATE_CREATED_UTC']).group(2))
                    day = int(re.search(pattern=r'(\d\d\d\d)-(\d\d)-(\d\d)', string=note['DATE_CREATED_UTC']).group(3))
                    offline_time_list.append(datetime(year, month, day, 0, 0).timestamp())
                if note['TITLE'].lower() == 'node status - offline':
                    year = int(re.search(pattern=r'(\d\d\d\d)-(\d\d)-(\d\d)', string=note['DATE_CREATED_UTC']).group(1))
                    month = int(re.search(pattern=r'(\d\d\d\d)-(\d\d)-(\d\d)', string=note['DATE_CREATED_UTC']).group(2))
                    day = int(re.search(pattern=r'(\d\d\d\d)-(\d\d)-(\d\d)', string=note['DATE_CREATED_UTC']).group(3))
                    offline_time_list.append(datetime(year, month, day, 0, 0).timestamp())
            offline_date = datetime.fromtimestamp(max(offline_time_list)).strftime("%Y/%m/%d")
        except ValueError:
            offline_date = 'N/A'
        offline_nodes.append({'name': name, 'address': address, 'offline_time': offline_date})
    return offline_nodes


