#!/usr/bin/env bash

mongosh DCMS_test -u DCM -p DCMS --authenticationDatabase admin --eval 'db.dropDatabase()'
mongosh DCMS_test -u DCM -p DCMS --authenticationDatabase admin --eval 'db.createCollection("users");db.createCollection("customers");db.createCollection("defaults");db.createCollection("rebirths");db.createCollection("fs.chunk");db.createCollection("fs.files")'
mongosh DCMS_test -u DCM -p DCMS --authenticationDatabase admin --eval '
    db.users.insertMany([
    {
        "_id": ObjectId("64a51ddc3d2d73f7be5eff30"),
        "认定人信息": {
            "姓名": "用于测试的认定人",
            "性别": "用于测试的性别",
            "年龄": 1000
        },
        "账号": "用于测试的账号",
        "密码": "用于测试的密码"
    }
    ]);
    db.customers.insertMany([
    {
        "_id": ObjectId("64a51ddc3d2d73f7be5eff30"),
        "姓名": "用于测试的客户",
        "年龄": 1000,
        "性别": "用于测试的性别",
        "联系方式": "用于测试的联系方式",
        "区域": "用于测试的区域",
        "行业": "用于测试的行业",
        "外部等级": "用于测试的外部等级",
        "当前状态": "用于测试的当前状态"
    },
    ]);
    db.defaults.insertMany([
    {
        "_id": ObjectId("64a51ddc3d2d73f7be5eff30"),
        "客户信息": {
            "客户id": ObjectId("64a51ddc3d2d73f7be5eff30"),
            "外部等级": "用于测试的外部等级",
            "当前状态": "用于测试的当前状态"
        },
        "违约原因": "用于测试的违约原因",
        "是否启用": false,
        "严重性": "用于测试的严重性",
        "认定人信息": {
            "认定人id": ObjectId("64a51ddc3d2d73f7be5eff30"),
            "认定人姓名": "用于测试的认定人"
        },
        "申请时间": "3099-07-01T12:00:00",
        "审核状态": "待审核",
        "审核时间": null
    },
    ]);
    db.rebirths.insertMany([
    {
        "_id": ObjectId("64a51ddc3d2d73f7be5eff30"),
        "违约信息": {
            "违约id": ObjectId("64a51ddc3d2d73f7be5eff30"),
            "违约原因": "用于测试的违约原因",
            "认定人姓名": "用于测试的认定人"
        },
        "申请时间": "3099-07-01T12:00:00",
        "重生原因": "用于测试的重生原因",
        "审核状态": "待审核",
        "审核时间": null
    },
    {
        "_id": ObjectId("64a51ddc3d2d73f7be5eff31"),
        "违约信息": {
            "违约id": ObjectId("64a51ddc3d2d73f7be5eff30"),
            "违约原因": "用于测试的违约原因",
            "认定人姓名": "用于测试的认定人"
        },
        "申请时间": "3099-07-01T12:00:00",
        "重生原因": "用于测试的重生原因",
        "审核状态": "待审核",
        "审核时间": null
    },
    ]);
'