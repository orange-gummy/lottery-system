# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 22:35:05 2021

@author: T.MIYAKE
"""
# ライブラリ一覧 os,pandas,random,tkinter,(time)
# インストール必要なライブラリ　pandas
import os
import pandas as pd
import random
import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
# ライブラリ読み込み

def main():# main proglam
    value_setting()
    GUI()

def command():
    GUI_get()
    read()
    if error_bool == 0:
        lottery_preparation()
        lottery('applied_class')# 第一希望
        lottery('applied_class2')# 第二希望の抽選
        rest_lottery()# 枠の残ったクラスの抽選(完全ランダム)
        output()# txtで抽選結果の出力
        output2()# csvで次に確率を下げる生徒をtxtで出力
    else:
        txt2.delete('1.0', tk.END)
        txt2.insert('end','正常に抽選されませんでした')

def value_setting():# 定数の定義
    # 定数をグローバス変数として宣言
    global GROUPS_APPLIED_CLASS
    global NUMBER_OF_WINNERS
    global SECOND_PROBABILITY
    
    #　定数を設定
    GROUPS_APPLIED_CLASS = ['5A','5B','5C','5D','6A','6B','6C','6D']# 劇をするクラスのlist
    NUMBER_OF_WINNERS = 40# クラスごとの当選者の数
    SECOND_PROBABILITY = 0.5# 一回当選した人が二回目以降に当選する確率

def GUI():#GUI
    #　ここからテータを取り出すためにテキストボックスをグローバル変数とする
    global box
    global txt1
    global txt2
    global combo
    global label7
    global label8
    
    # ここからウィンドウに表示するデータを作る
    box = tk.Tk()
    box.title('創作展創作部門抽選システム')
    box.geometry("680x400")
    font1 = font.Font(size=10,family="MSゴシック",weight="bold")
    font2 = font.Font(size=10)
    combo = ttk.Combobox(box, state='readonly', width=20)
    combo["values"] = ("1回目","2回目","3回目","4回目")
    combo.current(0)
    button1 = tk.Button(box, text='抽選する', fg="white", bg='black',font=font1, command=command, relief='flat', width=15)
    label2 = tk.Label(box, text='抽選するデータ：')
    label4 = tk.Label(box, text='出力：')
    label6 = tk.Label(box, text='何回目の抽選：')
    label7 = tk.Label(box, text='',fg='red')
    label8 = tk.Label(box, text='',fg='red')
    txt1 = tk.Entry(width=60)
    txt2 = ScrolledText(box, height=10, width=60)
    dialog_button = tk.Button(box, text='ファイルを開く', command=file_open, width=15, relief='raised')
    button2 = tk.Button(box, text='クリップボードにコピー', command=copy,font=font2, width=20)
    button3 = tk.Button(box, text='textで保存', command=export,font=font2, width=20)
    
    # ここからウィンドウに配置
    label2.place(x=100, y=50)# 抽選するデータ：
    txt1.place(x=190, y=50)# 入力
    label4.place(x=100, y=200)# 出力するファイル名
    label6.place(x=100, y=100)# 何回目の抽選か
    combo.place(x=190, y=100)# 何回目
    button1.place(x=280, y=150)# 抽選する
    dialog_button.place(x=440, y=75)#ファイルを開く
    txt2.place(x=140, y=200)# 出力
    button2.place(x=185, y=350)#コピーする
    button3.place(x=355, y=350)#保存する
    label7.place(x=190, y=30)
    label8.place(x=190, y=75)
    box.mainloop()# 表示

def copy():#出力結果をクリップボードにコピー
    box.clipboard_append(txt2.get("1.0","end"))
    
def export():#txtファイルに出力結果を保存
    typ = [('TXTファイル','*.txt')]
    fle = filedialog.asksaveasfilename(filetypes = typ, initialdir = os.getcwd(),defaultextension='txt')
    f = open(fle, 'w')
    f.write(txt2.get("1.0","end"))

def file_open():#抽選するcsvファイルを選択する
    txt1.delete(0, tk.END)
    typ = [('CSVファイル','*.csv')]
    fle = filedialog.askopenfilename(filetypes = typ, initialdir = os.getcwd())
    txt1.insert(tk.END,fle)

def GUI_get():# GUIに入力された値の読み取り
    # GUIから取得したデータを入れる変数を宣言
    global questionnaire_results
    global Number_of_lottery
    
    # GUIからデータを取得して変数に入れる
    questionnaire_results = txt1.get()
    Number_of_lottery = combo.get()


def read():# 入力のcsvファイルの読み込み
    # カレントディレクトリの絶対パスを取得
    global cwd
    cwd =  os.getcwd()
    
    global error_bool#errorの判定
    error_bool = 0
    
    # 生徒と希望クラスのデータをdatefarmeに読み込み
    global df
    try:
        label7["text"] = ''
        df = pd.read_csv(questionnaire_results, sep=',', encoding='shift jis', index_col=False, engine='python', dtype=str, names=['student_grade','student_class','student_number','applied_class','applied_class2'])
    
    except:#error
        error_bool = 1
        label7["text"] = '抽選するCSVファイルを開いてください'
    
    if df.isnull().values.sum() != 0:
        label7["text"] = 'CSVファイルの様式が間違っている可能性があります'
        error_bool = 1
    
    label8["text"] = ''
    
    if Number_of_lottery != '1回目':# 二回目以降の抽選の場合
        try:
            global df_of_winners#確率を下げる人のlistを作成
            if Number_of_lottery == '2回目':
                df_of_winners = pd.read_csv(cwd + '\\' + 'List of winners1回目.csv',encoding='shift jis', names=["student_grade","student_class","student_number"], dtype=str)
            elif Number_of_lottery == '3回目':
                df_of_winners1 = pd.read_csv(cwd + '\\' + 'List of winners1回目.csv',encoding='shift jis', names=["student_grade","student_class","student_number"], dtype=str)
                df_of_winners2 = pd.read_csv(cwd + '\\' + 'List of winners2回目.csv',encoding='shift jis', names=["student_grade","student_class","student_number"], dtype=str)
                df_of_winners = pd.merge(df_of_winners1,df_of_winners2)
            elif Number_of_lottery == '4回目':
                df_of_winners1 = pd.read_csv(cwd + '\\' + 'List of winners1回目.csv',encoding='shift jis', names=["student_grade","student_class","student_number"], dtype=str)
                df_of_winners2 = pd.read_csv(cwd + '\\' + 'List of winners2回目.csv',encoding='shift jis', names=["student_grade","student_class","student_number"], dtype=str)
                df_of_winners12 = pd.merge(df_of_winners1,df_of_winners2)
                df_of_winners3 = pd.read_csv(cwd + '\\' + 'List of winners3回目.csv',encoding='shift jis', names=["student_grade","student_class","student_number"], dtype=str)
                df_of_winners = pd.merge(df_of_winners12,df_of_winners3)
        # 一度当選した人をdateframeに読み込み
        
        except:#error
            error_bool = 1
            label8["text"] = '必ず1回目から順に指定して実行してください'
        
        global list_of_winners
        df_comparison = df.copy()
        df_comparison['index'] = df_comparison.index
        list_of_winners = list(pd.merge(df_comparison, df_of_winners)['index'])

def lottery_preparation():# lottryの準備
    global df_
    global restNum
    
    df_ = df.copy()# 実際にいじるデータにコピー
    df_["decided"] = "Not yet"
    restNum = [NUMBER_OF_WINNERS,NUMBER_OF_WINNERS,NUMBER_OF_WINNERS,NUMBER_OF_WINNERS,NUMBER_OF_WINNERS,NUMBER_OF_WINNERS,NUMBER_OF_WINNERS,NUMBER_OF_WINNERS]
    # resutNumはクラスごとの残りの枠　初期値はnumber_of_winner

def lottery(stage):# 抽選 stage=希望クラスの列の見出し
    for i, group in enumerate(GROUPS_APPLIED_CLASS):# groupに劇のクラスを代入して実行を繰り返す
        cond = (df_[stage] == group)&(df_["decided"] == "Not yet")# 全員のdecidedに'Not yet'を入れる
        dfM = df_[cond]# そのクラスに希望した人のみのデータ
        
        if restNum[i] >= dfM.shape[0]:# 行数(希望者)が枠より少なかった場合
            restNum[i] -= dfM.shape[0]# 残りの枠を計算
            df_.loc[cond,"decided"] = group# その場合はdecidedに希望するクラス名を入れる
            
        elif restNum[i] < dfM.shape[0]:# 行数(希望者)が枠より多かった場合
            ind = list(dfM.index.values)# 希望した人のindex
            
            if Number_of_lottery != '1回目':#2回目以降の確率を下げる処理
                for index in ind:#一回当たったことがある人を一定の確率で抜く
                    if index in list_of_winners:
                        continue
                    if random.random() > SECOND_PROBABILITY:
                        ind.remove(index)
            
            
            if len(ind) >= restNum[i]:#抜いたデータが枠よりまだ大きい場合
                sel = random.sample(ind,restNum[i])# 希望した人indexから枠の数取り出す
                df_.loc[sel,"decided"] = group# 当たった人のdecidedに希望するクラス名を入れる
                restNum[i] = 0# 残りの枠は0
            else:#抜いたデータが枠より少なくなってしまった場合
                df_.loc[ind,"decided"] = group#抜いたデータの全員を当選させる
                restNum[i] -= len(ind)#残りの枠の計算

def rest_lottery():# 枠の余ったクラスの抽選　完全ランダム
     for i, group in enumerate(GROUPS_APPLIED_CLASS):# groupに劇のクラスの残りの枠代入して実行を繰り返す
        if restNum[i] != 0:#まだ枠のが残っていた場合
            cond = (df_["decided"] == "Not yet")# まだ決まっていない人
            dfM = df_[cond]
            ind = list(dfM.index.values)
            if Number_of_lottery != '1回目':#2回目以降の抽選の場合
                for index in ind:
                    if index in list_of_winners:
                        continue
                    if random.random() > SECOND_PROBABILITY:
                        ind.remove(index)
            if len(ind) >= restNum[i]:#残りの人から一回当選した人を抜いた人数が残りの枠より多かった場合(普通は必ずこうなる)
                sel = random.sample(ind,restNum[i])# 希望した人indexから枠の数取り出す
                df_.loc[sel,"decided"] = group# 当たった人のdecidedに希望するクラス名を入れる
                restNum[i] = 0# 残りの枠は0
            else:
                ind_ = list(dfM.index.values)
                sel = random.sample(ind_,restNum[i])# 希望した人indexから枠の数取り出す
                df_.loc[sel,"decided"] = group
                restNum[i] = 0# 残りの枠は0

def output():#出力に表示する
    txt2.delete('1.0', tk.END) #テキストボックスを空にする
    global df__
    global df_dict
    df__ = df_[df_.decided != 'Not yet'].copy()# 受からなかった人を除外
    df__['output'] = df__['student_grade'].copy()+'年'+df__['student_class'].copy()+'組'+df__['student_number'].copy()+'番'
    df_dict = {}
    
    for name, group in df__.groupby('decided'):# 当選クラスごとに分割
        df_dict[name] = group
        
    for key in GROUPS_APPLIED_CLASS:# クラスごとに当選者を呼び出す
        txt2.insert('end','●' + key + 'の劇の当選者：')
        txt2.insert('end',df_dict[key].to_csv(path_or_buf=None , mode='a' , columns=['output'] , encoding='shift jis' , header=False , index=False , line_terminator='、'))
        txt2.insert('end','\n')

def output2():# 次の抽選から確率を下げる人のリストを出力
    df__.to_csv(cwd + '\\' + 'List of winners' + Number_of_lottery + '.csv' , encoding='shift jis' , columns=['student_grade','student_class','student_number'] , header=False , index=False)

if __name__ == '__main__':
    main()
