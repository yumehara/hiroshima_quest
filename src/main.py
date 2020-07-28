# coding:utf-8
import os
import Preprocess_All as merge
import Preprocess_ball as ball
import Preprocess_pitch as pitch
import Preprocess_player_2017 as play2017
import Preprocess_player as player
import Predict_Ball as pred_ball
import Predict_Course as pred_course
import Predict_Lastball as pred_lastball
import ensemble as ensmbl
import common


submit_No = '66'

boosting1 = common.DART
boosting2 = common.GBDT

common.set_divide_num(5)

# # playerごと
# play2017.preprocess()
# player.preprocess(True)      # 穴埋めあり

# # 投球ごと
# ball.preprocess()
# pitch.preprocess()

# # 前処理
# merge.preprocess(submit_No)
# print('--- preprocess ---')


# # コース予測(1:dart)
# use_sub_model = False
# metric1 = common.M_LOGLOSS
# sub_str1 = boosting1 + '_' + metric1
# cv1 = pred_course.train_predict(submit_No, use_sub_model, boosting1, metric1, sub_str1)
# print('--- predict course {}---'.format(sub_str1))

# # コース予測(2:gbdt)
# sub_str2 = boosting2 + '_' + metric1
# cv2 = pred_course.train_predict(submit_No, use_sub_model, boosting2, metric1, sub_str2)
# print('--- predict course {}---'.format(sub_str2))

# # コース予測アンサンブル(gbdt + dart)
# cv_ave = (cv1 + cv2)/2
# ensmbl.ensemble(submit_No, submit_No, sub_str1, submit_No, sub_str2, False, cv_ave)
# print('--- ensemble course ---')


# # コース予測サブモデル(LRHL)
# metric0 = common.M_LOGLOSS
# boosting0 = common.GBDT
# pred_course.train_predict2(submit_No, boosting0, metric0, 'LR')
# pred_course.train_predict2(submit_No, boosting0, metric0, 'HL')
# pred_course.ensemble_RLHL(submit_No)
# print('--- predict course sub ---')


# # 球種予測(1:dart)
# use_sub_model = True
# metric2 = common.M_ERROR
# sub_str1 = boosting1 + '_' + metric2
# cv1 = pred_ball.train_predict(submit_No, use_sub_model, boosting1, metric2, sub_str1)
# print('--- predict ball {}---'.format(sub_str1))

# # 球種予測(2:gbdt)
# sub_str2 = boosting2 + '_' + metric2
# cv2 = pred_ball.train_predict(submit_No, use_sub_model, boosting2, metric2, sub_str2)
# print('--- predict ball {}---'.format(sub_str2))


# # 球種予測アンサンブル(gbdt + dart)
# cv_ave = (cv1 + cv2)/2
# ensmbl.ensemble(submit_No, submit_No, sub_str1, submit_No, sub_str2, True, cv_ave)
# print('--- ensemble ball ---')

# Tuning
# python main.py 2>> tuning_0705.log
# use_sub_model = True
# pred_ball.tuning(submit_No, use_sub_model, boosting, metric)
# pred_course.tuning(submit_No, use_sub_model, boosting, metric)


# 球種予測(アンサンブル)
cv_ave = (0.4878164618 + 0.4878935676)/2
ensmbl.ensemble(submit_No, 63, 'ensmbl', 64, 'ensmbl', True, cv_ave)

# コース予測(アンサンブル)
cv_ave = (2.3406924206 + 2.3403137704)/2
ensmbl.ensemble(submit_No, 63, 'ensmbl', 65, 'ensmbl', False, cv_ave)