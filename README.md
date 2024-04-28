# Large Language Models Application to Financial Portfolio Construction

## Introduction

This is the repository with code for the thesis work.

Applications of AI in the finance field are advancing with the development of AI itself. The Large Language Models are good at performing general tasks but must be tailored to excel in solving niche problems. The question researched in this work is whether LLMs can construct financial portfolios that outperform the benchmarks. The portfolios comprising 15 stocks from each of the S&P 500 sector indices are constructed by prompting three GPT models, Bard AI, and Claude 3. These models also assign weights to the stocks in the portfolios. The equally weighted and three optimised portfolios from the pre-selected stocks are also constructed for each model and each sector. The whole process results in 275 portfolios. Their performance is compared to the benchmarks - the sector indices - via different metrics.

## Usage

All the information on obtaining the data, constructing the portfolios, using the optimisation, analysis, and visualisation can be found in the thesis paper.

### Clone the repository

```
git clone https://github.com/linvieson/llm_financial_portfolio_construction
```

### Install the requirements

```
pip install -r requirements. txt
```

### Install cplex solver

[__IBM website__](https://www.ibm.com/docs/en/icos/20.1.0?topic=cplex-setting-up-python-api) has the instructions.

Install CPLEX solver. To setup CPLEX solver for Python:
* Use the script `setup.py` located in the directory `yourCPLEXhome/python`
* Execute the following command from the command line `python yourCPLEXhome/python/setup.py install` or `python yourCPLEXhome/python/setup.py install --home yourPythonPackageshome`
* Set the environment variable `PYTHONPATH` to `yourCPLEXhome/python/VERSION/PLATFORM`

### Set up thte OpenAI API key

Get the API key from OpenAI for GPT models usage. Create a file __api_key.txt__ in the directory of the project, add your API key there.

### Run the code

After you are all set, you can run the code. The __cached__ directory has all the main data on the portofolios cached for the optimisation purposes. When you run the code, that data will be used.

Some modules have parameters at the beginning of them to be configured for each sector and model. Instructions are provided within such modules. Normally, if you want to process, for example, sector Energy, you comment all the cells with other sectors and uncomment the Energy sector cell. Works the same with every sector. If you want to choose a specific model, uncomment the row in the cell with this model and comment the other rows with other models.

If you want to run the code using the API and not using the cached data, delete the files (or directories) that you want to regenerate and run the code. The requests to the GPT models will be sent using your API key.

Regarding Bard and Claude models, no API keys were provided for them. In order to create the portfolios from scratch, you need to use the web interface. After each response, paste the string in the corresponding place in the code and run the code. You will need to do this all manually. Because of this specifics with the approach of constructing the portofolios, the [__process_bard_and_claude_avg.ipynb__](https://github.com/linvieson/llm_financial_portfolio_construction/blob/main/process_bard_and_claude_avg.ipynb) module is left as it was used to process Real Estate sector as an example.

If you construct portfolios from scratch, the files will be saved to your new __cached/__ dicrectory for future usage.


## Modules

- [__portfolio_construction.ipynb__](https://github.com/linvieson/llm_financial_portfolio_construction/blob/main/portfolio_construction.ipynb): construct the portfolios with three GPT models (GPT-3.5, GPT-4, GPT-4 preview) through APIs.
- [__process_bard_and_claude_avg.ipynb__](https://github.com/linvieson/llm_financial_portfolio_construction/blob/main/process_bard_and_claude_avg.ipynb): construct the portfolios with Bard AI and Claude 3. The responses have been gathered manually, hence the notebook contains processing of these responses rather than all the tools for from-scratch obtainment of the portfolios with these models.
- [__portfolio_analysis.ipynb__](https://github.com/linvieson/llm_financial_portfolio_construction/blob/main/portfolio_analysis.ipynb): notebook for analysing the portfolios constructed prior with 5 LLMs.
- [__metrics_analysis.ipynb__](https://github.com/linvieson/llm_financial_portfolio_construction/blob/main/metrics_analysis.ipynb): notebook for analysing portfolio performance using different metrics, and visualising the results.
- [__index_cumulative_returns.ipynb__](https://github.com/linvieson/llm_financial_portfolio_construction/blob/main/index_cumulative_returns.ipynb): calculation of the specific metric on sector indices.
- [__average_weight_calculator.py__](https://github.com/linvieson/llm_financial_portfolio_construction/blob/main/average_weight_calculator.py): module with the functions used for average weight calculation on the stage of LLM portfolio construction.

## Directories and files
- [__4_returns_insample__/](https://github.com/linvieson/llm_financial_portfolio_construction/tree/main/4_returns_insample): in-sample period (5 years prior to April 2023) data on stock returns, all stocks from S&P 500 index.
- [__4_returns_outsample__/](https://github.com/linvieson/llm_financial_portfolio_construction/tree/main/4_returns_outsample): out-of-sample period (April 2023 - December 2023) data on stock returns, all stocks from S&P 500 index
- [__cached/__](https://github.com/linvieson/llm_financial_portfolio_construction/tree/main/cached): all the data on LLM responses on portfolios saved for the optimisation purposes and convenient analysis.
- [__metrics/__](https://github.com/linvieson/llm_financial_portfolio_construction/tree/main/metrics): folder with files containing the metric results.

- [__SP500.csv__](https://github.com/linvieson/llm_financial_portfolio_construction/blob/main/SP500.csv): data on the companies from S&P 500 index
- [__tickers.csv__](https://github.com/linvieson/llm_financial_portfolio_construction/blob/main/tickers.csv): data on the tickers of the companies and the sectors to which these companies belong (GICS)

## Results

 After comparing the cumulative returns of the portfolios with the cumulative returns of the sector indices, the results were found to be that there are three sectors in which LLMs fail to construct good portfolios and eight sectors in which LLMs happened to be good stock-selectors. Different metrics are considered to understand the logic behind such results and LLMs’ reasons for such portfolio selections. The hypothesis to be accepted is that in the sectors where LLMs fail to construct competitive portfolios, the sector indices themselves perform very well - so it is hard for LLM to choose only 15 stocks to outperform the good-performing index. When portfolios are compared to the sector indices by risk measures (Sharpe ratio), LLMs outperform the sector index in every sector.

## Demonstration

The video with the demonstration of work of the code can be found by following the [__link__] (YouTube video).

