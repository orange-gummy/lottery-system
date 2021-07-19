# lottry-system
創作展創作部門の抽選システム

# Development Environment
使った言語：python3.9  
エディター：spyder  

# How to use
1.lottery.zipをダウンロード後解凍する  
2.lotteryの中にあるlottery.exeを実行(隠しファイルがたくさんあるのでlotteryの外に出すと動きません)(不明な提供元みたいなやつは詳細から実行してくださいー）  
3.実行後のウィンドウでファイルのを選択、何回目の抽選かを入力して実行をクリック  
4.出力のボックスに抽選結果が表示されれば抽選完了  
5.コピーするを押せばクリップボードにコピー、保存するを押せば指定した名前で.txtで保存できる  
6.一回抽選をした後でもそのまま二度目以降の抽選をすることができる  
# How to test
sample.csvが使えます960人分のサンプルデータです

# Date
・入力するデータ(.csv)  
　　左から順に生徒の学年、生徒のクラス、生徒の出席番号、第一希望の学年クラス、第二希望の学年クラス  
　　(例)1,A,1,5A,6C  
  
・出力されるデータ  
　　テキストボックスに出力される  
　　コピペするか保存するかして使う 
  
・List of winners1~4回目.csv  
　　一度抽選したら自動で作られるファイル  
　　抽選に当たった人の一覧  
　　二回目以降の抽選ではこのファイルを使って確率を下げる  

# Error(red letters)
・抽選するCSVファイルを開いてください
　　パスが間違っている、または指定されていません。ファイルを開くボタンから指定してください  
  
・CSVファイルの様式が間違っている可能性があります  
　　抽選をするデータに欠陥値が見つかりました。データの様式が間違えている、またはデータが抜けている可能性があります  
  
・必ず1回目から順に指定して実行してください  
　　一度当選した人の確率を下げるために使うCSVファイルが見つかりません。1回目から順に実行してください  
  
・正常に抽選されませんでした(出力に表示される)  
　　文章の通り何かしらのエラーが起きた場合に表示される  
  
# Commitment
・必要最低限の入力で抽選できるようにした  
・GUIを立ち上げたまま何回も抽選できる  
・errorを表示するようにして、その場合抽選を行わないようにした  
・一度GUIを閉じても一度当選した人のデータは残るため、2回目以降から抽選できる
・コードもわかりやすい...はず  
