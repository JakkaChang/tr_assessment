from bot import Bot
import pandas as pd


df_train = pd.read_csv('eth-perp_train.csv')


if __name__ == '__main__':
    print('############## TRAIN BOT ##################')
    bot_train = Bot(df_train)
    bot_train.run()


    '''BELOW IS THE TEST BOT WITH THE DATASET THAT WE WILL RUN YOUR CODE ON'''
    # print('############## TEST BOT ##################')
    # df_test = pd.read_csv('eth-perp_test.csv')
    # bot_test = Bot(df_test)
    # bot_test.run()