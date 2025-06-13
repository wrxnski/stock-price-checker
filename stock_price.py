import yfinance as yf
import time
import os
import colorama
import contextlib
import io

colorama.init()

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

DELAY_SEC_2 = 1

def clear_and_print_header():
    """Clears terminal and prints the header Check Stock Prices📊"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Check Stock Prices📊\n")

def space():
    """Prints a blank line adding readability"""
    print()

def get_stock_price(ticker_symbol, period):
    """Returns price for given ticker and time period with additional info"""
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            stock = yf.Ticker(ticker_symbol)
            info = stock.info
            price_latest = stock.fast_info["lastPrice"]
            stock_name = info.get("shortName", ticker_symbol.upper())

        if period == "now":
            space()
            print(f"{BOLD}{stock_name}{RESET} ({ticker_symbol}) {BOLD}Latest Price{RESET}")
            print("-----------------------------------------------------")
            print(f"Real Time Price: ${price_latest:,.2f}")
            return
        
        data = stock.history(period=period, auto_adjust=True, back_adjust=True)
  
        close_prices = data['Close'].dropna()

        if close_prices.empty:
            space()
            time.sleep(DELAY_SEC_2)
            error_message_print(ticker_symbol, period)
            return
        
        price_start = close_prices.iloc[0]
        price_end = close_prices.iloc[-1]

        date_start = close_prices.index[0].date()
        date_end = close_prices.index[-1].date()

        price_open = data['Open'].iloc[0]
        price_close = data['Close'].iloc[-1]

        if period == "1d":
            print(f"{BOLD}{stock_name}{RESET} ({ticker_symbol}) Price Summary over: {BOLD}{period}{RESET}")
            print("------------------------------------------------------")
            print(f"{date_start.strftime('%d %b %Y')} Open: ${price_open:,.2f}")
            print(f"{date_end.strftime('%d %b %Y')} Close: ${price_close:,.2f}")
            price_change = price_close - price_open
            percentage_change = (price_change / price_open) * 100

        else:
            print(f"{BOLD}{stock_name}{RESET} ({ticker_symbol}) Price Summary over: {BOLD}{period}{RESET}")
            print("------------------------------------------------------")
            print(f"{date_start.strftime('%d %b %Y')}: ${price_start:,.2f}")
            print(f"{date_end.strftime('%d %b %Y')}: ${price_end:,.2f}")
            price_change = price_end - price_start
            percentage_change = (price_change / price_start) * 100

        if percentage_change > 0:
            print(f"Change: {BOLD}{GREEN}+${price_change:,.2f} ({percentage_change:,.2f}%) 📈{RESET}")
        elif percentage_change < 0:
            print(f"Change: {BOLD}{RED}${price_change:,.2f} ({percentage_change:,.2f}%) 📉{RESET}")
        else:
            print(f"Change: {BOLD}{YELLOW}${price_change:,.2f} ({percentage_change:,.2f}%) ➖{RESET}")

    except Exception as e:
        message_error = str(e).lower()
        if "404" in message_error or "no price data" in message_error:
            space()
            error_message_print(ticker_symbol, period)
        else:
            print(f"Error getting data for {ticker_symbol}: {str(e)}")

def valid_periods():
    return ["now", "1d", "5d", "1mo", "3mo", "6mo", "ytd", "1y", "2y", "5y", "10y", "max"]

def clear_and_print_header_enter_ticker(ticker):
    """Clears terminal but keeps Enter Ticker: """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Check Stock Prices📊\n")
    print(f"Enter Ticker: {ticker}\n")

def error_message_print(ticker_symbol, period):
    """Prints out a message saying there is no data for teh entered ticker"""
    print(f"No data found for {ticker_symbol} in the period {period}")
    time.sleep(DELAY_SEC_2)
    print("------------------------------------------------------")
    print("This could mean:")
    print("- The ticker is incorrect or inactive")
    print("- The stock is delisted")
    print("- No trading activity in the selected period")

def main():
    """Stock Price Checker! Returns prices after entering ticker and period"""
    while True:
        
        clear_and_print_header()

        enter_ticker = input("Enter Ticker: ").strip().upper()
        while not enter_ticker:
            clear_and_print_header()
            enter_ticker = input("Please enter a valid ticker: ").strip().upper()

        while True:

            enter_period = input("Enter Time Period(now, 1d, 5d, 1mo, 3mo, 6mo, ytd, 1y, 2y, 5y, 10y, max): ").lower().strip()
            periods = valid_periods()

            while enter_period not in periods:
                clear_and_print_header()
                enter_period = input(f"Invalid period. Choose from ({', '.join(periods)}): ").lower().strip()
            
            clear_and_print_header()

            get_stock_price(enter_ticker, enter_period)
            print("------------------------------------------------------")
            time.sleep(DELAY_SEC_2)
            choice_next = input(f"{BOLD}[P]{RESET} Change Period {BOLD}[S]{RESET} New Stock {BOLD}[X]{RESET} Exit App: ").upper().strip()

            while choice_next not in ["P", "S", "X"]:
                space()
                choice_next = input("Invalid input. Please choose (P, S, X): ").upper().strip()
                                
            clear_and_print_header()
            if choice_next == "P":
                clear_and_print_header_enter_ticker(enter_ticker)
            elif choice_next == "S":
                break
            elif choice_next == "X":
                print("See you next time!")
                return
        
if __name__ == "__main__":
    main()