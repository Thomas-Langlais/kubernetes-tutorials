import psycopg2, argparse, time

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--timeout', default=120, type=int)
parser.add_argument('-s', '--sleep', default=5, type=int)
parser.add_argument('host', type=str)

args = parser.parse_args()

start_time = time.time()
flag = False

while time.time() - start_time < args.timeout:
    try:
        c = psycopg2.connect(host=args.host, user='postgres')
        # it connected
        print('Connected to database ' + args.host)
        c.close()
        flag = True
        break
    except Exception as e:
        print('Did not connect to database ' + args.host)
    time.sleep(args.sleep)

if flag:
    exit(0)
else:
    exit(1)