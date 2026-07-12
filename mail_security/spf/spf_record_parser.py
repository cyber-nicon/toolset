# spf_record_parser.py
# Author: nicon
# Created 04/24 - 05/03/2026
# Last updated: 06/14/2026
# This peace of code, can be used to determine all
# ipv4 and ipv6 Adresses covered by a Domains SPF Entry

# to run this code simply give the wanted domain as argument
# output will be a list of ipv4 and ipv6 in csv

# the script is capped initially by 15 dns requests
# this is a requrement to a valid SPF record based on RFC
# if you want to cover all from your domain just increase 
# but make sure that you don't run into a loop

import dns.resolver
import sys
import ipaddress
import csv

first_domain = str(sys.argv[1])
print(first_domain)
spf_include = []
spf_include.append(first_domain)

all_ip4 = []
all_ip6 = []

max_dns_requests = 15
request_counter = 0

def is_ip(ip) -> bool:
    try:
        ip_adress = ipaddress.ip_adress(ip)
        return True
    except ValueError:
        return False

def is_ip_subnet(ip) -> bool:
    try:
        ip_subnet = ipaddress.ip_network(ip, strict=True)
        return True
    except ValueError:
        return False

for every_domain in spf_include:
    if(request_counter < max_dns_requests):
        print("Domain:", every_domain)
        continue_q = input("Do you want to continue with checking and adding the domain aboth? (y/n)")
        if(continue_q == "y"):
            print("start finding spf for:", every_domain)
            request_answer = dns.resolver.resolve(every_domain, "TXT")
            request_counter += 1

            initial_spf = ""

            for i in request_answer:
                initial_spf=i.to_text()
                if(initial_spf.startswith('"v=spf1')):
                    print("### Found SPF ####")
                    print(initial_spf)
                    print("##################")
                    break

            initial_spf = initial_spf.replace('" "', '')
            print(initial_spf)
            spf_entries = []
            # take initial spf record and split after each space
            word = ""
            spf_a = []
            spf_mx = []
            spf_ip4 = []
            spf_ip6 = []
            for i in initial_spf:
                if(i != " "):
                    word += i
                else:
                    spf_entries.append(word)
                    if(word.startswith("include:")):
                        spf_include.append(word[8:])
                    elif(word.startswith("a")):
                        spf_a.append(word)
                    elif(word.startswith("mx")):
                        spf_mx.append(word)
                    elif(word.startswith("ip4:")):
                        spf_ip4.append(word)
                        all_ip4.append(word[4:])
                    elif(word.startswith("ip6:")):
                        spf_ip6.append(word)
                        all_ip6.append(word[4:])
                    word = ""
                
            print(spf_entries)
            print("##################")
            print(spf_include)
            print(spf_a)
            print(spf_mx)
            print(spf_ip4)
            print(spf_ip6)


            print("starting resolving A and AAAA records now:")
            for i in spf_a:
                if (request_counter < max_dns_requests):
                    if (i == "a"):
                        print("try resolve A and AAAA:", every_domain)
                        try:
                            request_answer = dns.resolver.resolve(every_domain, "A")
                            for a in request_answer:
                                print (a.to_text())
                                all_ip4.append(a.to_text())
                        except dns.resolver.NoAnswer:
                            print("No A Record for Domain")
                        except dns.revolser.NXDOMAIN:
                            print("Domain not existing")
                        except dns.resolver.TIMEOUT:
                            print("DNS not answering")
                        except Exception as e:
                            print("A Unusal Error occured:", e)

                        request_counter += 1

                        try:
                            request_answer = dns.resolver.resolve(every_domain, "AAAA")
                            for a in request_answer:
                                print (a.to_text())
                                all_ip6.append(a.to_text())
                        except dns.resolver.NoAnswer:
                            print("No AAAA Record for Domain")
                        except dns.revolser.NXDOMAIN:
                            print("Domain not existing")
                        except dns.resolver.TIMEOUT:
                            print("DNS not answering")
                        except Exception as e:
                            print("A Unusal Error occured:", e)
                        
                        request_counter += 1
                    else:
                        print("try resolve A and AAAA:", i[2:])
                        try:
                            request_answer = dns.resolver.resolve(i[2:], "A")
                            for a in request_answer:
                                print (a.to_text())
                                all_ip4.append(a.to_text())
                        except dns.resolver.NoAnswer:
                            print("No A Record for Domain")
                        except dns.revolser.NXDOMAIN:
                            print("Domain not existing")
                        except dns.resolver.TIMEOUT:
                            print("DNS not answering")
                        except Exception as e:
                            print("A Unusal Error occured:", e)

                        request_counter += 1

                        try:
                            request_answer = dns.resolver.resolve(i[2:], "AAAA")
                            for a in request_answer:
                                print (a.to_text())
                                all_ip6.append(a.to_text())
                        except dns.resolver.NoAnswer:
                            print("No AAAA Record for Domain")
                        except dns.revolser.NXDOMAIN:
                            print("Domain not existing")
                        except dns.resolver.TIMEOUT:
                            print("DNS not answering")
                        except Exception as e:
                            print("A Unusal Error occured:", e)
                        
                        request_counter += 1

            print("start resolving MX records and ipv4 plus ipv6 out of it")
            mx_records = []
            for mx in spf_mx:
                if(request_counter < max_dns_requests):
                    if(mx == "mx"):
                        print("try resolve MX of:", every_domain)
                        try:
                            request_answer = dns.resolver.resolve(every_domain, "MX")
                            for a in request_answer:
                                print (a.to_text())
                                mx_records.append(a.to_text())
                        except dns.resolver.NoAnswer:
                            print("No MX Record for Domain")
                        except dns.revolser.NXDOMAIN:
                            print("Domain not existing")
                        except dns.resolver.TIMEOUT:
                            print("DNS not answering")
                        except Exception as e:
                            print("A Unusal Error occured:", e)

                        request_counter += 1
                    else:
                        print("try resolve MX of:", i[2:])
                        try:
                            request_answer = dns.resolver.resolve(i[2:], "MX")
                            for a in request_answer:
                                print (a.to_text())
                                mx_records.append(a.to_text())
                        except dns.resolver.NoAnswer:
                            print("No MX Record for Domain")
                        except dns.revolser.NXDOMAIN:
                            print("Domain not existing")
                        except dns.resolver.TIMEOUT:
                            print("DNS not answering")
                        except Exception as e:
                            print("A Unusal Error occured:", e)

                        request_counter += 1

                    for i in mx_records:
                        if(request_counter < max_dns_requests):
                            print("try resolve A and AAAA:", i)
                            try:
                                request_answer = dns.resolver.resolve(i, "A")
                                for a in request_answer:
                                    print (a.to_text())
                                    all_ip4.append(a.to_text())
                            except dns.resolver.NoAnswer:
                                print("No A Record for Domain")
                            except dns.revolser.NXDOMAIN:
                                print("Domain not existing")
                            except dns.resolver.TIMEOUT:
                                print("DNS not answering")
                            except Exception as e:
                                print("A Unusal Error occured:", e)

                            request_counter += 1

                            try:
                                request_answer = dns.resolver.resolve(i, "AAAA")
                                for a in request_answer:
                                    print (a.to_text())
                                    all_ip6.append(a.to_text())
                            except dns.resolver.NoAnswer:
                                print("No AAAA Record for Domain")
                            except dns.revolser.NXDOMAIN:
                                print("Domain not existing")
                            except dns.resolver.TIMEOUT:
                                print("DNS not answering")
                            except Exception as e:
                                print("A Unusal Error occured:", e)
                            
                        request_counter += 1
            print("current requests:", request_counter)
            print("#####################################")
            print("#####################################")
            print("#####################################")
            print("#####################################")
            print("#####################################")
        else:
            print("domain skipped")


