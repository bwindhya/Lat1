import requests
import hashlib
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error : {res.status_code}, Cek APi dan coba lagi')
    return res

def read_res(response):
    print(response.text)

def get_pass_leak_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    # print(hashlib.sha1(password.encode('utf-8')).hexdigest().upper())
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1password[:5], sha1password[5:]
    # print(first5, tail)
    response = request_api_data(first5)
    # print(response)
    return get_pass_leak_count(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} ditemukan {count} kali, silahkan diganti.')
        else:
            print(f'{password} tidak ditemukan, mantapp.')
    return 'Selesai'

# pwned_api_check('123')
# request_api_data('Password123')

if __name__ == '__main__':
    with open('./CekPass.txt', mode='r') as myFile:
        text = myFile.readlines()
        main(text)
    # sys.exit(main(sys.argv[1:]))