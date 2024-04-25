import r2pipe
import time

pid = '853899'  # replace with your PID
r2 = r2pipe.open(f'pid://{pid}')

# Search for initial values between 1 and 100
addresses = []
for i in range(1, 101):
    hex_value = format(i, '04x')
    results = r2.cmdj(f'/xj {hex_value}')
    for result in results:
        addresses.append(result['offset'])

# Check if values decrement every second
for _ in range(100):  # Adjust this to the number of seconds you want to check
    time.sleep(1)
    r2.cmd('dc')  # Continue execution
    new_addresses = []
    for address in addresses:
        value = int(r2.cmd(f'pv @ {address}'), 16)
        if 1 <= value <= 100:
            new_addresses.append(address)
    addresses = new_addresses

# Print the addresses that consistently contained decrementing values
for address in addresses:
    print(hex(address))

