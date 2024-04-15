import re
import pandas as pd

def find_missing_invoices(series):
    a = series.str.split("-").str[-1].str[-7:].str.strip()
    a = a.dropna()
    invoices = sorted(a.apply(lambda x: re.sub(r'[^0-9]', '', str(x))).replace('', '0').astype(int))
    
    missing_invoices = []
    prev_invoice = invoices[0] - 1  # Initialize to a value before the first invoice
    
    for invoice in invoices:
        diff = invoice - prev_invoice
        if diff <= 100:
            if diff > 2:
                # If there's a gap larger than 1, include a range instead of single missing invoices
                missing_range = f"{prev_invoice + 1}-{invoice - 1}"
                missing_invoices.append(missing_range)
            if diff == 2:
                # If there's a gap larger than 1, include a range instead of single missing invoices
                missing_range = f"{prev_invoice + 1}"
                missing_invoices.append(missing_range)
        
        prev_invoice = invoice
    
    return missing_invoices

def main(df):
    # Convert created_date_time to datetime
    df['created_date_time'] = pd.to_datetime(df['created_date_time'])
    
    # Extract date, hour, location, ntn, and pos_id from the data
    df['date'] = df['created_date_time'].dt.date
    df['hour'] = df['created_date_time'].dt.hour
    
    result_list = []

    for (pos_id,ntn,location,date,hour), group in df.groupby(['pos_id','ntn','location','date', 'hour',]):
        invoices = group['invoice_no']
        
        # Find missing invoices or gaps in ranges
        missing_or_gaps = find_missing_invoices(invoices)
        
        # Join missing invoices or gaps in ranges into a comma-separated string
        missing_invoices_str = ','.join(missing_or_gaps)
        
        # Combine date and hour into a single datetime field
        date_time = pd.to_datetime(f"{date} {hour}:00:00")
        
        # Only add the entry if missing_invoices_str is not empty
        if missing_invoices_str:
            result_dict = {
                'date': date_time,
                'location': location,
                'ntn': ntn,
                'pos_id': pos_id,
                'invoices': missing_invoices_str
            }
            result_list.append(result_dict)

    return result_list