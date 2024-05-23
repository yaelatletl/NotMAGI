import win32api
import win32security

def get_object_properties(object_type, object_name):
  # Convert the object name to a SID.
  sid = win32security.LookupAccountName(None, object_name)[0]

  # Get the object's properties.
  if object_type == 'user':
    properties = win32security.GetSecurityInfo(sid, win32security.SE_USER_OBJECT, win32security.OWNER_SECURITY_INFORMATION | win32security.GROUP_SECURITY_INFORMATION | win32security.DACL_SECURITY_INFORMATION)
  elif object_type == 'group':
    properties = win32security.GetSecurityInfo(sid, win32security.SE_GROUP_MANDATORY, win32security.OWNER_SECURITY_INFORMATION | win32security.GROUP_SECURITY_INFORMATION | win32security.DACL_SECURITY_INFORMATION)
  elif object_type == 'computer':
    properties = win32security.GetSecurityInfo(sid, win32security.SE_COMPUTER_OBJECT, win32security.OWNER_SECURITY_INFORMATION | win32security.GROUP_SECURITY_INFORMATION | win32security.DACL_SECURITY_INFORMATION)

  # Print the object's properties.
  print('{}: {}'.format(object_type, object_name))
  print('SID: {}'.format(sid))
  print('Owner: {}'.format(properties['owner']))
  print('Group: {}'.format(properties['group']))
  print('DACL: {}'.format(properties['dacl']))

# Get the object type and name from the user.
object_type = input('Enter the object type (user, group, or computer): ')
object_name = input('Enter the object name: ')

# Get the object's properties.
get_object_properties(object_type, object_name)

import platform
import psutil
import wmi

def get_system_info():
  """Gathers information about the operative system."""

  # Get general information about the system
  system_info = platform.uname()
  # Get information about the CPU
  cpu_info = psutil.cpu_times()
  # Get information about the memory
  memory_info = psutil.virtual_memory()
  # Get information about the disks
  disk_info = psutil.disk_usage('/')
  # Get information about the network interfaces
  network_info = psutil.net_if_stats()
  # Get information about the processes
  process_info = [p.info for p in psutil.process_iter()]
  # Get information about the users
  user_info = [u.name for u in wmi.WMI().Win32_UserAccount()]

  # Return a dictionary with all the information
  return {
    "system_info": system_info,
    "cpu_info": cpu_info,
    "memory_info": memory_info,
    "disk_info": disk_info,
    "network_info": network_info,
    "process_info": process_info,
    "user_info": user_info,
  }