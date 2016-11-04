## Fetches stock live data from google finance
## _P0W!

try:
    from urllib.request import *
except:
    from urllib import * 
import json
import time
import winsound
import copy

class GoogleFinanceStockGrabber(object):
    def __init__(self):
        self.prefix = "http://finance.google.com/finance/info?client=ig&q="

    def get(self,symbol):
        url = self.prefix+"%s"%(symbol)
        u = urlopen(url)
        content = u.read().decode('utf-8')
        
        obj = json.loads(content[3:])
        return obj

    def stockPrinter( self, symb ):
        print ( '\n%10s | %-6s : %10s (%8s %% ) < %s >' % (symb['t'], symb['e'], symb['l'], symb['cp'], symb['lt'] ) )
          
class StockChangeDetectorRunner(  GoogleFinanceStockGrabber ):
    def __init__(self, AllStocks):
        super(StockChangeDetectorRunner, self).__init__()
        self.AllStocks = copy.deepcopy(AllStocks)
        for _ in self.AllStocks:
            self.AllStocks[_] = 0.0
            
    def run(self):
        quote = self.get(','.join( self.AllStocks.keys() ) )
        for symb in quote:
            stockKey = '%s:%s' % ( symb['e'], symb['t'] )
            if symb['cp'] != self.AllStocks[ stockKey ]:
                self.AllStocks[ stockKey ] = symb['cp']
                self.stockPrinter( symb )
                
class BuyCallRunner( GoogleFinanceStockGrabber ):
    def __init__(self, AllStocks, Target ):
        super( BuyCallRunner, self).__init__()
        self.AllStocks = copy.deepcopy(AllStocks)
        self.target = Target
  
    def run(self):
        quote = self.get(','.join( self.AllStocks.keys() ) )
        total = 0.0
        for symb in quote:
            stockKey = '%s:%s' % ( symb['e'], symb['t'] )
            total += float(symb['l'].replace(',','')) * self.AllStocks[ stockKey ]
        
        if total < self.target:
            print ( 'Total = %.2f' % total )                
            winsound.Beep( 2500, 500 )
        
    
if __name__ == "__main__":
    
##    AllStocks = { 'NSE:PFS'    : 0.0,
##                  'NSE:STAR'   : 0.0,
##                  'NSE:INFY'   : 0.0,
##                  'NSE:SBIN'   : 0.0,
##                  'NSE:CANBK'  : 0.0,
##                  'NSE:BERGER' : 0.0,
##                  'NSE:DABUR'  : 0.0,
##                  'NSE:TATAMOTORS':0.0,
##                     }

    AllStocks = { 
               ## 'Exchange:Symbol' : Qty to buy
                  'BOM:509480'      : 25.0, ## Berger Paints    : 25.0,
                  'BOM:500233'      : 15.0, ##'NSE:KAJARIACER'  : 15.0,
                  'BOM:532540'      : 6.0,  ##'NSE:TCS'         : 6.0 ,
                  'BOM:532500'      : 2.0,  ##'NSE:MARUTI'      : 2.0 ,
                  'BOM:500096'      : 30.0  ##'NSE:DABUR'       : 30.0,
                  
                }
    
    changeDetector = StockChangeDetectorRunner(AllStocks)
    buycall = BuyCallRunner( AllStocks, 51000.0 )
    
    while True:
        try:
            changeDetector.run()
            buycall.run()
        except:
            print ('Failed to Fetch...' )
        time.sleep(5)
