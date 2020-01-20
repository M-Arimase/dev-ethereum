#!/bin/bash

export GOROOT=/usr/local/go
export GOPATH=/root
export PATH=/usr/local/go/bin:/root/1806-ethereum/build/bin:$PATH

cd /root/1806-ethereum
git reset --hard
git pull

cd /root

datadir='/root/data-ethereum'
genesis='/root/dev-ethereum/genesis.json'
networkid='1806'
bootnode='enode://efdd65ad5419e2f7d6a53d65d72b0189cef1f89beab2b5f8860f3e48a63fd108843254759c5ba4e226a66f7d8cf51323d1f05e0e929b45e4b87372411fc4938a@172.17.0.8:30301'
extip=$(/sbin/ifconfig -a | grep inet | grep -v 127.0.0.1 | awk '{print $2}')

cmd="nohup geth --datadir $datadir init $genesis &"
echo $cmd
nohup geth --datadir $datadir init $genesis &

cmd="nohup geth --datadir $datadir --networkid $networkid --bootnodes $bootnode --nat "extip:$extip" &"
echo $cmd
nohup geth --datadir $datadir --networkid $networkid --bootnodes $bootnode --nat "extip:$extip" &
