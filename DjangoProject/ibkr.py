from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.wrapper import EWrapper
from ibapi.client import EClient
import threading

class TestWrapper(EWrapper):
    def __init__(self):
        print("TestWrapper")

class TestClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)

    def placeOrder(self, orderId, ticker, numShares):
        print("placeOrder")

        # create order
        order = Order()
        order.action = "BUY"
        order.orderType = "MKT"
        order.totalQuantity = numShares

        # create contract
        contract = Contract()
        contract.symbol = ticker
        contract.secType = "STK"
        contract.exchange = "NYSE"

        super(TestClient, self).placeOrder(orderId, contract, order)
        print("placed order id: ", orderId)

class TestApp(TestWrapper, TestClient):
	def __init__(self):
		TestWrapper.__init__(self)
		TestClient.__init__(self, wrapper=self)
        	# 4002 for gateway
        	# 7497 for TWS
		self.connect("127.0.0.1", 7497, clientId=0)
 
	def nextValidId(self, orderId: int):
		print("nextValidId called")
		self.nextValidOrderId = orderId
		print("NextValidId:", orderId)

	def buy(self, ticker, numShares):
		self.placeOrder(self.nextValidOrderId, ticker, numShares)
		self.nextValidOrderId += 1

def exec():
        print("exec called")
        app.run()
        print("exec")

app = TestApp()
t1 = threading.Thread(target=exec)
t1.start()

def buy(ticker, numShares):
	print("buy called")
	app.buy(ticker, numShares)
