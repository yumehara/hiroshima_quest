# coding:utf-8
import gc
import numpy as np
import pandas as pd
import feather
import common

def preprocess():
    OUTPUT = common.BALL_2017

    train_pitch = pd.read_feather(common.TRAIN_PITCH)
    print(train_pitch.shape)

    train_pitch.rename(columns={'球種': 'ball', '投球位置区域': 'course'}, inplace=True)
    train_pitch['ball_cnt'] = train_pitch['プレイ前ストライク数'].astype(str) + '-' + train_pitch['プレイ前ボール数'].astype(str)

    train_pitch.replace('左', 'L', inplace=True)
    train_pitch.replace('右', 'R', inplace=True)
    train_pitch['pit_bat'] = train_pitch['投手投球左右'] + '_' + train_pitch['打者打席左右']

    # 球種
    train_ball_cnt = train_pitch[['ball', 'ball_cnt', 'pit_bat']].groupby(['ball_cnt', 'pit_bat', 'ball']).size()
    train_ball_cnt = pd.DataFrame(train_ball_cnt).reset_index()
    train_ball_cnt.rename(columns={0:'ball_sum'}, inplace=True)

    ball_total = train_ball_cnt.groupby(['ball_cnt', 'pit_bat']).sum().reset_index()
    ball_total.rename(columns={'ball_sum':'total'}, inplace=True)
    train_ball_cnt = train_ball_cnt.merge(ball_total[['ball_cnt', 'pit_bat', 'total']], on=['ball_cnt', 'pit_bat'], how='left')
    train_ball_cnt['rate'] = train_ball_cnt['ball_sum'] / train_ball_cnt['total']

    train_ball_pivot = pd.pivot_table(train_ball_cnt[['ball_cnt', 'pit_bat', 'ball', 'rate']], index=['ball_cnt', 'pit_bat'], columns='ball', values='rate').reset_index()
    train_ball_pivot.rename(columns={
        0: 'bc_straight', 
        1: 'bc_curve', 
        2: 'bc_slider', 
        3: 'bc_shoot', 
        4: 'bc_fork', 
        5: 'bc_changeup', 
        6: 'bc_sinker', 
        7: 'bc_cutball'
    }, inplace=True)

    train_ball_pivot.fillna(0, inplace=True)
    print(train_ball_pivot.shape)

    # コース
    train_course = train_pitch[['course', 'ball_cnt', 'pit_bat']].groupby(['ball_cnt', 'pit_bat', 'course']).size()
    train_course = pd.DataFrame(train_course).reset_index()
    train_course.rename(columns={0:'course_sum'}, inplace=True)

    course_total = train_course.groupby(['ball_cnt', 'pit_bat']).sum().reset_index()
    course_total.rename(columns={'course_sum':'total'}, inplace=True)
    train_course = train_course.merge(course_total[['ball_cnt', 'pit_bat', 'total']], on=['ball_cnt', 'pit_bat'], how='left')
    train_course['rate'] = train_course['course_sum'] / train_course['total']

    train_course_pivot = pd.pivot_table(train_course[['ball_cnt', 'pit_bat', 'course', 'rate']], index=['ball_cnt', 'pit_bat'], columns='course', values='rate').reset_index()
    train_course_pivot.rename(columns={
        0: 'bc_course_0', 
        1: 'bc_course_1', 
        2: 'bc_course_2', 
        3: 'bc_course_3', 
        4: 'bc_course_4', 
        5: 'bc_course_5', 
        6: 'bc_course_6', 
        7: 'bc_course_7', 
        8: 'bc_course_8', 
        9: 'bc_course_9', 
        10: 'bc_course_10', 
        11: 'bc_course_11', 
        12: 'bc_course_12'
    }, inplace=True)

    train_course_pivot.fillna(0, inplace=True)

    # コースの種類
    train_course_pivot['bc_high_str'] = train_course_pivot['bc_course_0'] + train_course_pivot['bc_course_3'] + train_course_pivot['bc_course_6'] 
    train_course_pivot['bc_high_ball'] = train_course_pivot['bc_course_9'] + train_course_pivot['bc_course_10'] 
    train_course_pivot['bc_mid_str'] = train_course_pivot['bc_course_1'] + train_course_pivot['bc_course_4'] + train_course_pivot['bc_course_7'] 
    train_course_pivot['bc_low_str'] = train_course_pivot['bc_course_2'] + train_course_pivot['bc_course_5'] + train_course_pivot['bc_course_8'] 
    train_course_pivot['bc_low_ball'] = train_course_pivot['bc_course_11'] + train_course_pivot['bc_course_12'] 
    train_course_pivot['bc_left_str'] = train_course_pivot['bc_course_0'] + train_course_pivot['bc_course_1'] + train_course_pivot['bc_course_2'] 
    train_course_pivot['bc_left_ball'] = train_course_pivot['bc_course_9'] + train_course_pivot['bc_course_11'] 
    train_course_pivot['bc_center_str'] = train_course_pivot['bc_course_3'] + train_course_pivot['bc_course_4'] + train_course_pivot['bc_course_5'] 
    train_course_pivot['bc_right_str'] = train_course_pivot['bc_course_6'] + train_course_pivot['bc_course_7'] + train_course_pivot['bc_course_8'] 
    train_course_pivot['bc_right_ball'] = train_course_pivot['bc_course_10'] + train_course_pivot['bc_course_12'] 

    # train_course_pivot.drop(columns=[
    #     'bc_course_0', 'bc_course_1', 'bc_course_2', 'bc_course_3', 'bc_course_4', 'bc_course_5',
    #     'bc_course_6', 'bc_course_7', 'bc_course_8', 'bc_course_9', 'bc_course_10', 'bc_course_11', 'bc_course_12'
    # ], inplace=True)
    print(train_course_pivot.shape)

    # マージ
    ball_cnt_all = train_ball_pivot.merge(train_course_pivot, on=['ball_cnt', 'pit_bat'], how='left')
    print(ball_cnt_all.shape)

    # 出力
    ball_cnt_all.to_feather(OUTPUT)
