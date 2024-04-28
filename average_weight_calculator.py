import pandas as pd
import numpy as np
import openai
import os

def calculate_weights_by_sector_average(sector_name, full_ticker, model, params, rerun=False):
    # if calculated average weights file already exists
    if model == 'gpt-4':
        csv_path = f'cached/4_avg_weights_assigned/responses15_auto_{sector_name}.csv'
    elif model == 'gpt-4-1106-preview':
        csv_path = f'cached/4preview_avg_weights_assigned/responses15_auto_{sector_name}.csv'
    else:
        csv_path = f'cached/3_avg_weights_assigned/responses15_auto_{sector_name}.csv'

    if os.path.isfile(csv_path) and not rerun:
        print("Reading from local csv file")
        print(pd.read_csv(csv_path))
        return pd.read_csv(csv_path)

    # otherwise calculate avg weights from scratch
    max_tokens, n, stop, temperature = params

    if model == 'gpt-4':
        csv_path_read = f'cached/4_sectors/stocks15_auto_{sector_name}.csv'
    elif model == 'gpt-4-1106-preview':
        csv_path_read = f'cached/4preview_sectors/stocks15_auto_{sector_name}.csv'
    else:
        csv_path_read = f'cached/3_sectors/stocks15_auto_{sector_name}.csv'

    sector_df = pd.read_csv(csv_path_read)

    temp_df = sector_df[sector_df['IsValid'] == 1]
    input = temp_df['Stocks'].to_list()
    print(input)

    responses = []

    for i in range(5):
        prompt3 = f"Assume you're designing a theoretical model portfolio from these {full_ticker} {sector_name} stocks: {input}. Provide a hypothetical example of how you might distribute the weightage of these stocks (normalized i.e weights should add up to 1.00) in the portfolio to potentially outperform the {full_ticker} {sector_name} index. Also mention the underlying strategy or logic which you used to assign these weights"

        response3 = openai.ChatCompletion.create(
            model=model,
            messages=[
            {"role": "system", "content": "You are a helpful assistant. Your task is to create a hypothetical allocation of weights to the stocks in a theoretical investment fund."},
            {"role": "user", "content": prompt3},
            ],
            max_tokens=max_tokens,
            n=n,
            stop=stop,
            temperature=temperature,
        )

        coutput3 = response3['choices'][0]['message']['content']

        prompt4 = f'Extract tickers of stocks and corresponding weights as a single comma "," separated string, with the weights expressed as floats : "{coutput3}". Provide a list of type TICKER: weight, no extra symbols used.'

        print(f'calling openai for response to prompt 4 sector {sector_name}')
        response4 = openai.ChatCompletion.create(
            model=model,
            messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt4},
            ],
            max_tokens=max_tokens,
            n=n,
            stop=stop,
            temperature=temperature,
        )

        coutput4 = response4['choices'][0]['message']['content']
        print(coutput4.strip('"'))

        if 'Sure' in coutput4:
            coutput4 = coutput4.strip('\n')[1]

        responses.append(coutput4)

        # data_dict = {key.strip(): float(value.strip()) for key, value in (pair.split(":") for pair in coutput4.split(","))}
        data_dict = dict()

        pairs = coutput4.split(',')

        for pair in pairs:
            stock, weight = pair.split(':')

            stock = stock.lstrip()
            if "\"" in stock: stock = stock.strip("\"")
            if "\'" in stock: stock = stock.strip("\'")

            weight = weight.lstrip()
            if "\"" in weight: weight = weight.strip("\"")
            if "\'" in weight: weight = weight.strip("\'")

            data_dict[str(stock).strip()] = float(weight.strip())


        if model == 'gpt-4':
            csv_path_write_avg = f'cached/4_avg_weights_response/responses15_auto_{sector_name}.csv'
        elif model == 'gpt-4-1106-preview':
            csv_path_write_avg = f'cached/4preview_avg_weights_response/responses15_auto_{sector_name}.csv'
        else:
            csv_path_write_avg = f'cached/3_avg_weights_response/responses15_auto_{sector_name}.csv'

        if os.path.isfile(csv_path_write_avg):
            print("Adding weights to file")

            existing_df = pd.read_csv(csv_path_write_avg)
            new_df = pd.DataFrame(list(data_dict.items()), columns=['Stock', f'Weight_{i}'])

            # check if the 'asset' column in the existing DataFrame matches the keys in the parsed data
            common_assets = set(existing_df['Stock']).intersection(set(data_dict.keys()))

            existing_df[f'Weight_{i}'] = existing_df['Stock'].map(lambda x: data_dict[x] if x in common_assets else None)

            new_assets = set(data_dict.keys()).difference(set(existing_df['Stock']))
            new_df = new_df[new_df['Stock'].isin(new_assets)]
            
            final_df = pd.concat([existing_df, new_df], ignore_index=True)
            final_df.to_csv(csv_path_write_avg, index=False)

        else:
            print("Creating a file to keep weights from responses")
            new_df = pd.DataFrame(list(data_dict.items()), columns=['Stock', f'Weight_{i}'])
            new_df.to_csv(csv_path_write_avg, index=False)


    print("Calculating averages")
    avg_weights_response_df = calculate_avg_weights(responses, input)

    if model == 'gpt-4':
        csv_path_write = f'cached/4_avg_weights_assigned/responses15_auto_{sector_name}.csv'
    elif model == 'gpt-4-1106-preview':
        csv_path_write = f'cached/4preview_avg_weights_assigned/responses15_auto_{sector_name}.csv'
    else:
        csv_path_write = f'cached/3_avg_weights_assigned/responses15_auto_{sector_name}.csv'
    
    avg_weights_response_df.to_csv(csv_path_write, index=False)

    return avg_weights_response_df


def calculate_avg_weights(responses, stock_list):
    stock_dict = {str(stock): [] for stock in stock_list}

    for response in responses:
        pairs = response.split(',')

        for pair in pairs:
            stock, weight = pair.split(':')

            stock = stock.lstrip()
            if "\"" in stock: stock = stock.strip("\"")
            if "\'" in stock: stock = stock.strip("\'")

            weight = weight.lstrip()
            if "\"" in weight: weight = weight.strip("\"")
            if "\'" in weight: weight = weight.strip("\'")

            stock_dict[str(stock)].append(float(weight))

    averages = {str(stock): sum(weights) / len(weights) for stock, weights in stock_dict.items()}
    print(averages)

    df = pd.DataFrame()
    stocks, weights = [], []

    for stock, weight in averages.items():
        stocks.append(str(stock))
        weights.append(float(weight))

    df = pd.DataFrame({'Stock': stocks, 'Weight': weights})

    if not np.isclose(df['Weight'].sum(), 1):
        df['Weight'] = df['Weight'] / df['Weight'].sum()

    return df


