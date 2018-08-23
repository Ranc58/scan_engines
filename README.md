
Scan engines
=====================

Scan engines server + client. Based on RabbitMQ. 

# How to install server + client

- Setup RabbitMQ (or use `docker-compose up`).
- Recomended use venv or virtualenv for better isolation.\
  Venv setup example: \
  `python3 -m venv myenv`\
  `source myenv/bin/activate`
- `pip3 install -r requirements.txt`

    
# How to use (Local example)

- Run RabbitMQ (if you use docker `docker-compose up`)
- Server support argparse. Arguments: 
   - `-s` or `--source` - Path from which server getting files for scan. Non required. Default value `<parent dir for server>/source` \
   Example `-s /Users/user/scan/source_for_scan/`
   - `-d` or `--dist` - Path where the server will place the downloaded files. Non required. If path not exists - server will create it. Default value `<parent dir for server>/files_storage`. \
   Example `-d /Users/user/scan/storage/`
   - `-w` or `--workers` - Workers count for server. Non required. Default value `5`. \
   Example `-w 3`. 
   - `-r` or `--rabbit` - Set host for RabbitMQ. Non Required. Default value `localhost`.
   Example `-r 127.0.0.1`. \
   For run with default settings `python3 tasks_server/server.py`\
   Full example with all args:\
   `python3 tasks_server/server.py -s /Users/user/scan/source_for_scan/ -d /Users/user/scan/storage/ -w 3 -r 127.0.0.1`
- Client support argparse. Arguments:
   - `-f` or `--files` - Select files for scan. Required. Multiple files supported.\
   Example `-f test.txt file.py example.json`
   - `-e` or `--engines` - Select engines for scan. Required. Multiple engines supported. \
   Example `-e enginea EngineB engineC`
   - `-s` or `--save` - Set this arg if you need to save results in txt file. Pass here path to folder, where client can create files. File name format: `<ENGINE_NAME> <DATE>.txt`. Non required. \
   Example `-s /Users/user/scan/logs/`. 
   - `-c` or `--clear` - Delete files after check from service path. Default value - False. Non required. Example `-c`.\
   - `-r` or `--rabbit` - Set host for RabbitMQ. Non Required. Default value `localhost`.
   Full example with all args:\
   `python3 tasks_client/sender.py -c -s /Users/user/logs/ -f example.json -e enginea engineC`

Result example:
```
- ENGINEA:
h1.py scanned. Result: fa01cb65-bf8a-4d23-8e68-30b8f0ed7700
h2.py scanned. Result: 547243c4-2318-44c9-9d48-d80b809ddb7c
- ENGINEB:
{"h1.py": "baf9c930-de10-4f72-82e1-3e530e737a7f"}
{"h2.py": "179987bb-34c3-4435-a30c-c1b1ff9decc3"}
```
# Tests
For tests run `./run_tests.sh`
 
