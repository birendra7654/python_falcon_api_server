Documentation
===
    JDBE.Take2 diaries

    May 17, 2016 11:22:00
    Create an interim git checkin

    May 10, 2016 21:10:00
    Opened the project


FIxed
===
    Parental Control fix[201605072151]
    To Load Profile
        python loadProfiles.py ProductProfile.csv LogisticsProfile.csv SubscriberProfile.csv SLP_relation.csv

    To Start JDBE
        python main.py start -c data/JDBE_local.ini --log debug

    EDIT JDBE.ini with corresponding details
    example JDBE.ini

    	[JDBE]
    	mongo_ip = 10.10.1.31
    	mongo_port = 27017
    	keystone_ip = 10.10.1.151
    	keystone_port = 5000
    	mysql_port = 3306
    	ldap_port = 389
    	JAip = 192.168.1.14
    	JAport = 8080

    	[keystone]
    	kusername = admin
    	kpassword = stack
    	ktenant_name = demo

    	[mail_password]
    	username = telenetnewpass@gmail.com
    	password = telenewpass


API list
===
    append with https://<JDBE_ip:JDBE_port>/
    JA
        - cmts discovery
        - cm discovery
        - cm state
        - cm stats

        /v0.9/cm-discovery
        /v0.9/cmts-discovery
        /v0.9/cm-state
        /v0.9/cm-stats

    Wifi
        - list of all access points under CMTS
            /v0.9/cmts/access-points/{mac_address}
    Popsite
        - create popsite - assign cmts to popsite
        - list of unassigned cmts
        - list of all popsite
        - list of cmts under popsite
        - list of cm under cmts
        - discovery log -- [popsite created, cm discovered, cmts discovered, cm stats added, cm state updated]

        /v0.9/popsite-create
        /v0.9/popsite/unassigned-cmts-list
        /v0.9/popsite/all-list
        /v0.9/popsite/cmts-list/{popsite_name}
        /v0.9/popsite/cm-list/{cmts_id}
        /v0.9/popsite/log

    Portals
        - docsis channel details of cm
        - device data of cm
        - access points details of cm
        - wifi peer details of cm
        - devices connected to access points of cm

        /v0.9/docsis-channel/{mac_address}
        /v0.9/device-meta/{mac_address}
        /v0.9/wifi-accesspoints/{mac_address}
        /v0.9/wifi-peers/{mac_address}
        /v0.9/wifi-devices/{mac_address}

    Reports
        - report on single metric between dates on given interval
        - list of metric in single api call
        /v0.9/reset-password
        /v0.9/update-password

    Meters
        - vservice meteric data
        /v0.9/vservice/meter/{meter_name}/{resource_id}  
        /v0.9/vservice/resources
        /v0.9/vservices/resources/{resource_id}

    Auth
        - authentication of services and users
        - creating different role
        /v0.9/auth/users
        /v0.9/auth/projects
        /v0.9/auth/roles     

ELASTICSEARCH CREATE INDEX
==========
curl -XPUT 10.10.1.230:9200/_template/template_1 -d '{
    "template": "sanctum-*",
    "settings": {
        "index.refresh_interval": "5s"
    },
    "mappings": {
        "_default_": {
            "_all": {
                "enabled": true
            },
            "dynamic_templates": [
                {
                    "string_fields": {
                        "match": "*",
                        "match_mapping_type": "string",
                        "mapping": {
                            "index": "not_analyzed",
                            "omit_norms": true,
                            "type": "string"
                        }
                    }
                }
            ]
            }
        }
}'



TD-AGENT
====
copy td-agent conf file data directory and past in /etc/td-agent/td-agent.conf file

loads.py file
=======
To load tunnel user, modify in subscriber.csv of data directory and run this script

python load.py -P data/ProductProfile.csv -L data/LogisticsProfile.csv -S SubscriberProfile.csv

JA CMTS assigned
======
python load.py -V data/CMtsJaAssign.csv  

Run Tests 
======
Make changes in tests/config.ini
Run:- python automate.py
Check tests/log_file.txt

NOTE:
===
	use lower case instead of upper case in log level type because ES does not support searching in upper case
