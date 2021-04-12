import subprocess,time
process = subprocess.Popen(['ipfs', 'daemon'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
time.sleep(4)
print(process.poll())
time.sleep(4)
process.terminate()
time.sleep(4)
print(process.poll())


