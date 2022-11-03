"""
    RTLOC - Social Distancing

    utils.py

    (c) 2020-2022 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

"""

def print_distances(distances):
    addresses = list(distances.keys())

    if len(addresses) == 0:
        print("No distant tags found.")
    else:
        for address in addresses:
            print("TAG {} seen at {} cm".format(address, distances[address]))
    print("="*20)
