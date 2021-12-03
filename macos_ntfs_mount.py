#!/usr/bin/python3

import os, re


def umount_volume(device, mount_point='', force=False):
    force_flag = 'force ' if force else ''
    exit_code = os.system('diskutil {}umount '.format(force_flag) + device.replace(' ', '\\ '))
    if exit_code != 0:
        print('Error unmounting ' + device + ' at ' + mount_point)
    return exit_code


def mount_ntfs(device, mount_point, open=False):
    if not os.path.exists(mount_point):
        exit_code = os.system('sudo mkdir -p ' + mount_point.replace(' ', '\\ '))
        if exit_code != 0:
            print('Error creating directory ' + mount_point)
            return exit_code
    exit_code = os.system('sudo mount -t ntfs -o rw,auto,nobrowse ' + device + ' ' + mount_point.replace(' ', '\\ '))
    if exit_code != 0:
        print('Error mounting ' + device + ' at ' + mount_point)
        return exit_code
    # open the disk in Finder
    if open:
        os.system('open ' + mount_point.replace(' ', '\\ '))
    return exit_code

def ask_user(prompt, default=None):
    if default is None:
        prompt += ' [y/n] '
    else:
        prompt += ' [Y/n] '
    while True:
        answer = input(prompt).lower()
        if answer in ['y', 'yes', 'n', 'no']:
            break
        if default is not None:
            answer = default
            break
    return answer in ['y', 'yes']

target_volumes = []
mount = os.popen('mount')
for line in mount:
    if 'ntfs://' in line:
        search = re.search(r'ntfs://(disk\d+s\d+)/ on (/.+) \(+', line)
        disk = '/dev/' + search.group(1)
        mount_point = search.group(2)
        target_volumes.append((disk, mount_point))

if len(target_volumes) == 0:
    print('No NTFS volumes found.')
    if ask_user('Specify a disk to mount?', 'n'):
        disk = input('Disk: ')
        mount_point = input('Mount point: ')
        target_volumes.append((disk, mount_point))
    else:
        exit(1)

print('The following volumes will be unmounted and remounted as NTFS:')
for disk, mount_point in target_volumes:
    print(disk, mount_point)
input('Press Enter to continue...')
print('Checking for permissions, please enter your password if prompted...')
is_sudo = os.system('sudo -v')
if is_sudo != 0:
    print('Permission denied.')
    exit()

print('Unmounting volumes...')
for disk, mount_point in target_volumes:
    if umount_volume(disk, mount_point) != 0:
        if ask_user('Unmount failed, try to force unmount?', 'n'):
            umount_volume(disk, mount_point, True)

print('Mounting volumes...')
for disk, mount_point in target_volumes:
    if mount_ntfs(disk, mount_point, True) != 0:
        input('Press Enter to continue...')

print('Done!')
