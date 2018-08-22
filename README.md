Scan engines
=====================

Scan engines server + client. Based on RabbitMQ. 

# How to install server + client

- Setup RabbitMQ (or use `docker-compose up`).
- Recomended use venv or virtualenv for better isolation.\
  Venv setup example: \
  `python3 -m venv myenv`\
  `source myenv/bin/activate`
- If it need - setup server's `env` file in `tasks_server`. By default workers count for server=5,
  source path is `<parent dir for server>/source`, dist path `<parent dir for server>/files_storage`, 
  rabbit host is localhost(for server and client too)/
  env file description:
  1) `SOURCE_PATH` - path, from which server getting files for scan.
  2) `DIST_PATH` - path, where the server will place the downloaded files.
  3) `WORKERS_COUNT` - workers count for server.
  4) `RABBIT_HOST` - host for RabbitMQ. *Attention* 
  If you want run server and client on different hosts - please make `export RABBIT_HOST=<rabbit host>` on client side!
  If you configured `env` file - `source env` from `tasks_server`.
  For current time server support only local source storage for files.
- `pip3 install -r requirements.txt`

    
# How to use (Local example)

- Run RabbitMQ (if you use docker `docker-compose up`)
- Run Server `python3 tasks_server/server.py`
- Put files for check in `SOURCE_PATH`
- Client side description:
   Client support argparse. Arguments:
   1) `-f` or `--files` - Select files for scan. Required. Multiple files supported. Example `-f test.txt file.py example.json`
   2) `-e` or `--engines` - Select engines for scan. Multiple engines supported. Example `-e enginea EngineB engineC`
   3) `-s` or `--save` - Set this arg if you need to save results in txt file. Pass here path to folder, where client can create files. 
   File name format: `<ENGINE_NAME> <DATE>.txt` Non required. Example `-s /Users/user/scan/logs/`. 
   4) `-c` or `--clear` - Delete files after check from service path. Default value - False. Non required. Example `-c`.
   Full example with all args `python3 tasks_client/sender.py -c -s /Users/user/scan/logs/ -f test.txt example.json -e enginea EngineB engineC`

 
