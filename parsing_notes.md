# Mirai C2 message parsing notes

## Example message
```
           00 22 00 00 01 2C 03 01 29 39 51 19 20 02 0C 01 31 19 0F 3235352E3235352E3235352E323535"
     00 00 00 22 00 00 0E 10 03 01 29 39 51 00 1A 02 0C 01 31 19 0F 3235352E3235352E3235352E323535"
     00 00 00 22 00 00 07 08 03 01 29 39 51 00 1A 02 0C 01 31 19 0F 3235352E3235352E3235352E323535"
                |           |  |  |           |  |     |  |     |  |
      0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 -
     PONG | LEN | duration  |AV|TC| Target IP |MK|OC|OP|OL|OV|OP|OL|OV
```

## Legend
```
AV - Attack vector
TC - Target count
MK - IP netmask
OC - Options count
OP - Option type
OL - Option value length
OV - Option value
```

## Parsed
```
(duration=300, atk_vec='SYN', targets=[Target(IP='41.57.81.25', mask=32)], opts=[Options(var=12, val_len=1, val="b'1'"), Options(var=25, val_len=15, val="b'255.255.255.255'")])
(duration=3600, atk_vec='SYN', targets=[Target(IP='41.57.81.0', mask=26)], opts=[Options(var=12, val_len=1, val="b'1'"), Options(var=25, val_len=15, val="b'255.255.255.255'")])
(duration=1800, atk_vec='SYN', targets=[Target(IP='41.57.81.0', mask=26)], opts=[Options(var=12, val_len=1, val="b'1'"), Options(var=25, val_len=15, val="b'255.255.255.255'")])
```
