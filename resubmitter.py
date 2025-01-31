import os
def resubmitter():
    crab_dirs = os.listdir('../')
    abs_path = os.path.abspath('../')
    crab_dirs = [abs_path + '/' + x for x in crab_dirs if 'crab_' in x]
    count_success = 0
    for crab_dir in crab_dirs:
        log = os.popen('crab status -d ' + crab_dir).readlines()
        print('checking: ' + crab_dir)
        with open(crab_dir.split('/')[-1]+'.log','w') as f:
            for line in log:
                f.writelines(line)
        #check crab3 log, if 'failed' '%' 'Job Status' in one line, resubmit
        #if not, print('all jobs are done')
        failedJobNotExist = True
        for line in log:
            if 'Jobs status:' in line and 'finished' in line and '100.0%' in line:
                count_success = count_success + 1
                break
            
            elif 'failed' in line and '%' in line and 'Jobs status' in line:
                failedJobNotExist = False
                break
            
        if failedJobNotExist:
            print('all jobs are done')
            continue
        
        #resubmit crab3
        os.system('crab resubmit -d ' + crab_dir)
        print('resubmitted: ' + crab_dir)

    if count_success == len(crab_dirs):
        return True
    return False

if __name__ == '__main__':
    #call resubmitter every 2 hours
    import time
    while True:
        start_time = time.time()
        if resubmitter():
            break
        time_passed = time.time() - start_time
        
