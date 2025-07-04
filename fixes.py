import pandas as pd
from decimal import Decimal
from collections import Counter, defaultdict
from product_class import Product
import math


BAD_CHARS = set("',%")

VAT_CODES = {0.0: 0,
             23.0: 1,
             13.5: 2,
             9.0: 3}



def fix_description(df: pd.DataFrame):
    """Remove any bad characters and cut description down to 50 characters"""
    df_fixed = df.copy()
    changes = []
    for i, desc in df_fixed['description'].items():
        if isinstance(desc, str):
            og_desc = desc
            cleaned = ''.join(c for c in desc if c not in BAD_CHARS)
            final = cleaned

            if og_desc != cleaned:
                changes.append(f"Line {i+2} \u00A0\u00A0|\u00A0\u00A0 Bad characters removed from description: '{og_desc}', updated to '{cleaned}'")
                        
            if len(cleaned) > 50:
                final = cleaned[:50]
                changes.append(f"Line {i+2} \u00A0\u00A0|\u00A0\u00A0 Long description: '{og_desc}' shortened to '{final}'")
            
            if desc != final:
                df_fixed.at[i, 'description'] = final
    return df_fixed, changes
            


def fix_decimals(df: pd.DataFrame):
    """Update the decimal rounding/format to the correct 2 decimal places"""
    df_fixed = df.copy()
    columns = ['costprice', 'rrp', 'sellingprice', 'stgprice']
    changes = []
    for column in columns:
        for i, num in df_fixed[column].items():
            if isinstance(num, (int, float)) and not math.isnan(num):
                decimal_val = Decimal(str(num))
                if -decimal_val.as_tuple().exponent > 2:
                    new_num = round(num, 2)
                    df_fixed.at[i, column] = new_num
                    changes.append(f"Line {i+2} \u00A0\u00A0|\u00A0\u00A0 {column} of {num} rounded to {new_num}")
    return df_fixed, changes


def fix_vat(df: pd.DataFrame):
    """Assign the correct VAT codes for given percentages"""
    df_fixed = df.copy()
    changes = []
    for i, vat in df_fixed['vatrate'].items():

        if vat in VAT_CODES:
            new_vat = VAT_CODES[vat]
            df_fixed.at[i, 'vatrate'] = new_vat
            changes.append(f"Line {i+2} \u00A0\u00A0|\u00A0\u00A0 VAT Rate {vat} updated to code {new_vat}")
    return df_fixed, changes



def update_all(df: pd.DataFrame):
    """Call fix functions and returns updated dataframe (a copy)"""
    df1, desc_changes = fix_description(df)
    df2, decimal_changes = fix_decimals(df1)
    df3, vat_changes = fix_vat(df2)
    # print("Final columns available:", df.columns.tolist())

    return df3, desc_changes + decimal_changes + vat_changes





