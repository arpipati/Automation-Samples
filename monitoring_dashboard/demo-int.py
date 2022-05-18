import urllib
def main():
    a = []  ## --- List to capture the parsed output from the comma separated text files

    ## --- Counter variables to track every occurance of "exited" container status
    api_ctr = 0
    app_ctr = 0
    url_ctr = 0
    cals_ctr = 0
    flag = 0

    ## --- File object to open HTML files in "write" mode
    t = open('/Users/arpitpatil/python-tests/dashboard_bkp/demo-int.html','w')

    ## --- File object to open comma separated environment text files in "write" mode
    f = open('/Users/arpitpatil/python-tests/dashboard_bkp/demo-int.txt','r')

    ## --- Add the project logo at the begining of the HTML file
    t.write('<htm><center><img src="https://cwscms.osi.ca.gov/portals/0/Images/CWDS-Logo-Horizontal.png?ver=2016-03-30-141326-323"</img></center><hr></hr><body><center><table border=1></center>')
    #t.write('<tr><td><strong><center>Application</strong></td><td><strong><center>Status</strong></td><td><strong><center>Version</center></strong></td></tr>')
    
    ## --- Parse the comma separated text file and append the list "a" with the file contents
    for line in f:
        for word in line.split(','):
            a.append(word.strip('\n'))

    ## --- Identify the EC2 hostname
    for hosts in a:
        if 'cwds.io' in hosts:
            env = hosts.split('.')[1].split('.')[0]
            flag += 1

    ## --- Add Environment metadata to the HTML file
    t.write('<h1><center><font face="palatino">ENVIRONMENT NAME: ' + env.upper() + '</center></h1><hr></hr>')

    t.write('<center><font face="timesnewroman">Environment URL: <a href="https://web.demo-int.cwds.io">https://web.demo-int.cwds.io</a></font></center>')

    t.write('<tr><td><strong><center>Application</strong></td><td><strong><center>Status</strong></td><td><strong><center>Version</center></strong></td></tr>')
    
    ## --- Main logic to check for "exited" containers and add appropriate HTML code blocks to the HTML file
    for item in range(len(a)):
        ## --- If construct to identify EC2 hostname and add Table Row in the HTML file.
        if 'cwds.io' in a[item]:
            host = a[item]
            t.write('<tr><td colspan="3"><center><font color="blue">' + host + '</font></center></td></tr>')
        else:
            if 'app' in a[item] and 'cwds.io' not in a[item] and 'cwds/' not in a[item]:
                ## --- "pos" is short for position of the item in the list.
                pos = item 
                t.write('<tr><td>' + a[item] + '</td>')
                status = a[pos+1]
                version = a[pos+2]
                if 'Exited' in status:
                    t.write('<td><font color="red">' + status + '</font></td>')
                    app_ctr += 1
                else:
                    t.write('<td><font color="green">' + status + '</font></td>')
                t.write('<td>' + version + '</td></tr>')
            
            if 'api' in a[item] and 'cwds.io' not in a[item] and 'cwds/' not in a[item]:
                #pos = a.index(item)
                pos = item
                t.write('<tr><td>' + a[item] + '</td>')
                status = a[pos+1]
                version = a[pos+2]
                if 'Exited' in status:
                    t.write('<td><font color="red"><blink>' + status + '</blink></font></td>')
                    api_ctr += 1
                else:
                    t.write('<td><font color="green">' + status + '</font></td>')
                t.write('<td>' + version + '</td></tr>')

            if 'cals' in a[item] and 'cwds.io' not in a[item] and 'cwds/' not in a[item] and 'api' not in a[item]:
                #pos = a.index(item)
                pos = item
                t.write('<tr><td>' + a[item] + '</td>')
                status = a[pos+1]
                version = a[pos+2]
                if 'Exited' in status:
                    t.write('<td><font color="red">' + status + '</font></td>')
                    cals_ctr += 1
                else:
                    t.write('<td><font color="green">' + status + '</font></td>')
                t.write('<td>' + version + '</td></tr>')
            
            if 'logspout' in a[item] and 'logspout-logstash' not in a[item]:
                #pos = a.index(item)
                pos = item
                t.write('<tr><td>' + a[item] + '</td>')
                status = a[pos+1]
                version = a[pos+2]
                if 'Exited' in status:
                    t.write('<td><font color="red">' + status + '</font></td>')
                    cals_ctr += 1
                else:
                    t.write('<td><font color="green">' + status + '</font></td>')
                t.write('<td>' + version + '</td></tr>')
        
    t.write('</table></body></htm>')

    ## --- Flag is set to 5 because we have 5 EC2 instances running the core application components. 
    if flag == 5:
        ## --- If any of the counters are incremented, we have a Docker Container in "Exited" status. 
        if app_ctr >= 1 or api_ctr >=1 or cals_ctr >= 1 or url_ctr >= 1:
            ## --- "m" is the File object for the master HTML file, the landing page for the dashboard.
            m = open('/Users/arpitpatil/python-tests/dashboard_bkp/master-dash.html','a')
            m.write('<div class="floating-box"><center>Preint Environment</center><h4><center><font color="red">1 or more issues reported<center></font></center></h4><center><a href="https://s3-us-west-1.amazonaws.com/env-status.cwds.io/demo-int.html">Click here to check environment stats</a></div>')
            m.close()
        else:
            m = open('/Users/arpitpatil/python-tests/dashboard_bkpmaster-dash.html','a')
            m.write('<div class="floating-box"><center>Preint Environment</center><h4><center><font color="green">No Issues Reported</font></center></h4><center><a href="https://s3-us-west-1.amazonaws.com/env-status.cwds.io/demo-int.html">Click here to check environment stats</a></div>')
            m.close()

    t.close()
    f.close()
    
if __name__ == '__main__':
    main()
