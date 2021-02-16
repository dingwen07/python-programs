from u2flib_host import u2f, exc

# Enumerate available devices
devices = u2f.list_devices()

print(devices)
'''
for device in devices:
    # The with block ensures that the device is opened and closed.
    with device as dev:
        # Register the device with some service
        registrationResponse = u2f.register(device, registrationRequest, facet)
'''
