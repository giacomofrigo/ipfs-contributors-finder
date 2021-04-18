import os.path

import requests, ast, subprocess, time
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
    def get_content_info_bash(cid):
        '''
        This function returns info about the content with cid passed as argument
        '''
        try:
            response = subprocess.check_output(['ipfs', 'files', 'stat', '/ipfs/'+cid], stderr=subprocess.STDOUT, timeout=5)
            parsed_response = response.decode().strip().split("\n")
            dict_response = {'CID': parsed_response[0]}
            parsed_response = parsed_response[1:]
            for item in parsed_response:
                k,v = item.replace(' ', '').split(':')
                dict_response[k] = v

            return (dict_response)

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
                    if peer_stat["Recv"] > 0:
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
        time.sleep(4)
        #clean the IPFS cache
        #sometimes can happen that repo lock is not released
        try:
            if (os.path.isfile('/root/.ipfs/repo.lock')):
                p = subprocess.run(['rm', '-rf', '/root/.ipfs/repo.lock'])
        except:
            pass

        p = subprocess.run(['ipfs', 'repo', 'gc'])
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
        
        p = subprocess.run(['rm', '-rf', cid], stderr=subprocess.STDOUT)
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


