import pandas as pd
import random
from datetime import datetime, timedelta
import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import pandas as pd
# Constants for the promotions
brands = ["RED BULL", "COCA COLA", "PEPSI", "FANTA", "SPRITE", "MONSTER", "GATORADE", "MOUNTAIN DEW"]
locations = ["CENTER_OF_STORE", "TOP_SHELF", "STORE_ENTRANCE", "EXIT_FRIDGE"]
campaign_types = ["STORE_DISPLAY", "FRIDGE_DISPLAY", "SHELF_DISPLAY"]
retailers = ["TARGET", "COSTCO", "ALBERTSONS", "KROGER", "WALMART"]
tactic_types = {"STORE_DISPLAY": 1, "FRIDGE_DISPLAY": 2, "SHELF_DISPLAY": 3}
ALB_ADR = ["4541 Campus Dr, Irvine, CA 92612", "14201 Jeffrey Rd, Irvine, CA 92620", "24251 Muirlands Blvd, Lake Forest, CA 92630", "24251 Muirlands Blvd, Lake Forest, CA 92630", "19640 Beach Blvd, Huntington Beach, CA 92648"]
TAR_ADR =["200 Westminster Mall, Westminster, CA 92683", "16400 Beach Blvd, Westminster, CA 92683", "13831 Brookhurst St, Garden Grove, CA 92843", "9882 Adams Ave, Huntington Beach, CA 92646", "9882 Adams Ave, Huntington Beach, CA 92646", "9882 Adams Ave, Huntington Beach, CA 92646", "9882 Adams Ave, Huntington Beach, CA 92646"]
CSC_ADR = ["2200 E Willow St, Signal Hill, CA 90755", "500 Lakewood Center Mall, Lakewood, CA 90712", "5401 Katella Ave, Cypress, CA 90720", "7562 Center Ave, Huntington Beach, CA 92647", "13225 Beach Blvd, Westminster, CA 92683", "13225 Beach Blvd, Westminster, CA 92683", "17900 Newhope St, Fountain Valley, CA 92708", "900 S Harbor Blvd, Fullerton, CA 92832"]
KRG_ADR = ["4033 Ball Rd, Cypress, CA 90630", "5241 Warner Ave, Huntington Beach, CA 92649", "5241 Warner Ave, Huntington Beach, CA 92649", "915 S Brookhurst St, Anaheim, CA 92804", "12051 Euclid St, Garden Grove, CA 92840", "380 E 17th St, Costa Mesa, CA 92627", "380 E 17th St, Costa Mesa, CA 92627", "2555 Eastbluff Dr, Newport Beach, CA 92660"]
WMT_ADR = ["8450 La Palma Ave, Buena Park, CA 90620", "12840 Beach Blvd, Stanton, CA 90680", "12840 Beach Blvd, Stanton, CA 90680", "21132 Beach Blvd, Huntington Beach, CA 92648", "3600 W McFadden Ave, Santa Ana, CA 92704", "1120 S Anaheim Blvd, Anaheim, CA 92805", "2300 N Tustin St, Orange, CA 92865"]
# Generate random dates within the specified range
def generate_random_dates():
    start_date = datetime.strptime("01-01-2024", "%d-%m-%Y")
    end_date = datetime.strptime("31-12-2024", "%d-%m-%Y")
    random_start = start_date + timedelta(days=random.randint(0, (end_date - start_date).days - 30))
    random_end = random_start + timedelta(days=random.randint(1, 30))
    return random_start.strftime("%d-%m-%Y"), random_end.strftime("%d-%m-%Y")

def get_address_from_store(store):
    if store == "ALBERTSONS":
        return random.choice(ALB_ADR)
    elif store == "TARGET":
        return random.choice(TAR_ADR)
    elif store == "COSTCO":
        return random.choice(CSC_ADR)
    elif store == "KROGER":
        return random.choice(KRG_ADR)
    elif store == "WALMART":
        return random.choice(WMT_ADR)
    else:
        return "UNKNOWN"
    
def pdf(df):

    d = {'x{}'.format(i): range(30) for i in range(10)}

    table = pd.DataFrame(d)

    fig = plt.figure()

    ax=fig.add_subplot(111)

    cell_text = []
    for row in range(len(table)):
        cell_text.append(table.iloc[row])

    ax.table(cellText=cell_text, colLabels=table.columns, loc='center')
    ax.axis('off')

    pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")
    pdf.savefig(fig)
    pdf.close()

# Generate the promotions
promotions = []
for i in range(1, 201):
    brand = random.choice(brands)
    location = random.choice(locations)
    campaign_type = random.choice(campaign_types)
    promotion_name = f"{brand} BRAND {location}"
    product = f"{brand} {'CANS' if random.choice([True, False]) else 'BOTTLES'}"
    retailer = random.choice(retailers)
    store = get_address_from_store(retailer)
    tactic_type = tactic_types[campaign_type]
    start_date, end_date = generate_random_dates()
    promotions.append([i, promotion_name, product, campaign_type, retailer, store, tactic_type, start_date, end_date])

# Convert to DataFrame
df = pd.DataFrame(promotions, columns=["id", "Promotion Name", "Product", "Campaign Type", "Retailer", "Store", "Tactic Type", "Start Date", "End Date"])

# Save to CSV
df.to_csv('promotions_data_v2.csv', index=False)

df.to_html('promotions_data_v2.html', index=False)

# Save to PDF
# pdf(df)
