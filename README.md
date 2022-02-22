# Catalyst 9K Thousand Eyes Deployment
Use Nornir and scapli_netconf to automate deployment of Thousand Eyes Enterprise agents on Catalyst 9K switches.

## Setup
1. Add hosts to the nornir_data/hosts.yaml inventory file
2. Identify groups and set platform, connection options, nameservers, and TE token in the nornir_data/groups.yaml inventory file
3. Set NETCONF credentials in the nornir_data/defaults.yaml file

## Use
If using poetry:
```
poetry install
poetry run python run.py
```
If using pip:
```
pip install -r requirements.txt
python run.py
```

## Tools
1. Nornir
2. Scrapli
3. Jinja
4. NAPALM
5. Poetry
6. Yang Suite
7. IOS-XE on Catalyst 9300
8. DevNet Sandbox