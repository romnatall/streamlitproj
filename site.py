import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import random
import numpy as np
import pandas as pd
from PIL import Image
import time
from db import SimpleDatabase as sb
from model import guess



tabs = st.tabs(["котировки", "чаевые","игра"])
with tabs[0]:
    # Заголовок приложения
    st.write("""
    # Простое приложение для отображения цен акций
    Показаны цены закрытия и объем акций Apple
    """)

    # Обозначение тикера 
    tickerSymbol = 'AAPL'

    # Получение данных о ценах акций
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2023-1-30')

    # Отображение графика цен закрытия
    st.write("""### цены закрытия""")
    st.line_chart(tickerDf.Close)

    # Отображение графика объема акций
    st.write("""### объемы""")
    st.line_chart(tickerDf.Volume)

with tabs[1]:
    df=pd.read_csv('datasets/tips.csv', index_col=0)
    d=df.groupby('time')[['tip','total_bill']].sum().reset_index()

    fig = px.bar(d, x='time', y='tip', title='Чаевые в зависимости от времени заказа')
    st.plotly_chart(fig)

    d['tip']=d['tip']/d['total_bill']
    fig = px.bar(d, x='time', y='tip', title='Чаевые относительно счета в зависимости от времени заказа')
    st.plotly_chart(fig)

    p=str(round((d['tip'].max()/d['tip'].min())*100-100,ndigits=2))+"% "
    st.write(f"""хотя вечером дают в сумме больше чаевых, в обед дают на {p} чаевых больше относительно чека""")




with tabs[2]:

    db =sb()
    
    wins= db.data.get('win',0)
    loses= db.data.get('lose',0)
    draws= db.data.get('draw',0)
    winrate=str(round((wins/(wins+loses) if (wins+loses)>0 else 1 )*100,ndigits=2))+"% "
    play= db.data.get('play','012')
    db.data['play']=play
    predic={
        "Камень": '0',
        "Ножницы": '1',
        "Бумага": '2'
    }
    кpredic = {i: key for key, i in predic.items()}

    # Загрузка изображений
    res=(200,200)
    pngs = {
        "Камень": Image.open("images/rock.jpg").resize(res),
        "Ножницы": Image.open("images/scissors.jpeg").resize(res),
        "Бумага": Image.open("images/paper.png").resize(res),
        "win": Image.open("images/win.jpeg").resize(res),
        "lose": Image.open("images/lose.png").resize(res),
        "draw": Image.open("images/draw.jpg").resize(res)
    }

    with st.spinner("Идет загрузка..."):
        def play_game(player_choice):
            
            #пауза нужна только чтобы было нагляднее при нажатии на  ту же клавишу
            #time.sleep(2)
            pred=guess(db.data['play'])
            st.write(pred)
            db.data['play']+=predic[player_choice]
            choices = ["Камень", "Ножницы", "Бумага"]
            computer_choice = choices[(pred.index(max(pred))+2)%len(pred) ]
        

            col1, col2 = st.columns(2)

            # В первой колонке разместим изображение
            with col1:
                st.write(f"## Вы выбрали:\n {player_choice}")
                st.image(pngs[player_choice])

            # Во второй колонке разместим текст или другие элементы
            with col2:
                st.write(f"## Компьютер выбрал:\n {computer_choice}")
                st.image(pngs[computer_choice])

            col1, col2, col3 = st.columns(3)


            with col2:
                    if player_choice == computer_choice:
                        db.data['draw']+=1
                        st.write("## Ничья!")
                        st.image(pngs["draw"])
                    elif (
                        (player_choice == "Камень" and computer_choice == "Ножницы") or
                        (player_choice == "Ножницы" and computer_choice == "Бумага") or
                        (player_choice == "Бумага" and computer_choice == "Камень")
                    ):
                        db.data['win']+=1
                        st.write("## Победа!")
                        st.image(pngs["win"])
                    else:
                        db.data['lose']+=1
                        st.write("## Поражение")
                        st.image(pngs["lose"])
            db.save_data()

    # Веб-приложение
    st.title("Игра в Камень-Ножницы-Бумага")
    st.write("эта игра использует машинное обучение (модель я сам однажды придумал), она не дает ответы случайно, в обычной игре можно каждый раз выбирать один и тот же вариант и остаться в ничьей, тут так не получится")

    # Вывод в колонках
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("####  Побед: ", wins)

    with col2:
        st.write("####  Поражений: ", loses)

    with col3:
        st.write("####  Ничьих: ", draws)

    st.write("####  Процент побед (не считая ничьих): ", winrate)

    # Создаем кнопки для выбора
    col1, col2, col3 = st.columns(3)
    with col1:
        rock_button = st.button("Камень")
    with col2:
        scissors_button = st.button("Ножницы")
    with col3:
        paper_button = st.button("Бумага")


    # Обработка нажатий кнопок
    if rock_button:
        play_game("Камень")
    elif scissors_button:
        play_game("Ножницы")
    elif paper_button:
        play_game("Бумага")