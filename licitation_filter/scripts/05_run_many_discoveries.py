import time
from licitation_filter.scripts.run_licitation_discovery import run_licitation_discovery

dates = ["05102025"]

for date in dates:
    run_licitation_discovery(date)
    time.sleep(5)
    print("\n")