# coding:utf-8
import os
import gc
import pandas as pd
import feather
import common

def preprocess(model_No):

    # 出力先のフォルダ作成
    os.makedirs(common.OUTPUT_PATH.format(model_No), exist_ok=True)

    for sample_No in range(1, common.DIVIDE_NUM+1):
        ALL_PITCH = common.ALL_PITCH
        ALL_PITCHER = common.ALLPITCHER.format(sample_No)
        ALL_CATCHER = common.ALLCATCHER.format(sample_No)
        ALL_PLAYER = common.ALLPLAYER.format(sample_No)

        OUTPUT = common.ALL_MERGE.format(model_No, sample_No)

        # 投球情報
        all_pitch = pd.read_feather(ALL_PITCH)
        print(all_pitch.shape)

        # 投手情報
        all_pitcher = pd.read_feather(ALL_PITCHER)
        print(all_pitcher.shape)

        # 捕手情報
        all_catcher = pd.read_feather(ALL_CATCHER)
        print(all_catcher.shape)

        # 打者情報
        all_player = pd.read_feather(ALL_PLAYER)
        print(all_player.shape)

        # Join
        merge_all = pd.merge(all_pitch, all_pitcher, left_on=['投手ID', '年度', 'pit_bat'], right_on=['選手ID', '年度', 'pit_bat'], how='left')
        merge_all = pd.merge(merge_all, all_player, left_on=['打者ID', '年度', 'pit_bat'], right_on=['選手ID', '年度', 'pit_bat'], how='left', suffixes=['_pit', '_bat'])
        merge_all = pd.merge(merge_all, all_catcher, left_on=['捕手ID', '年度', 'pit_bat'], right_on=['選手ID', '年度', 'pit_bat'], how='left')

        del all_pitch, all_pitcher, all_player

        # player同士の組み合わせ
        merge_all['salary_dif_p-b'] = merge_all['salary_pit'] - merge_all['salary_bat']
        merge_all['play_year_dif_p-b'] = merge_all['play_year_pit'] - merge_all['play_year_bat']
        merge_all['age_dif_p-b'] = merge_all['age_pit'] - merge_all['age_bat']
        merge_all['salary_year_dif_p-b'] = merge_all['salary_year_pit'] - merge_all['salary_year_bat']
        merge_all['salary_x_year_dif_p-b'] = merge_all['salary_x_year_pit'] - merge_all['salary_x_year_bat']
        merge_all['rank_year_dif_p-b'] = merge_all['rank_year_pit'] - merge_all['rank_year_bat']
        merge_all['rank_x_year_dif_p-b'] = merge_all['rank_x_year_pit'] - merge_all['rank_x_year_bat']
        merge_all['bmi_dif_p-b'] = merge_all['bmi_pit'] - merge_all['bmi_bat']

        merge_all['salary_dif_p-c'] = merge_all['salary_pit'] - merge_all['salary']
        merge_all['play_year_dif_p-c'] = merge_all['play_year_pit'] - merge_all['play_year']
        merge_all['age_dif_p-c'] = merge_all['age_pit'] - merge_all['age']
        merge_all['salary_year_dif_p-c'] = merge_all['salary_year_pit'] - merge_all['salary_year']
        merge_all['salary_x_year_dif_p-c'] = merge_all['salary_x_year_pit'] - merge_all['salary_x_year']
        merge_all['rank_year_dif_p-c'] = merge_all['rank_year_pit'] - merge_all['rank_year']
        merge_all['rank_x_year_dif_p-c'] = merge_all['rank_x_year_pit'] - merge_all['rank_x_year']
        merge_all['bmi_dif_p-c'] = merge_all['bmi_pit'] - merge_all['bmi']

        merge_all['salary_dif_b-c'] = merge_all['salary_bat'] - merge_all['salary']
        merge_all['play_year_dif_b-c'] = merge_all['play_year_bat'] - merge_all['play_year']
        merge_all['age_dif_b-c'] = merge_all['age_bat'] - merge_all['age']
        merge_all['salary_year_dif_b-c'] = merge_all['salary_year_bat'] - merge_all['salary_year']
        merge_all['salary_x_year_dif_b-c'] = merge_all['salary_x_year_bat'] - merge_all['salary_x_year']
        merge_all['rank_year_dif_b-c'] = merge_all['rank_year_bat'] - merge_all['rank_year']
        merge_all['rank_x_year_dif_b-c'] = merge_all['rank_x_year_bat'] - merge_all['rank_x_year']
        merge_all['bmi_dif_b-c'] = merge_all['bmi_bat'] - merge_all['bmi']

        # 球種の組合せ
        ball_kind = ['straight', 'curve', 'slider', 'shoot', 'fork', 'changeup', 'sinker', 'cutball']
        
        for ball in ball_kind:
            bc_ball = 'bc_' + ball
            pit_ball = ball + '_pit'
            bat_ball = ball + '_bat'
            cat_ball = ball

            merge_all['sub_bc_p_' + ball] = merge_all[bc_ball] - merge_all[pit_ball]
            merge_all['sub_p_c_' + ball] = merge_all[pit_ball] - merge_all[cat_ball]
            merge_all['sub_bc_c_' + ball] = merge_all[bc_ball] - merge_all[cat_ball]
            merge_all['sub_p_b_' + ball] = merge_all[pit_ball] - merge_all[bat_ball]
            merge_all['sub_bc_b_' + ball] = merge_all[bc_ball] - merge_all[bat_ball]
            merge_all['sub_b_c_' + ball] = merge_all[bat_ball] - merge_all[cat_ball]

            merge_all['div_bc_p_' + ball] = merge_all[bc_ball] / merge_all[pit_ball]
            merge_all['div_p_c_' + ball] = merge_all[pit_ball] / merge_all[cat_ball]
            merge_all['div_bc_c_' + ball] = merge_all[bc_ball] / merge_all[cat_ball]
            merge_all['div_p_b_' + ball] = merge_all[pit_ball] / merge_all[bat_ball]
            merge_all['div_bc_b_' + ball] = merge_all[bc_ball] / merge_all[bat_ball]
            merge_all['div_b_c_' + ball] = merge_all[bat_ball] / merge_all[cat_ball]

            merge_all['mul_bc_p_' + ball] = merge_all[bc_ball] * merge_all[pit_ball]
            merge_all['mul_p_c_' + ball] = merge_all[pit_ball] * merge_all[cat_ball]
            merge_all['mul_bc_c_' + ball] = merge_all[bc_ball] * merge_all[cat_ball]
            merge_all['mul_p_b_' + ball] = merge_all[pit_ball] * merge_all[bat_ball]
            merge_all['mul_bc_b_' + ball] = merge_all[bc_ball] * merge_all[bat_ball]
            merge_all['mul_b_c_' + ball] = merge_all[bat_ball] * merge_all[cat_ball]

            merge_all['ave_bc_p_' + ball] = (merge_all[bc_ball] + merge_all[pit_ball])/2
            merge_all['ave_p_c_' + ball] = (merge_all[pit_ball] + merge_all[cat_ball])/2
            merge_all['ave_bc_c_' + ball] = (merge_all[bc_ball] + merge_all[cat_ball])/2
            merge_all['ave_p_b_' + ball] = (merge_all[pit_ball] + merge_all[bat_ball])/2
            merge_all['ave_bc_b_' + ball] = (merge_all[bc_ball] + merge_all[bat_ball])/2
            merge_all['ave_b_c_' + ball] = (merge_all[bat_ball] + merge_all[cat_ball])/2

            merge_all['rate_bc_p_' + ball] = merge_all['ave_bc_p_' + ball] /(1-merge_all['ave_bc_p_straight'])
            merge_all['rate_p_c_' + ball] = merge_all['ave_p_c_' + ball] /(1-merge_all['ave_p_c_straight'])
            merge_all['rate_bc_c_' + ball] = merge_all['ave_bc_c_' + ball] /(1-merge_all['ave_bc_c_straight'])
            merge_all['rate_p_b_' + ball] = merge_all['ave_p_b_' + ball] /(1-merge_all['ave_p_b_straight'])
            merge_all['rate_bc_b_' + ball] = merge_all['ave_bc_b_' + ball] /(1-merge_all['ave_bc_b_straight'])
            merge_all['rate_b_c_' + ball] = merge_all['ave_b_c_' + ball] /(1-merge_all['ave_b_c_straight'])
    
        ball_kind_bc = list(map(lambda x: 'bc_' + x, ball_kind))
        merge_all.drop(columns=ball_kind, inplace=True)
        merge_all.drop(columns=ball_kind_bc, inplace=True)

        # コースの組合せ
        course_kind = [
            # 'course_0', 'course_1', 'course_2', 'course_3', 'course_4', 'course_5', 'course_6', 
            # 'course_7', 'course_8', 'course_9', 'course_10', 'course_11', 'course_12',
            'high_str', 'high_ball', 'mid_str', 'low_str', 'low_ball', 
            'left_str', 'left_ball', 'center_str', 'right_str', 'right_ball',
            ]

        for course in course_kind:
            bc_course = 'bc_' + course
            pit_course = course + '_pit'
            bat_course = course + '_bat'
            cat_course = course

            merge_all['sub_bc_p_' + course] = merge_all[bc_course] - merge_all[pit_course]
            merge_all['sub_p_c_' + course] = merge_all[pit_course] - merge_all[cat_course]
            merge_all['sub_bc_c_' + course] = merge_all[bc_course] - merge_all[cat_course]
            merge_all['sub_p_b_' + course] = merge_all[pit_course] - merge_all[bat_course]
            merge_all['sub_bc_b_' + course] = merge_all[bc_course] - merge_all[bat_course]
            merge_all['sub_b_c_' + course] = merge_all[bat_course] - merge_all[cat_course]

            merge_all['div_bc_p_' + course] = merge_all[bc_course] / merge_all[pit_course]
            merge_all['div_p_c_' + course] = merge_all[pit_course] / merge_all[cat_course]
            merge_all['div_bc_c_' + course] = merge_all[bc_course] / merge_all[cat_course]
            merge_all['div_p_b_' + course] = merge_all[pit_course] / merge_all[bat_course]
            merge_all['div_bc_b_' + course] = merge_all[bc_course] / merge_all[bat_course]
            merge_all['div_b_c_' + course] = merge_all[bat_course] / merge_all[cat_course]
            
            merge_all['mul_bc_p_' + course] = merge_all[bc_course] * merge_all[pit_course]
            merge_all['mul_p_c_' + course] = merge_all[pit_course] * merge_all[cat_course]
            merge_all['mul_bc_c_' + course] = merge_all[bc_course] * merge_all[cat_course]
            merge_all['mul_p_b_' + course] = merge_all[pit_course] * merge_all[bat_course]
            merge_all['mul_bc_b_' + course] = merge_all[bc_course] * merge_all[bat_course]
            merge_all['mul_b_c_' + course] = merge_all[bat_course] * merge_all[cat_course]

            merge_all['ave_bc_p_' + course] = (merge_all[bc_course] + merge_all[pit_course])/2
            merge_all['ave_p_c_' + course] = (merge_all[pit_course] + merge_all[cat_course])/2
            merge_all['ave_bc_c_' + course] = (merge_all[bc_course] + merge_all[cat_course])/2
            merge_all['ave_p_b_' + course] = (merge_all[pit_course] + merge_all[bat_course])/2
            merge_all['ave_bc_b_' + course] = (merge_all[bc_course] + merge_all[bat_course])/2
            merge_all['ave_b_c_' + course] = (merge_all[bat_course] + merge_all[cat_course])/2

        course_kind_bc = list(map(lambda x: 'bc_' + x, course_kind))
        merge_all.drop(columns=course_kind, inplace=True)
        merge_all.drop(columns=course_kind_bc, inplace=True)

        # ダミー変数
        # merge_all = pd.get_dummies(merge_all, columns=['pit_bat'])

        # 不要な列を削除
        merge_all.drop(columns=[
            '選手ID_pit', '選手ID_bat', '選手ID',
            '試合内連番',
            '年度', 
            '試合ID', 
            'ホームチームID', 'アウェイチームID', 
            '投手ID', '投手チームID', 
            '打者ID', '打者チームID', 
            'プレイ前走者状況', 
            '捕手ID', 
            'opening_date', 'game_date',
            'start_time', 'game_time', 'elapsed_time', 'pit_bat'
        ], inplace=True)

        # Rename
        merge_all.rename(columns={
            'データ内連番': 'No',
            '試合内投球数': 'pitch_cnt_in_game',
            'イニング': 'inning',
            'イニング内打席数': 'bat_cnt_in_inning',
            '打席内投球数': 'pitch_cnt_in_bat',
            '投手登板順': 'pitch_order',
            '投手試合内対戦打者数': 'player_cnt_in_game',
            '投手試合内投球数': 'pitcher_cnt_in_game',
            '投手イニング内投球数': 'pitcher_cnt_in_inning',
            '打者打順': 'bat_order',
            '打者試合内打席数': 'bat_cnt_in_game',
            'プレイ前ホームチーム得点数': 'home_point',
            'プレイ前アウェイチーム得点数': 'away_point',
            'プレイ前アウト数': 'out_cnt',
            'プレイ前ボール数': 'ball_cnt',
            'プレイ前ストライク数': 'strike_cnt',
        }, inplace=True)

        print(merge_all.shape)

        merge_all.to_feather(OUTPUT)
        print(OUTPUT, merge_all.shape)

        del merge_all
    
    gc.collect()
