# 球種予測部門

|No|boosting|sub|features|CV|評価値|コメント|
|----|----|----|----|----|----|----|
|24|gbdt|sub|197|1.12025|1.35820|22相当|
|25|gbdt|sub|197|1.11685|1.35809|learning_rate=0.01|
|26|gbdt|sub|197|1.11553|1.35326|courseの予測値の変更|
|27|gbdt|sub|197|1.11563|1.35421|分割の切れ目を日付と一致させる|
|28-5|gbdt|sub|197|1.11574|1.35575|5分割|
|28-3|gbdt|sub|197|1.11602|1.35585|3分割|
|29|gbdt|sub|197|1.12506|1.35991|4分割,trainで使用する領域を逆転|
|30|gbdt|sub|295|1.11910|1.34488|球種・コースの組合せを追加|
|31|gbdt|sub|327|1.11799|1.34442|捕手の集計結果を追加|
|32|gbdt|sub|591|1.11760|1.34411|捕手の組み合わせを追加|
|32|gbdt|none|581|1.11915|1.34394|サブモデルを使用しない|
|33|dart|none|581|1.11317|1.34018|dart(tune)|
|34|gb+da|none|581|---|1.34010|32+33 アンサンブル|
|35|gbdt|none|581|1.11881|1.34394|32のseedをfoldごとに変える|
|36|gbdt|none|581|1.11914|1.35272|foldの区切りを変更|
|37|dart|none|581|---|1.35422|foldの区切りを変更|
|38|rf|none|581|1.44163|1.50862|random forest|
|39|gbdt|none|1010|1.12763|1.33920|打者の集計結果を追加|
|40|dart|none|1010|1.12086|1.33925|39のdart|
|41|gb+da|none|1010|---|1.33742|39+40 アンサンブル|
|42|gbdt|none|1010|0.48937|1.33584|multi-error|
|43|dart|none|1010|0.48762|1.33475|multi-error dart|
|44|dart|none|1010|---|1.33405|42+43 アンサンブル|
|45|gb+da|none|1010|---|1.33514|41+44 アンサンブル|
|46|dart|none|1010|0.48722|1.33518|multi-error dart log1p|
|47|dart|LRHL|1023|0.48817|1.33353|LRHRサブモデル(m-error/dart)|
|48|gbdt|LRHL|1023|0.48964|1.33561|LRHRサブモデル(m-error/gbdt)|
|49|gb+da|LRHL|1023|---|1.33333|47+48 アンサンブル|
|47-1|dart|LRHL|1023|0.48815|1.33229 *|LRHRサブモデル(m-error/dart) tune|
|50|dart|LRHL|1035|0.48736|1.33359|m-error/dart|
|50-1|dart|LRHL|1020|0.48766|1.33257|m-error/dart|
|51|gb+da|LRHL|1020|0.48904|1.33280|m-error アンサンブル|
|52|gb+da|LRHL|980|0.48863|1.33332|m-error 下位の特徴量を除外|
|53|gb+da|LRHL|974|0.48849|1.34105|m-error 外国人を日本人と同じに|
|54|gb+da|LRHL|649|0.48792|1.33264|m-error コースの特徴量を減らす|
|55|gb+da|LRHL|632|0.48819|1.33434|m-error コースの特徴量を減らす2|
|56|gb+da|LRHL|645|0.48815|1.33853|m-error 2年未満の選手の集計結果を除外|
|57|gb+da|LRHL|645|0.48813|1.33400|m-error 54相当|
|58|gb+da|LRHL|649|0.48792|1.33264|m-error 本当に54相当|
|59|gb+da|LRHL|636|0.488145|1.33339|m-error bc_courseを抜いた|
|59-1|gb+da|LRHL|636|0.48814|1.33366|m-error アンサンブルを幾何平均で|
|60|gb+da|LRHLSB|598|0.48715|1.33324|m-error 上下左右/strike/ball|
|61|gb+da|LRHL|637|0.48708|1.33333|m-error last-ball(leak)|
|62|gb+da|LRHL|637|0.48667|1.33366|m-error last-ball(leak/0-1)|

# コース予測部門

