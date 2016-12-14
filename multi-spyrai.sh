#!/bin/bash

while read c; do
    ./spyrai $c 23 &
done<$1

