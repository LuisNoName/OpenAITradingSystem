# Trading System

This framework has been built with the idea of managing a portfolio of portfolios. It allows the user to code his own strategies, data providers, portfolio managers and so on.  
The system is designed around 6 abstract classes: `AbstractDataProvider`, `AbstractStrategy`, `AbstractPortfolio`, `AbstractPortfolioManager`, `AbstractTrader` and `AbstractLogger`. These classes need to be implemented by the user (or one can also use some factory implementations provided here). The nice thing about this way of deigning the trading system is its modularity and implementation independence.  
Different implementations of various classes can be swiftly replaced by newer implementations, which includes easy wtiching from one Broker to another, Backtesting to Live execution etc.  
This design as well as a heavy part of the implementation has been created with the help of the OpenAI ChatGTP.
<br>

## How it all works
The idea behind the design is pretty straightforward and the development process can easily be explained in the following few steps:
1. `AbstractDataProvider` is a class for feeding data to different strategies of the portfolio. Every single external datapoint comes from this class.
2. `AbstractStrategy` is class where a single strategy is implemented. This class uses the `AbstractDataProvider` to get its data.  
3. `AbstractPortfolio` and `AbstractPortfolioManager` work closely together, but have different roles to play. The `AbstractPortfolio` is a class that handles all the strategies (`AbstractStrategy`) in the portfolio. It provides info about the current strategies and allows the user to add or remove strategies (`AbstractStrategy`) from the portfolio.  
The `AbastractPortfolioManager` class, on the other hand, handles the rebalancing of the portfolio and directly works with the `AbstractTrader` class, i.e., it serves as a 'bridge' between the Portfolio and the Broker.
4. `AbstractTrader` class implements all the logic behind sending orders, recieving messages from the broker etc. The idea is that the rest of the code be indifferent to which Broker is being used.
5. Finally, `AbstractLogger` is a helper class that could be used for various logging purposes, e.g. sending e-mails of succesfully completed trades etc.

The information below explains in more detail what each class does and what its methods and properties are.

## AbstractDataProvider Class

The DataProvider class is responsible for providing data to the rest of the trading system. It retrieves data from external sources and makes it available to the other classes in the system. The main usage of the `AbstractDataProvider` class will be inside of `AbstractStrategy`. Therefore, the implementation is not very strict. One can freely add as many custom methods as one needs in order to make the asset allocation procces in the `AbstractStrategy` class as simple and straightforward as possible.

### Constructors

- `__init__(self, data_sources: List[str]) -> None`: initializes the DataProvider with a list of data sources to use.
    - Parameters  
    `data_sources`: The list of data sources to use.

### Methods

 - `get_price_data(self, assets: List[str], start_date: datetime, end_date: datetime) -> Dict[str, pd.DataFrame]`: retrieves price data for a given list of assets over a specified time period. 
    - Parameters  
        `assets`: The list of assets for which to retrieve price data.  
        `start_date`: The start date of the time period.  
        `end_date`: The end date of the time period.  
    - Returns a dictionary with the asset symbols as keys and the price data as values, in the form of Pandas `DataFrame`.  
- `get_fundamental_data(self, assets: List[str]) -> Dict[str, pd.DataFrame]`: retrieves fundamental data for a given list of assets.
   - Parameters  
        `assets`: The list of assets for which to retrieve fundamental data.  
        `start_date`: The start date of the time period.  
        `end_date`: The end date of the time period.  
    - Returns a dictionary with the asset symbols as keys and the fundamental data as values, in the form of Pandas `DataFrame`.
- `get_market_data(self) -> pd.DataFrame`
    This method retrieves market data, such as indices or exchange rates.
    - Returns the market data in the form of a Pandas `DataFrame`.

### Properties
 - TBA 

<br>

## AbstractStrategy Class
The `AbstractStrategy` class is responsible for defining the investment strategies used by the portfolio. It determines the assets to be included in a single strategy and the weights assigned to each asset. The word 'strategy' might be a slightly problematic, since in this case 'strategy' implies one 'small portfolio'. The reason behind this choice is that in the future versions, extensions to real trading strategies (e.g. technical trading, options trading...) are planned.  
Nevertheless, this class handles all the logic of a single strategy. Here, the user is defining what assets this strategy can invest in as well as all the logic regarding the asset selection and allocation. Since this is generally the most creative part of investing, the class does not have a very strict form. The only important things (from the perspective of the trading system) are the weights and risk/return metrics of the strategy. The logic of how the assets are selected it completely up to the user to implement freely.

### Constructors

`__init__(self, data_provider: AbstractDataProvider) -> None`: constructor for the Strategy class.
    - Parameters  
    `data_provider`: An instance of a DataProvider class that provides data for the strategy.

### Methods

 - `get_asset_universe(self) -> List[str]`: returns the list of assets included in the investment strategy.
 - `rebalance(self) -> None`: rebalances the portfolio according to the defined investment strategy.
 - `get_risk(self) -> float`: returns the risk of the portfolio according to the defined investment strategy.
 - `get_returns(self) -> float`: returns the expected returns of the portfolio according to the defined investment strategy.
 - `get_VaR(self, alpha: float) -> float`: returns the $VaR_{alpha}$
### Properties

 - `asset_universe: List[str]`: a list containing all the assets that the strategy can invest in  
 - `strategy_weights: Dict[str, float]`: a list containing the names and weights of all assets that are in the current strategy's portfolio.  
 - `expected_risk: float`: the yearly volatility of the current strategy's portfolio
 - `expected_return: float`: the yearly expected return of the current strategy's portfolio

<br>

