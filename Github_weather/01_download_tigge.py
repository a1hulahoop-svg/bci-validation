#!/usr/bin/env python3
"""
Download TIGGE Ensemble Forecasts
Author: Emma Dobbin
Date: December 2025

Downloads operational ensemble forecasts from TIGGE archive for UK storms.
Requires ECMWF API access (https://api.ecmwf.int/v1/key/)
"""

from ecmwfapi import ECMWFDataServer
import os
from datetime import datetime

def download_tigge_storms():
    """Download TIGGE data for 14 UK extratropical cyclones"""
    
    print("="*80)
    print("TIGGE DATA DOWNLOAD - UK STORMS 2021-2024")
    print("="*80)
    
    server = ECMWFDataServer()
    
    # Storm definitions
    storms = [
        # Original validation set
        {'name': 'Eunice', 'dates': '2022-02-17/to/2022-02-19'},
        {'name': 'Ciaran', 'dates': '2023-11-01/to/2023-11-03'},
        {'name': 'Babet', 'dates': '2023-10-18/to/2023-10-21'},
        {'name': 'Henk', 'dates': '2024-01-02/to/2024-01-04'},
        {'name': 'Isha', 'dates': '2024-01-21/to/2024-01-23'},
        {'name': 'Jocelyn', 'dates': '2024-01-23/to/2024-01-25'},
        # Extended validation set
        {'name': 'Arwen', 'dates': '2021-11-26/to/2021-11-28'},
        {'name': 'Malik', 'dates': '2022-01-28/to/2022-01-30'},
        {'name': 'Dudley', 'dates': '2022-02-16/to/2022-02-17'},
        {'name': 'Franklin', 'dates': '2022-02-20/to/2022-02-21'},
        {'name': 'Noa', 'dates': '2023-04-12/to/2023-04-14'},
        {'name': 'Debi', 'dates': '2023-11-13/to/2023-11-15'},
        {'name': 'Fergus', 'dates': '2023-12-10/to/2023-12-12'},
        {'name': 'Gerrit', 'dates': '2023-12-27/to/2023-12-29'},
    ]
    
    # Models: ECMWF and CMC (most reliable TIGGE contributors)
    origins = ['ecmf', 'cwao']  
    
    output_dir = 'tigge_data'
    os.makedirs(output_dir, exist_ok=True)
    
    total = len(storms) * len(origins)
    completed = 0
    
    for storm in storms:
        print(f"\n{storm['name']} ({storm['dates']})...")
        
        for origin in origins:
            completed += 1
            filepath = os.path.join(output_dir, f"{storm['name'].lower()}_{origin}.grib")
            
            print(f"  [{completed}/{total}] {origin.upper()}...", end='')
            
            try:
                server.retrieve({
                    'class': 'ti',              # TIGGE class
                    'dataset': 'tigge',
                    'date': storm['dates'],
                    'expver': 'prod',
                    'levtype': 'sfc',           # Surface level
                    'origin': origin,            # Model origin code
                    'param': '2t',              # 2m temperature
                    'step': '0/6/12/18/24',     # Forecast lead times
                    'time': '00:00:00/06:00:00/12:00:00/18:00:00',  # Init times
                    'type': 'pf',               # Perturbed forecasts (ensemble)
                    'number': '1/2/3/4/5/6/7/8/9/10',  # First 10 members
                    'grid': '0.25/0.25',        # 0.25 degree resolution
                    'area': '53/-2/52/-1',      # UK region (lat/lon bounds)
                    'target': filepath,
                    'expect': 'any'             # Accept any number of fields
                })
                
                if os.path.exists(filepath):
                    size_mb = os.path.getsize(filepath) / (1024 * 1024)
                    print(f" ✓ {size_mb:.1f} MB")
                else:
                    print(" ✗ Failed")
                    
            except Exception as e:
                print(f" ✗ Error: {e}")
    
    print("\n" + "="*80)
    print("DOWNLOAD COMPLETE")
    print("="*80)
    
    files = [f for f in os.listdir(output_dir) if f.endswith('.grib')]
    if files:
        total_size = sum(os.path.getsize(os.path.join(output_dir, f)) for f in files)
        print(f"\nFiles: {len(files)}/{total}")
        print(f"Total: {total_size/(1024*1024):.1f} MB")
        print(f"Location: {os.path.abspath(output_dir)}")
    else:
        print("\n✗ No files downloaded")

if __name__ == '__main__':
    download_tigge_storms()
