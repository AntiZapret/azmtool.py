azmtool.py
==========

Python tool to work with Antizapret/AntiZapret

#### Описание:
Утилита для работы со списком околоправительственных организаций. В качестве исходного файла используется список в формате json (blacklist4.json)

#### Возможности:
- Выгрузка ip адресов в формате **plain text**
- Выгрузка ip адресов в формате **p2p** для torrent клиентов
- Выгрузка ip адресов для добавления в **nginx** (403 Forbidden)
- Выгрузка ip адресов для добавления в **nginx** (404 Not Found)
- Выгрузка ip адресов для добавления в **iptables** (межсетевой экран Linux)

#### Пример:
```sh
python2 azmtool.py -h
python2 azmtool.py -o p2p > torrent_block.p2p
python2 azmtool.py -i custom_list.json -o iptables
```

#### Совместимость:
Протестировано на Python 2.7
