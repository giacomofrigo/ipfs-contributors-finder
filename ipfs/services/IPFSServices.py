import requests, ast, os, subprocess, time
from flask import current_app


class IPFSServices:

    @staticmethod
    def get_content_info (cid):
        '''
        This function returns info about the content with cid passed as argument
        It exploits the /api/v0/file/ls API provided by IPFS
        '''
        try:
            response = requests.post('http://localhost:5001/api/v0/file/ls?arg='+cid, timeout=10)
            if response.status_code < 400:
                return ast.literal_eval(response.text.replace('null', 'None'))
            else:
                current_app.logger.error ("Error executing the request")
                current_app.logger.error ("Status code {}\nText {}".format(response.status_code, response.text))
                return None
        except Exception as e:
            current_app.logger.error("Error executing the request")
            current_app.logger.error(e)
            return None

    @staticmethod
    def find_contributors():
        '''
        This function find the contributors of the peer
        It exploits the /api/v0/swarm/peers  and the /api/v0/bitswap/ledger APIs provided by IPFS
        '''
        contributors=[]
        try:
            response = requests.post('http://localhost:5001/api/v0/swarm/peers')
            if response.status_code < 400:
                swarm = ast.literal_eval(response.text.replace('null', 'None'))
            else:
                current_app.logger.error ("Error executing the request")
                current_app.logger.error ("Status code {}\nText {}".format(response.status_code, response.text))
        except:
            current_app.logger.error("Unable to exec the request")
            return None

        #go through the IPFS node swarm
        for peer in swarm['Peers']:
            #get the peer_id (then used to query the ledger) and the ip address
            peer_id = peer ['Peer']
            ip_address = peer['Addr'].split("/")[2]

            try:
                #query the ledger passing to it the peer_id
                response = requests.post('http://localhost:5001/api/v0/bitswap/ledger?arg='+peer_id)
                if response.status_code < 400:
                    peer_stat = ast.literal_eval(response.text)
                    #if there are some bytes exchenged between the two peers append the peer to the contributors array
                    if peer_stat["Exchanged"] > 0:
                        contributors.append({"peer_id": peer_id, "ip_address": ip_address, "received_bytes": peer_stat['Recv']})
                else:
                    current_app.logger.error ("Error executing the request")
                    current_app.logger.error ("Status code {}\nText {}".format(response.status_code, response.text))
                    return None
            except Exception as ex:
                current_app.logger.error("Unable to exec the request")
                current_app.logger.error(ex)
                return None
        return contributors

    @staticmethod
    def restart_daemon():
        '''
        This method is called every time a download starts.
        It is used in order to restart the daemon. This operation allow to reset daemon stats.
        '''
        current_app.logger.info("Terminating ipfs daemon.")
        #killing process
        subprocess.Popen(["killall", "-9", "ipfs"])
        current_app.logger.info("IPFS daemon terminated. Now restarting it.")
        #restaring daemon
        current_app.config["IPFS_DAEMON"] = subprocess.Popen(['ipfs', 'daemon'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(3)
        #clean the IPFS cache
        p = subprocess.run(['ipfs', 'repo', 'gc'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        if p.returncode != 0:
            current_app.logger.error("ipfs repo gc command has not be completed successfully")
        current_app.logger.info("IPFS daemon restarted.")
    
    @staticmethod
    def clean_cache(cid):
        '''
        This method is used once the download is completed.
        It removes the donwloaded file and clean the IPFS cache
        '''
        current_app.logger.info("Removing directory and cleaning ipfs repo")
        
        p = subprocess.run(['rm', '-r', cid], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        if p.returncode != 0:
            current_app.logger.error("unable to delete directory {}".format(cid))


        p = subprocess.run(['ipfs', 'repo', 'gc'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        if p.returncode != 0:
            current_app.logger.error("ipfs repo gc command has not be completed successfully")

    @staticmethod
    def get_bw():
        '''
        This API return the actual downlaod/upload rate. It exploits /api/v0/stats/bw IPFS api.
        '''
        try:
            response = requests.post('http://localhost:5001/api/v0/stats/bw')
            if response.status_code < 400:
                return ast.literal_eval(response.text.replace('null', 'None'))
            else:
                current_app.logger.error ("Error executing the request")
                current_app.logger.error ("Status code {}\nText {}".format(response.status_code, response.text))
                return None
        except Exception as e:
            current_app.logger.error("Unable to exec the request")
            current_app.logger.error(e)
            return None


