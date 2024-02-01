#!/usr/bin/env bash

mongod --config /etc/mongod.conf --fork

sleep 5
mongosh admin --eval 'db.createUser({ user: "root", pwd: "mongodb", roles: ["root"] })'
mongosh admin -u root -p mongodb --authenticationDatabase admin --eval 'db.createUser({ user: "DCM", pwd: "DCMS", roles: [{role:"dbOwner",db:"DCMS"},{role:"dbOwner",db:"DCMS_test"}]})'
mongosh DCMS -u DCM -p DCMS --authenticationDatabase admin --eval 'db.createCollection("users");db.createCollection("customers");db.createCollection("defaults");db.createCollection("rebirths");db.createCollection("fs.chunk");db.createCollection("fs.files")'
mongosh DCMS -u DCM -p DCMS --authenticationDatabase admin --eval '
    db.users.insertMany([
    {
        "认定人信息": {
            "姓名": "沈彰",
            "性别": "男"
        },
        "账号": "user1",
        "密码": "password1"
    },
    {
        "认定人信息": {
            "姓名": "沈月",
            "年龄": 35
        },
        "账号": "user2",
        "密码": "password2"
    },
    {
        "认定人信息": {
            "姓名": "张昊",
            "性别": "男"
        },
        "账号": "user3",
        "密码": "password3"
    },
    {
        "认定人信息": {
            "姓名": "张静",
            "年龄": 42
        },
        "账号": "user4",
        "密码": "password4"
    },
    {
        "认定人信息": {
            "姓名": "陈晨",
            "性别": "女",
            "年龄": 28
        },
        "账号": "user5",
        "密码": "password5"
    },
    ]);
'

mongod --shutdown
mongod --config /etc/mongod.conf