|No|boosting|sub|features|CV|評価値|コメント|
|----|----|----|----|----|----|----|
|24|gbdt|none|187|2.34067|2.34866|22相当|
|25|gbdt|none|187|2.33886|2.34817|learning_rate=0.01|
|26|gbdt|none|187|2.33477|2.34893|特徴量で集計した部分を抜かない|
|27|gbdt|none|187|2.33482|2.34892|分割の切れ目を日付と一致させる|
|28-5|gbdt|none|187|2.33564|2.34880|5分割|
|28-3|gbdt|none|187|2.33402|2.34929|3分割|
|29|gbdt|none|187|2.32977|2.35135|4分割,trainで使用する領域を逆転|
|30|gbdt|none|285|2.33313|2.34746|球種・コースの組合せを追加|
|31|gbdt|none|317|2.33263|2.34766|捕手の集計結果を追加|
|32|gbdt|none|581|2.33313|2.34764|捕手の組み合わせを追加|
|32|gbdt|none|581|2.34091|2.34740|特徴量から集計期間を抜く|
|32|gbdt|sub|588|2.33698|2.34963|サブモデルを使用する|
|33|dart|none|581|2.34090|2.34759|dart|
|33|dart|none|581|2.33982|2.34683|dart(tune)|
|34|gb+da|none|581|---|2.34687|32+33 アンサンブル|
|35|gbdt|none|581|2.34081|2.34722|32のseedをfoldごとに変える|
|36|gbdt|none|581|2.34114|2.34884|foldの区切りを変更|
|37|dart|none|581|2.33936|2.34980|foldの区切りを変更|
|38|rf|none|581|2.38128|2.37949|random forest|
|39|gbdt|none|1010|2.34165|2.34657|打者の集計結果を追加|
|40|dart|none|1010|2.34117|2.34655|39のdart|
|41|gb+da|none|1010|---|2.34624 *|39+40 アンサンブル|
|42|gbdt|none|1010|0.77013|2.34655|multi-error|
|43|dart|none|1010|0.76921|2.34666|multi-error dart|
|44|dart|none|1010|---|2.34630|42+43 アンサンブル|
|45|gb+da|none|1010|---|2.34621|41+44 アンサンブル|
|46|dart|none|1010|0.76989|2.34667|multi-error dart log1p|
|47|dart|LRHL|1023|0.76986|2.34677|LRHRサブモデル(m-error/dart)|
|47-1|dart|none|1010|0.76938|2.34633|m-error/dart tune|
|50|dart|LRHL|1035|0.74534|2.35386|m-error/dart|
|50-1|dart|LRHL|1020|0.74690|2.35286|m-error/dart|
|51|gb+da|none|1010|0.76955|2.34621|m-error アンサンブル|
|52|gb+da|none|970|0.76971|2.34628|m-error 下位の特徴量を除外|
|52-1|gb+da|none|970|2.34133|2.34620 **|m-logloss 下位の特徴量を除外|
|55|gb+da|none|622|2.34262|2.34715|m-logloss コースの特徴量を減らす2|
|56|gb+da|none|635|2.34214|2.34706|m-logloss 2年未満の選手の集計結果を除外|
|57|dart|none|635|2.34164|2.34696|m-logloss 54相当|
|57|gb+da|none|635|2.34204|2.34684|m-logloss 54相当|
|58|gb+da|none|639|2.34135|2.34665|m-logloss 本当に54相当|
|59|dart|none|639|2.34094|2.34681|m-logloss tune|
|59|gb+da|none|639|2.34131|2.34668|m-logloss tune|
|59-1|gb+da|none|639|2.34131|2.34667|m-logloss アンサンブルを幾何平均で|
|60|gb+da|none|590|2.34205|2.34688|m-logloss 上下左右/strike/ball|
|60-1|dart|LRHLSB|598|2.22900|2.36213|m-logloss sub-model|
|61|gb+da|none|640|2.31920|2.32270|m-logloss last-ball(leak)|
|61-1|gb+da|lastball|640|2.31966|2.35255|m-logloss last-ball(predict)|
|61-2|dart|lastball|640|2.31907|2.35250|m-logloss last-ball(predict)|
|61-3|gbdt|lastball|640|2.32023|2.35266|m-logloss last-ball(predict/0-1)|
|62|gbdt|none|640|2.31994|2.32365|m-logloss last-ball(leak/0-1)|