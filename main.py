import os
import json


def validate_path(check_path):
    '''
    Create file path, if appropriate
    :param check_path: path to be checked
    :return: none
    '''
    if not os.path.exists(check_path):
        os.makedirs(check_path)

def next_filename(name, ext):
    '''
    Return next appropriate file name
    :param name: structured name scheme
    :param ext: file extension
    :return: non-existent filename with extension
    '''
    n = 1
    if not os.path.exists(f'{name}.{ext}'):
        return f'{name}.{ext}'
    while True:
        if not os.path.exists(f'{name}-{n}.{ext}'):
            return f'{name}-{n}.{ext}'
        n += 1


def update_master_json(new_dict):
    '''
    Update or create master.json file
    :param local: relative local path
    :param href: absolute href location
    :return: No python, file 'master.json' updated
    '''
    if not os.path.exists('master.json'):
        f = open('master.json', 'w')
        f.write('{\n}\n')
        f.close()
    f = open('master.json', 'r')
    try:
        existing_dict = json.load(f)
        f.close()
    except:  # Despite PEP8 E722, this is appropriate as it will always start fresh if ANY errors
        f.close()
        existing_dict = {}
        os.rename('master.json', next_filename('invalid-master', 'json'))
    f = open('master.json', 'w')
    json.dump({**existing_dict, **new_dict}, f)
    f.close()


def create_files(data):
    '''
    Create appropriate HTML redirect files
    :param data: dictionary json of redirects.json
    :return: No python, create files $slug/index.html
    '''
    master_json_dict = {}
    for permalink in data:
        validate_path('dist/' + permalink.lower())
        dist = open('dist/' + permalink.lower() + '/index.html', 'w+')
        # This is intentionally a single line /index.html to reduce disk space consumption.
        # However, an even smaller size could be achieved if violating W3C Validation.
        # W3C is required per directive, so 521 bytes is the smallest while maintaining required browser support.
        dist.write(f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="refresh" '
                   f'content="0; url={data[permalink]}"><noscript><meta http-equiv="refresh" content="0; url={data[permalink]}">'
                   f'</noscript><script>window.location.href="{data[permalink]}";</script><meta http-equiv="X-UA-Compatible" '
                   f'content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0" >'
                   f'<title>Redirecting...</title></head><body><h1>Hello, Stranger</h1><p>The address you are trying is access'
                   f'is actually elsewhere.</p><p>Please visit <a href={data[permalink]}>{data[permalink]}</a>'
                   f'instead.</p></body></html>')
        dist.close()
        master_json_dict[permalink.lower()] = data[permalink]
    print('HTML distribution completed; proceeding to update master.json')
    update_master_json(master_json_dict)
    print('Successfully updated master.json')


def main():
    f = open('redirects.json', 'r')
    try:
        data = json.load(f)
        assert isinstance(data, dict)
    except:  # Despite PEP8 E722, this is appropriate as it always warns the user of invalid inputs and exits the program
        f.close()
        print('The file "redirects.json" must be valid; please see README.md for an example.')
        exit()
    create_files(data)
    f.close()


if __name__ == '__main__':
    main()

