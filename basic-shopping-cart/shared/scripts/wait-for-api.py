import urllib3, argparse, time

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--timeout', default=120, type=int)
parser.add_argument('-s', '--sleep', default=5, type=int)
parser.add_argument('api', type=str)

args = parser.parse_args()

http = urllib3.PoolManager()


start_time = time.time()
flag = False

while time.time() - start_time < args.timeout:
    try:
        r = http.request('GET', args.api)
        if r.status == 200:
            flag = True
            print('api ' + args.api + ' is up')
            break
        print('api ' + args.api + ' is not up')
    except Exception as e:
        print('api ' + args.api + ' is not up')
    time.sleep(args.sleep)

if flag:
    exit(0)
else:
    exit(1)