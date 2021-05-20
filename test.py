#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/5/20 10:05
# @Author  : AsiHacker
# @File    : test.py
# @Software: PyCharm
# @notice  : True masters always have the heart of an apprentice.
from chia.cmds.my_keys_funcs import generate_and_add, show_all_keys, keychain
from sqlalchemy import Column, String, create_engine, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()
# 初始化数据库连接:
engine = create_engine(
    'mysql+pymysql://jishubu:Nantian@NS2020@rm-t4n0rbu63u50cs5mvzo.mysql.singapore.rds.aliyuncs.com/fb_data')
# 创建DBSession类型:
Session = sessionmaker(bind=engine)
session = Session()


# 定义User对象:
class Wallet(Base):
    __tablename__ = 'wallet'

    id = Column(BigInteger, primary_key=True)
    fingerprint = Column(String(32, 'utf8mb4_general_ci'), nullable=False, unique=True)
    mnemonic = Column(String(255, 'utf8mb4_general_ci'), nullable=False)
    address = Column(String(255, 'utf8mb4_general_ci'), nullable=False)
    master = Column(String(255, 'utf8mb4_general_ci'), nullable=False)
    farmer = Column(String(255, 'utf8mb4_general_ci'), nullable=False)
    pool = Column(String(255, 'utf8mb4_general_ci'), nullable=False)


def generate():
    # from .init_funcs import check_keys

    generate_and_add()
    # check_keys(ctx.obj["root_path"])


def show():
    return show_all_keys(True)


def to_db_and_clear():
    """
    入库并且清理
    """
    keys = show_all_keys(True)
    new_list = []
    for key in keys:
        new_list.append(Wallet(**key))
    session.add_all(new_list)  # 这个插入相对比较慢，小量插入可以使用,插入后有new_list[0].id
    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    delete_all()


def delete_all():
    keychain.delete_all_keys()


if __name__ == '__main__':
    from tqdm import tqdm
    jdt = tqdm(range(100000))
    for _ in jdt:
        generate()
        to_db_and_clear()
    # delete_all()
