import ctypes
import evdev
import pyudev
import threading
import extractData as exd
from logs import log

def get_connected_usb_devices():
    """Get connected USB devices."""
    devices = [evdev.InputDevice(device) for device in evdev.list_devices()]
    usb_devices = [device for device in devices if 'usb' in device.phys.lower()]
    return usb_devices

def wait_for_usb_events(connected=True):
    """Wait for USB ports updates."""
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')

    condition = threading.Condition()

    def device_event(observer, device):
        if (connected and device.action == 'add') or (not connected and device.action == 'remove'):
            with condition:
                condition.notify()

    observer = pyudev.MonitorObserver(monitor, device_event)
    observer.start()

    with condition:
        condition.wait()

    observer.stop()

def gracefully_terminate_threads(thread_list):
    """Gracefully terminate threads."""
    for thread in thread_list:
        thread.stop_requested = True
        thread.join()

def reset_threads(old_thread_list, new_devices_list):
    """Update thread list with new devices."""
    gracefully_terminate_threads(old_thread_list)
    
    new_thread_list = []
    
    for device in new_devices_list:
        thread = threading.Thread(target=exd.collectId, args=(device,))
        thread.start()
        new_thread_list.append(thread)
    
    return new_thread_list

# Usage
connected_usb_devices = get_connected_usb_devices()
threads = reset_threads(threads, connected_usb_devices)
wait_for_usb_events(connected=False)  # Wait for USB disconnections
