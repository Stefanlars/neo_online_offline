import requests
import json
from datetime import datetime
import insightly

my_headers = {
    'Authorization': 'Basic ZWFiOTY2NTYtNDU5NS00NDNjLWIzOTktMzgzNTVjM2E3MGQxOg==',
    'Content-Type': 'application/json',
    'Cookie': 'snaptid=sac1prdc01wut07'
}


def grab_opp(opp_id):

    url = f"https://api.insightly.com/v3.1/Opportunities/{opp_id}"
    node_data = requests.request('GET', url, headers=my_headers).json()
    return node_data


def move_node_data(opp_id_1, opp_id_2):
    opp_id_1 = int(opp_id_1)
    opp_id_2 = int(opp_id_2)
    node_1 = grab_opp(opp_id_1)
    # node_2 = grab_opp(opp_id_2)
    # org_id = node_1['OPPORTUNITY_ID']
    raw_custom_fields = node_1['CUSTOMFIELDS']
    tags = node_1['TAGS']
    links = node_1['LINKS']

    new_custom_fields = []
    for item in raw_custom_fields:
        if item['FIELD_NAME'] == 'Account__c':
            print('test')
            pass
        elif item['FIELD_NAME'] == 'Explorer_Link__c':
            pass
        elif item['FIELD_NAME'] == 'Hardware_1__c':
            pass
        elif item['FIELD_NAME'] == 'MAC_ID__c':
            pass
        elif item['FIELD_NAME'] == 'MN_Number__c':
            pass
        else:
            new_custom_fields.append(item)

    payload = json.dumps({
        "OPPORTUNITY_ID": opp_id_2,
        "CUSTOMFIELDS": new_custom_fields
    })
    # print(links)
    # print(payload)
    update_node = requests.request(
        "PUT",
        url="https://api.na1.insightly.com/v3.1/Opportunities",
        headers=my_headers,
        data=payload
    )
    print(update_node)
    for item in links:
        if item['LINK_OBJECT_NAME'] == 'Contact':
            contact_id = item['LINK_OBJECT_ID']
            payload = json.dumps({
                'DETAILS': None,
                'ROLE': 'Host',
                'OBJECT_NAME': 'Opportunity',
                'OBJECT_ID': opp_id_2,
                'LINK_OBJECT_NAME': 'Contact',
                'LINK_OBJECT_ID': contact_id
            })
            url = f'https://api.insightly.com/v3.1/Opportunities/{opp_id_2}/Links'
            r = requests.request('POST', url, data=payload, headers=my_headers)
            print(r, 'contact')
        elif item['LINK_OBJECT_NAME'] == 'Organisation':
            org_id = item['LINK_OBJECT_ID']
            payload = json.dumps({
                'DETAILS': None,
                'ROLE': None,
                'OBJECT_NAME': 'Opportunity',
                'OBJECT_ID': opp_id_2,
                'LINK_OBJECT_NAME': 'Organisation',
                'LINK_OBJECT_ID': org_id
            })
            url = f'https://api.insightly.com/v3.1/Opportunities/{opp_id_2}/Links'
            r = requests.request('POST', url, data=payload, headers=my_headers)
            print(r, 'org')
    node_2 = grab_opp(opp_id_2)
    tags2 = node_2['TAGS']

    #DELETES EXISTING TAGS FROM NODE 2 THEN ADDS THE TAGS FROM NODE1

    for item in tags2:
        insightly.del_tag(item['TAG_NAME'], opp_id_2)
    for item in tags:
        tag_name = item['TAG_NAME']
        insightly.post_tag(tag_name=tag_name, oppor_id=opp_id_2)

    print("Data successfully transferred!! Now deleting data from Old Node......")
    # Deletes the links
    for item in links:
        link_id = item['LINK_ID']
        url = f'https://api.insightly.com/v3.1/Opportunities/{opp_id_1}/Links/{link_id}'
        delete_link = requests.request('DELETE', url=url, headers=my_headers)
        print(delete_link, 'delete link')
    # Deletes the tags
    for item in tags:
        insightly.del_tag(item['TAG_NAME'], opp_id_1)

    print('Tags successfully deleted')

    # TODO: Create function to delete all changeable info

    payload = json.dumps({
        'OPPORTUNITY_ID': opp_id_1,
        'CUSTOMFIELDS' : [
            {'FIELD_NAME': 'Antenna_Type__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Antenna_Type__c'},
            {'FIELD_NAME': 'City__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'City__c'},
            {'FIELD_NAME': 'Connectivity__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Connectivity__c'},
            {'FIELD_NAME': 'Direction__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Direction__c'},
            {'FIELD_NAME': 'Floor__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Floor__c'},
            {'FIELD_NAME': 'Height_Ft__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Height_Ft__c'},
            {'FIELD_NAME': 'Host__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Host__c'},
            {'FIELD_NAME': 'Host__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Host__c'},
            {'FIELD_NAME': 'Installer__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Installer__c'},
            {'FIELD_NAME': 'Internet_Service_Provider__c', 'FIELD_VALUE': 'Ozarks-go',
             'CUSTOM_FIELD_ID': 'Internet_Service_Provider__c'},
            {'FIELD_NAME': 'ISP_Speed__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'ISP_Speed__c'},
            {'FIELD_NAME': 'Location__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Location__c'},
            {'FIELD_NAME': 'Location_Type__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Location_Type__c'},
            {'FIELD_NAME': 'Location_Type_C__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Location_Type_C__c'},
            {'FIELD_NAME': 'Node_Level__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Node_Level__c'},
            {'FIELD_NAME': 'Node_Status__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Node_Status__c'},
            {'FIELD_NAME': 'Payment_ID_1__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Payment_ID_1__c'},
            {'FIELD_NAME': 'Payment_Method_1__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Payment_Method_1__c'},
            {'FIELD_NAME': 'Property__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Property__c'},
            {'FIELD_NAME': 'RouterModem__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'RouterModem__c'},
            {'FIELD_NAME': 'Service_Contact__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'Service_Contact__c'},
            {'FIELD_NAME': 'State__c', 'FIELD_VALUE': None, 'CUSTOM_FIELD_ID': 'State__c'},
            {'FIELD_NAME': 'Street_Address__c', 'FIELD_VALUE': None,
             'CUSTOM_FIELD_ID': 'Street_Address__c'},
        ]
    })
    update_node = requests.request(
        "PUT",
        url="https://api.na1.insightly.com/v3.1/Opportunities",
        headers=my_headers,
        data=payload
    )
    print(update_node)

    print('Info swap complete!!!!')


move_node_data('34152875', '34238370')


# opp_id = 34152776
# url = f'https://api.insightly.com/v3.1/Opportunities/{opp_id}/Links'
# payload = json.dumps({
#   'DETAILS': None,
#   'ROLE': 'Host',
#   'OBJECT_NAME': 'Opportunity',
#   'OBJECT_ID': 34152776,
#   'LINK_OBJECT_NAME': 'Contact',
#   'LINK_OBJECT_ID': 337702012
# })
# r = requests.request('POST', url, data=payload, headers=my_headers)

#

def put_opp_fields(opp_id,node_status):
  url = "https://api.na1.insightly.com/v3.1/Opportunities"
  id_int = int(opp_id)
  payload = json.dumps({
    "OPPORTUNITY_ID": id_int,
    "CUSTOMFIELDS": [
      {
        "FIELD_NAME": "City__c",
        "FIELD_VALUE": node_status,
        "CUSTOM_FIELD_ID": "City__c"
      }
    ]
  })
  headers = {
    'Authorization': 'Basic ZWFiOTY2NTYtNDU5NS00NDNjLWIzOTktMzgzNTVjM2E3MGQxOg==',
    'Content-Type': 'application/json',
    'Cookie': 'snaptid=sac1prdc01wut07'
  }

  response = requests.request("PUT", url, headers=headers, data=payload)




# url = "https://api.na1.insightly.com/v3.1/Opportunities"
# id_int = int('32803983')
# payload = json.dumps({
# "OPPORTUNITY_ID": id_int,
# "CUSTOMFIELDS": [
#     {
#         "FIELD_NAME": "RouterModem__c",
#         "FIELD_VALUE": "Next to back window. TEST TEXT",
#         "CUSTOM_FIELD_ID": "RouterModem__c"
#     }
#   ]
# })
# headers = {
# 'Authorization': 'Basic ZWFiOTY2NTYtNDU5NS00NDNjLWIzOTktMzgzNTVjM2E3MGQxOg==',
# 'Content-Type': 'application/json',
# 'Cookie': 'snaptid=sac1prdc01wut07'
# }
#
# response = requests.request("PUT", url, headers=headers, data=payload)
# print(response)