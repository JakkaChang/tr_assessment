from volatility_calculation import longTermVol, shortTermVol
import numpy as np
class Bot:
    def __init__(self, df):
        self.df = df
        self.initial_capital = 10000 # in dollar units
        self.max_positions = 9000 # in dollar units
        
        self.bought_ethereums = 0
        self.cumulative_prices = 0 
        self.positions = 0 # in dollar units
        self.average_buy_price = 0

        self.earned_ethereums = 0

        '''
        TODO: You can make the following variables dynamic
        '''
        self.static_upsilon = 0.07
        self.static_psi = 0.05
        self.static_chi = 0.09
        self.sigma = 0 
       
    def buy(self, price, amount):
        self.bought_ethereums += amount / price
        self.positions += amount
        self.cumulative_prices += price * amount
        self.average_buy_price = self.cumulative_prices / self.positions
        # self.printBuyLogs(price, amount)

    def printBuyLogs(self, price, amount):
        print('Current ETH price is: ', price)
        print('amount is: ', amount)
        print('bought ethereums: ', self.bought_ethereums)
        print('average buy price: ', self.average_buy_price)

    def sell(self, price):
        sold_ethereums = self.positions / price
        self.earned_ethereums += (self.bought_ethereums - sold_ethereums)
        self.bought_ethereums = 0
        self.cumulative_prices = 0
        self.positions = 0
        self.average_buy_price = 0
        # self.printSellLogs(price, sold_ethereums)

    def printSellLogs(self, price, sold_ethereums):
        print('Current ETH price is: ', price)
        print('amount is: ', self.positions)
        print('sold ethereums: ', sold_ethereums)
        print('earned ethereums: ', self.earned_ethereums)

    def currentMadeProfit(self, price):
        return ((self.earned_ethereums * price) / self.initial_capital) * 100

    def clearPositions(self, price):
        if self.positions > 0:
            self.sell(price)

    def printResults(self, price):
        print('Amount of Ethereum gained from trading: ', self.earned_ethereums)
        print('Return: ',self.currentMadeProfit(price), '%')


    def determineBuythreshold(self):
        '''
        TODO: Implement the adjustment based on sigma
        '''

        if self.sigma == 0:
            new_upsilon = self.static_upsilon
        elif self.sigma <= 0.01:
            new_upsilon = self.static_upsilon - 0.03
        elif self.sigma > 0.01 and self.sigma <= 0.025:
            new_upsilon = self.static_upsilon
        elif self.sigma > 0.025:
            new_upsilon = self.static_upsilon - 0.025

        
        return self.average_buy_price * (1 - new_upsilon)
    
    
    def determineBuyamount(self):
        '''
        TODO: can be optimized
        '''

        if self.sigma == 0:
            new_chi = self.static_chi
        elif self.sigma <= 0.01:
            new_chi = self.static_chi
        elif 0.01 < self.sigma <= 0.025:
            new_chi = self.static_chi
        elif self.sigma > 0.025:
            new_chi = self.static_chi + 0.03

        self.amount = self.initial_capital * new_chi

        return self.amount
    

    def determineSellthreshold(self):
        '''
        TODO: Implement the adjustment based on sigma
        '''

        if self.sigma == 0:
            new_psi = self.static_psi
        elif self.sigma <= 0.01:
            new_psi = self.static_psi - 0.025
        elif 0.01 < self.sigma < 0.025:
            new_psi = self.static_psi
        elif self.sigma >= 0.025:
            new_psi = self.static_psi - 0.015

        return self.average_buy_price * (1 + new_psi)
    

    def predictSigma(self, current_index):
        '''
        TODO Implement the function that predicts sigma
        '''
        long_term_vol = longTermVol(current_index = current_index,
                                    n_days = 30,
                                    df = self.df)
        short_term_vol = shortTermVol(current_index = current_index,
                                      t_1 = 300,
                                      df = self.df)
        return 0.25*long_term_vol+0.75*short_term_vol



    ##########################################################
    ################ This is the main loop ###################
    ##########################################################
    def run(self):
        for row in self.df.itertuples():
            current_index = row.Index
            price = row.close
            buy_amount = self.determineBuyamount()
            
            if self.positions == 0:
                self.buy(price, buy_amount)
                
            elif self.positions > 0:

                buy_threshold = self.determineBuythreshold()
                sell_threshold = self.determineSellthreshold()

                if price <= buy_threshold and self.positions < self.max_positions:
                    self.buy(price, buy_amount)

                elif price >= sell_threshold:
                    self.sell(price)

            '''
            TODO: if you want to adjust the sigma based on predictions, you could do it here for the next iteration
            Example: self.sigma = self.predictSigma() 
            Note: it might not be neccessary to call the model every iteration since the data is minute based
            '''
            if current_index % 60 == 0:
                self.sigma = self.predictSigma(current_index)
                if np.isnan(self.sigma):
                    self.sigma = 0

                    
        self.clearPositions(price)
        self.printResults(price)
        