print(all_ip4)
print(all_ip6)
print("needed requests:", request_counter)

store_all_hosts_to_csv = input("Do you want me to put all ipv4 Hosts into a csv? (y/n)")
if(store_all_hosts_to_csv == "y"):
    print ("_._._._._._._._._._._._._._._._._._._._._._._._._._._._._.")
    print ("_._._._._._._._._._._._._._._._._._._._._._._._._._._._._.")
    print("now moving through ipv4 array to list all hosts from subnetts")
    print ("_._._._._._._._._._._._._._._._._._._._._._._._._._._._._.")
    print ("_._._._._._._._._._._._._._._._._._._._._._._._._._._._._.")

    ipv4_hosts = []

    for ip4 in all_ip4:
        if(is_ip_subnet(ip4)):
            subnet = ipaddress.ip_network(ip4)
            for host in subnet:
                ipv4_hosts.append(str(host))
        elif(is_ip(ip4)):
            ipv4_hosts.append(ip4)
        else:
            print("this is not an ipv4 nor subnet:", ip4)
    
    #storing
    with open("ipv4_output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(ipv4_hosts)
    print("done!")
else:
    print("okay, nothing stored")

continue_with_ip6 = input("Do you want to continue with ipv6 host-list-creation and storage? WARNING: depending on Network sizes this can be a lot. Continue (y/n)")
if(continue_with_ip6 == "y"):
    print ("_._._._._._._._._._._._._._._._._._._._._._._._._._._._._.")
    print ("_._._._._._._._._._._._._._._._._._._._._._._._._._._._._.")
    print("now moving through ipv6 array to list all hosts from subnetts")
    print ("_._._._._._._._._._._._._._._._._._._._._._._._._._._._._.")
    print ("_._._._._._._._._._._._._._._._._._._._._._._._._._._._._.")

    ipv6_hosts = []
    for ip6 in all_ip6:
        if(is_ip_subnet(ip6)):
            subnet = ipaddress.ip_network(ip6)
            for host in subnet:
                ipv6_hosts.append(str(host))
        elif(is_ip(ip6)):
            ipv6_hosts.append(ip6)
        else:
            print("this is not an ipv6 nor subnet:", ip6)
    #storing
    with open("ipv6_output.csv", "w", newline="") as fsix:
        writer = csv.writer(fsix)
        writer.writerow(ipv6_hosts)
    print("done!")
else:
    print("Fine, thank you for using")
    exit()
