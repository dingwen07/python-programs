#!/usr/bin/python3

import os, re

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
    exit(1)
else:
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
        exit_code = os.system('sudo umount ' + mount_point.replace(' ', '\\ '))
        if exit_code != 0:
            print('Error unmounting ' + disk + ' at ' + mount_point)
            input('Press Enter to continue...')

    print('Mounting volumes...')
    for disk, mount_point in target_volumes:
        exit_code = os.system('sudo mkdir -p ' + mount_point.replace(' ', '\\ '))
        if exit_code != 0:
            print('Error creating directory ' + mount_point)
            input('Press Enter to continue...')
        exit_code = os.system('sudo mount -t ntfs -o rw,auto,nobrowse ' + disk + ' ' + mount_point.replace(' ', '\\ '))
        if exit_code != 0:
            print('Error mounting ' + disk + ' at ' + mount_point)
            input('Press Enter to continue...')
        # open the disk in Finder
        os.system('open ' + mount_point.replace(' ', '\\ '))

print('Done!')