## AbstractPortfolio Class
The `AbstractPortfolio` class is responsible for representing the portfolio of strategies (`AbstractStrategy`) managed by the Trading System. It receives updates from `AbstractPortfolioManager` and reflects the current state of the portfolio.  
Here, one can add and remove strategies, monitor risk/return metrics etc.

### Constructor

 - `__init__(self, data_provider: AbstractDataProvider, strategies: List[AbstractStrategy]) -> None`: creates a new Portfolio instance.
    - Parameters  
    `data_provider`: The data provider to be used by the portfolio.
    `strategies: List[AbstractStrategy]`: The list of strategies in this portfolio.

### Methods

 - `set_portfolio(self, assets: List[str], weights: List[float]) -> None`: sets the portfolio to a given list of assets and weights.
    - Parameters  
    `assets`: The list of assets in the portfolio.  
    `weights`: The corresponding weights for each asset. The weights should sum to 1.  
 - `add_strategy(self, strategy: AbstractStrategy) -> None  `: adds the strategies to the current portfolio.
    - Parameters  
    `strategy`: An instance of the implemented `AbstractStrategy` class.  
 - `remove_strategy(self, strategy: AbstractStrategy) -> None`: removes the strategy from the current portfolio.
    - Parameters  
    `strategy`: An instance of the implemented `AbstractStrategy` class.  
 - `get_risk(self) -> float`: returns the risk of the portfolio.  
 - `get_returns(self) -> float`: returns the expected returns of the portfolio.  
 - `rebalance(self) -> None`: rebalances the portfolio to the target weights.
  
### Properties
 - `strategies: List[AbstractStrategy]`: list of strategies that are in the portfolio  
 - `portfolio_weights: List[float]`: list of weights assigned to each portfolio (should add up to 1)
 - `data_provider`: instance of `AbstractDataProvider` that provides data to the portfolio 


<br>

## AbstractPortfolioManager Class
 
The `AbstractPortfolioManager` class is responsible for optimizing the portfolio (instance of `AbstractPortfolio`) of strategies (instances of `AbstractStrategy`) based on the given constraints. In the method `rebalance`, the `AbstractPortfolio.weights` property is being optimized and orders are sent to the broker.  
There is also some functionality around adding and removing constraints to make the process flexible. Since each instance of `AbstractStrategy` has its own instance of `AbstractDataProvider`, the `PortfolioManager` does not have its own `AbstractDataProvider` instance.

### Constructor

- `__init__(self, trader: AbstractTrader, portfolio: AbstractPortfolio, log: AbstractLogger)`: initializes the `PortfolioManager` with a `DataProvider`, `Trader`, `Portfolio`, and `Logger`.

    - Parameters
    `data_provider`: The DataProvider to be used by the PortfolioManager.
    `trader`: The Trader to be used by the PortfolioManager.
    `portfolio`: The Portfolio to be managed by the PortfolioManager.
    `log`: The Logger to be used by the PortfolioManager.

### Methods

 - `rebalance(self) -> None`: rebalances the portfolio based on the given constraints in the `constraints` property of the class
 - `add_constraint(self) -> None`: adds a specific constraint to be used when optimizing the portfolio of strategies
 - `remove_constraint(self) -> None`: removes a specific constraint  
 - `set_constraints(self, Dict[str,float]) -> None`: adds a whole dictionary of constraints to the `constraints` property of the class  
 - `get_constraints(self) -> Dict[str, float]`: returns the `constraints` dictionary.
 - `change_trader(self, new_trader: AbstractTrader) -> None`: changes the trader being used in the rebalancing
### Properties
 - `constraints: Dict[str, float]`: a dictionary containing all the constraints on the whole portfolio, i.e., `max_risk`, `min_expected_return`, `min_cash_weight` etc.
 - `trader`: The Trader to be used by the PortfolioManager
 - `portfolio`: The Portfolio to be managed by the PortfolioManager
 - `log`: The Logger to be used by the PortfolioManager

<br>

## AbstractTrader Class

The Trader class is responsible for executing trades on behalf of the portfolio. It receives orders from the PortfolioManager and submits them to the exchange. It also keeps track of the portfolio's balance and positions.

### Methods

- `get_balance(self) -> float`: returns the current balance of the portfolio.
- `submit_order(self, asset: str, quantity: int, order_type: str, price: Optional[float] = None) -> Union[Dict[str, Any], str]`: submits an order to the exchange.
    - Parameters  
    `asset`: The asset to be traded.  
    `quantity`: The number of assets to be traded.  
    `order_type`: The type of order (e.g. "market", "limit").  
    `price`: The price at which the order should be executed (optional).  

    - Returns a dictionary containing information about the order (e.g. order ID, execution price), or a string indicating an error.  
 - `get_position(self, asset: str) -> Dict[str, Any]`: returns information about the portfolio's position in a given asset.
    - Parameters  
    `asset`: The asset for which to retrieve the position.
    - Returns a dictionary containing information about the position (e.g. quantity, average price).
 - `get_execution(self, order_id: str) -> Dict[str, Any]`: returns information about the execution of a given order.
    - Parameters  
    `order_id`: The ID of the order for which to retrieve the execution.  
    - Returns a dictionary containing information about the execution (e.g. execution price, fill quantity).
    
<br>

## AbstractLogger Class

The Logger class is responsible for logging messages and data in a way that is easily accessible and searchable. It receives messages and data from various parts of the trading system and stores them in a way that is easy to review and analyze.

### Constructors

- `__init__(self, log_file: str) -> None`: initializes the Logger with a specified log file.
    - Parameters  
    `log_file`: the file to which the log entries will be written.

### Methods

- `log(self, message: str, data: Any = None) -> None`
This method logs a message with optional data.
    - Parameters
    `message`: The message to log.
    `data`: Optional data to include in the log entry.
    - Returns nothing.