import streamlit as st

def calculate_actual_price_with_charges(shares, price_per_share, transaction_type, brokerage_rate=1.35, vat_rate=7.5, sec_fees_rate=0.3, stamp_duties_rate=0.08, ngx_fees_rate=0.3, ngx_vat_rate=0.0225, cscs_fees_rate=0.3, cscs_vat_rate=0.0225):
    # Calculate total consideration
    total_consideration = round(shares * price_per_share, 2)

    cscs_x_alert_fees = 4  # Flat fee in Naira

    if transaction_type == 'buy':
        # Calculate buying charges
        brokerage_commission = round(total_consideration * (brokerage_rate / 100), 2)
        vat_on_brokerage = round(brokerage_commission * (vat_rate / 100), 2)
        sec_fees = round(total_consideration * (sec_fees_rate / 100), 2)
        stamp_duties = round(total_consideration * (stamp_duties_rate / 100), 2)
        total_charges = round(brokerage_commission + vat_on_brokerage + sec_fees + stamp_duties + cscs_x_alert_fees, 2)
    else:
        # Calculate selling charges
        brokerage_commission = round(total_consideration * (brokerage_rate / 100), 2)
        vat_on_brokerage = round(brokerage_commission * (vat_rate / 100), 2)
        ngx_fees = round(total_consideration * (ngx_fees_rate / 100), 2)
        ngx_vat = round(total_consideration * (ngx_vat_rate / 100), 2)
        cscs_fees = round(total_consideration * (cscs_fees_rate / 100), 2)
        cscs_vat = round(total_consideration * (cscs_vat_rate / 100), 2)
        stamp_duties = round(total_consideration * (stamp_duties_rate / 100), 2)
        total_charges = round(brokerage_commission + vat_on_brokerage + ngx_fees + ngx_vat + cscs_fees + cscs_x_alert_fees + cscs_vat + stamp_duties, 2)

    contract_total = round(total_consideration - total_charges if transaction_type == 'sell' else total_consideration + total_charges, 2)
    actual_price_per_share = round(contract_total / shares, 2)

    return {
        "Total Consideration": total_consideration,
        "Total Charges": total_charges,
        "Contract Total (Net)": contract_total,
        "Actual Price per Share": actual_price_per_share
    }

def calculate_profit(shares, buying_price_per_share, selling_price_per_share, brokerage_rate=1.35, vat_rate=7.5):
    buying_info = calculate_actual_price_with_charges(shares, buying_price_per_share, 'buy', brokerage_rate, vat_rate)
    selling_info = calculate_actual_price_with_charges(shares, selling_price_per_share, 'sell', brokerage_rate, vat_rate)

    profit = round(selling_info["Contract Total (Net)"] - buying_info["Contract Total (Net)"], 2)
    percentage_gain_loss = round(((selling_info["Actual Price per Share"] - buying_info["Actual Price per Share"]) / buying_info["Actual Price per Share"]) * 100, 2)

    return buying_info, selling_info, profit, percentage_gain_loss

# Streamlit App
st.title("Stock Profit Calculator")

shares = st.number_input("Number of Shares", min_value=1)
buying_price_per_share = st.number_input("Buying Price per Share", min_value=0.0, format="%.2f")
selling_price_per_share = st.number_input("Selling Price per Share", min_value=0.0, format="%.2f")

# Optional: Allow user to modify the charges
brokerage_rate = st.number_input("Brokerage Rate (%)", min_value=0.0, value=1.35, format="%.2f")
vat_rate = st.number_input("VAT Rate (%)", min_value=0.0, value=7.5, format="%.2f")

if st.button("Calculate Profit"):
    buying_info, selling_info, profit, percentage_gain_loss = calculate_profit(shares, buying_price_per_share, selling_price_per_share, brokerage_rate, vat_rate)

    st.subheader("Buying Info")
    st.write(f"Total Consideration: {buying_info['Total Consideration']} Naira")
    st.write(f"Total Charges: {buying_info['Total Charges']} Naira")
    st.write(f"Actual Price per Share (after charges): {buying_info['Actual Price per Share']} Naira")

    st.subheader("Selling Info")
    st.write(f"Total Consideration: {selling_info['Total Consideration']} Naira")
    st.write(f"Total Charges: {selling_info['Total Charges']} Naira")
    st.write(f"Actual Price per Share (after charges): {selling_info['Actual Price per Share']} Naira")

    st.subheader("Profit and Gain/Loss")
    st.write(f"Profit: {profit} Naira")
    st.write(f"Percentage Gain/Loss: {percentage_gain_loss}%")
