import urllib
def main():
    a = []    
    api_ctr = 0
    app_ctr = 0
    url_ctr = 0
    cals_ctr = 0
    flag = 0

    t = open('/Users/arpitpatil/python-tests/dashboard_bkp/demo-int.html','w')

    f = open('/Users/arpitpatil/python-tests/dashboard_bkp/demo-int.txt','r')

    t.write('<htm><center><img src="https://cwscms.osi.ca.gov/portals/0/Images/CWDS-Logo-Horizontal.png?ver=2016-03-30-141326-323"</img></center><hr></hr><body><center><table border=1></center>')
    #t.write('<tr><td><strong><center>Application</strong></td><td><strong><center>Status</strong></td><td><strong><center>Version</center></strong></td></tr>')
    
    for line in f:
        for word in line.split(','):
            a.append(word.strip('\n'))

    for hosts in a:
        if 'cwds.io' in hosts:
            env = hosts.split('.')[1].split('.')[0]
            flag += 1

    t.write('<h1><center><font face="palatino">ENVIRONMENT NAME: ' + env.upper() + '</center></h1><hr></hr>')

    t.write('<center><font face="timesnewroman">Environment URL: <a href="https://web.demo-int.cwds.io">https://web.demo-int.cwds.io</a></font></center>')

    t.write('<tr><td><strong><center>Application</strong></td><td><strong><center>Status</strong></td><td><strong><center>Version</center></strong></td></tr>')
    
    for item in range(len(a)):
        if 'cwds.io' in a[item]:
            host = a[item]
            t.write('<tr><td colspan="3"><center><font color="blue">' + host + '</font></center></td></tr>')
        else:
            if 'app' in a[item] and 'cwds.io' not in a[item] and 'cwds/' not in a[item]:
                #pos = a.index(item)
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

    if flag == 5:
        if app_ctr >= 1 or api_ctr >=1 or cals_ctr >= 1 or url_ctr >= 1:
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
