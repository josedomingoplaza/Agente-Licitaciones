import time
from licitation_filter.scripts.licitation_discovery import run_licitation_discovery

dates = ["10112025"]

for date in dates:
    run_licitation_discovery(date)
    time.sleep(5)
    print("\n")