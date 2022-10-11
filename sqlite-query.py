import sys
import os
import sqlite3
import argparse
import subprocess


if __name__ == '__main__':
    # read the command line arguments
    parser = argparse.ArgumentParser()
    # query.py [database] -f <script> -f <script> ...
    parser.add_argument('database', nargs='?', default=':memory:', help='database file to use, memory database will be used if not specified')
    # -f, --file: sql script file, could be multiple
    parser.add_argument('-f', '--file', action='append', help='sql script file, could be assigned multiple times and they will be executed in order')
    # -d, --width: width of each column in the output
    parser.add_argument('-d', '--width', metavar='N', type=int, default=13, help='width of each column in the output')
    # -l, --less: use less to display the output
    parser.add_argument('-l', '--less', action='store_true', help='use less to display the output')


    args = parser.parse_args()
    # print(args)

    db_name = args.database
    column_width = args.width
    use_less = args.less
    # create a database connection
    conn = sqlite3.connect(db_name)
    # create a cursor
    c = conn.cursor()

    # if file is not empty, execute sql scripts
    if args.file:
        for file in args.file:
            if not os.path.exists(file):
                print('Error: file {} does not exist'.format(file))
                sys.exit(1)
            with open(file, 'r') as f:
                sql = f.read()
                try:
                    c.executescript(sql)
                except sqlite3.Error as e:
                    print('Error: {}'.format(e))
                    sys.exit(1)
        conn.commit()

    # accept query from user
    # end with ;
    while True:
        query = ''
        user_input = None
        print('> ', end='')
        while True:
            try:
                user_input = input(' ')
            except KeyboardInterrupt:
                print('')
                query = ''
                break
            if user_input == '':
                continue
            query += user_input + '\n'
            # if query have ;, break
            inx = query.find(';')
            if inx != -1:
                query = query[:inx]
                break
        
        # check empty
        if query.strip() == '':
            continue
        
        # check exit
        if query.lower().strip() == 'exit':
            break

        # check import file
        command_name = 'load'
        if query.lower().startswith(command_name):
            # get file name
            file_name = query[len(command_name):].strip()
            if not os.path.exists(file_name):
                print('File not exist')
                continue
            # read file
            try:
                with open(file_name, 'r') as f:
                    # execute the file
                    c.executescript(f.read())
                # commit changes
                conn.commit()
            except Exception as e:
                print(e)
            finally:
                continue
        

        # make query
        try:
            c.execute(query)
            # get description
            desc = c.description
            # get data
            data = c.fetchall()
            # commit changes
            conn.commit()
            if len(data) != 0:
                # print in table format
                # print header
                print_buffer = ''
                table_header = '|'
                seprate_line = '-'
                for col in desc:
                    col_name = col[0]
                    table_header += ' {:<{column_width}} |'.format(col_name[:column_width], column_width=column_width)
                    seprate_line += '-' * (column_width + 2) + '+'
                seprate_line = seprate_line[:-1] + '-'
                print_buffer += '-' * len(table_header) + '\n'
                print_buffer += table_header + '\n'
                print_buffer += seprate_line + '\n'
                # print data
                for row in data:
                    table_row = '|'
                    for col in row:
                        table_row += ' {:<{column_width}} |'.format(str(col)[:column_width], column_width=column_width)
                    print_buffer += table_row + '\n'
                print_buffer += '-' * len(table_header) + '\n'
                print_buffer += '{} rows in selected'.format(len(data))
                # print if not use less, else use less
                if not use_less:
                    print(print_buffer)
                else:
                    # use pipe to pass data to less
                    p = subprocess.Popen(['less'], stdin=subprocess.PIPE)
                    p.communicate(print_buffer.encode('utf-8'))
            
            # print number of rows affected
            if c.rowcount != -1:
                print('{} rows affected'.format(c.rowcount))

        except Exception as e:
            print(e)
            # rollback changes
            conn.rollback()
