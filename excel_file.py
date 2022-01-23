import pandas as pd

invoice_info_list_full = []


def create_csv(invoice_num, client_name, invoice_amount, output_path):
    # put each piece of data into a local list, also replaces : with / since Python saves files with : as / from dirs
    invoice_info_list = invoice_num.replace(':', '/'), client_name, invoice_amount
    # add the local list to the global list (creates a nested list)
    invoice_info_list_full.append(invoice_info_list)

    # creates a dataframe using the nested list from above
    df = pd.DataFrame(invoice_info_list_full)
    # saves the database as a csv file
    df.to_csv(f"{output_path}invoice_list.csv", index=False)
