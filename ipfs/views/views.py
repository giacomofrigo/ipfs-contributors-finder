from flask import Blueprint, render_template, jsonify, current_app
from ipfs.services import IPFSServices

import subprocess, requests

views = Blueprint("views", __name__)

download_process = None
downloading_cid = None
current_contributors_addresses = {}

def localize_ip(ip_address):
    '''
    This is a utility function that localize ip address using ipapi API
    '''
    current_app.logger.debug("Localizing ip address {}".format(ip_address))
    try:
        response = requests.get("https://ipapi.co/{}/json".format(ip_address), timeout=1).json()
    except:
        current_app.logger.error("Unable to localize ip address {}".format(ip_address))
        return None
    if 'error' in response:
        current_app.logger.error("Unable to localize ip address {}".format(ip_address))
        return None
    current_app.logger.debug("City {}, Region {}, Country Name {}, Country Code {}".format(response["city"], response["region"], response["country_name"], response["country_code"]))
    return response["city"], response["region"], response["country_name"], response["country_code"]

@views.route("/")
def index():
    return render_template("index.html")

@views.route("/api/download/<cid>", methods=['GET'])
def start_download(cid):
    '''
    This API allows to start a new Download o the CID speficified in the GET request
    '''
    global download_process, downloading_cid
    # if download process is not none and it has not completed yet
    current_app.logger.info("Download requested.")
    if download_process is not None and download_process.poll() is None:
        current_app.logger.error("Can not start a new download, a download is already in progress. Download_process: {}, .poll(): {}".format(download_process, download_process.poll()))
        return "A download is already accouring.. please wait", 500

    cid = cid.strip()
    downloading_cid = cid

    #restart the daemon in order to reset stats
    current_app.logger.info("Restarting the daemon.")
    IPFSServices.restart_daemon()

    #check if the cid exists
    info = IPFSServices.get_content_info(cid)
    if info is None:
        current_app.logger.error("Object ID not found.")
        return "Unable to contact IPFS daemon, please try again later.", 404
    
    if info['Objects'][cid]['Type'] == "File":
        obj_type = "File"
        obj_dimension = info['Objects'][cid]['Size']
    elif info['Objects'][cid]['Type'] == "Directory":
        obj_type = "Directory"
        obj_dimension = info['Objects'][cid]['Links'][0]['Size']
    else:
        obj_type = None
        obj_dimension = None

    current_app.logger.info("Requested obj {}, TYPE: {}, DIMENSION: {}".format(downloading_cid, obj_type, obj_dimension))

    #start the download thread that will execute the get_content method
    
    download_process = subprocess.Popen(['/usr/local/bin/ipfs', 'get', cid], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return jsonify({"message":"Download started", "obj_type":obj_type, "obj_dimension":obj_dimension}), 200

@views.route("/api/download/status", methods=['GET'])
def download_status():
    '''
    API to get download thread status
    '''
    global downloading_cid, download_process, current_contributors_addresses

    if download_process is not None and download_process.poll() is None:
        return "Process alive", 200
    else:
        if downloading_cid != None:
            #cleaning downloaded file and ipfs repo gc
            IPFSServices.clean_cache(downloading_cid)

        current_app.logger.info("cleaning ip addresses cache")
        current_contributors_addresses = {}
        downloading_cid = None
        return "Process dead", 200
        
@views.route("/api/stats/contributors", methods=['GET'])
def get_contributors():
    '''
    This API will return the current contributors
    It returns a json with the following format:
    [{"peer_id": peer_id, "ip_address": ip_address, "received_blocks": # received blocks,
      "city": city, "region": region, "country_name": countr_name, "country_code": country_code}]

    There could be the possibility that the IP localization fails. In that case the above cited result dictionary
    will not contains keys city, region, country_name, country_code
    '''

    result = []
    #find contributors by query the IPFS daemon
    contributors = IPFSServices.find_contributors()
    #contributors is in the following format
    #[{"peer_id": peer_id, "ip_address": ip_address, "received_blocks": # received blocks}]
    if contributors is None:
        return "An error occured getting contributors", 500

    #for each peer localize its ip address
    for contributor in contributors:
        #if the ip address is already in address cache, take localization from there
        if contributor['ip_address'] in current_contributors_addresses:
            current_app.logger.debug("Contributor {} is already in localize cache".format(contributor['ip_address']))
            result.append({**contributor, **current_contributors_addresses[contributor['ip_address']]})
            continue
        #otherrwise localize ip address
        else:
            current_app.logger.debug("Contributor {} is not in localize cache.. localizing it".format(contributor['ip_address']))
            try:
                city, region, country_name, country_code = localize_ip(contributor['ip_address'])
            except:
                #if the localizing API failed, just do not append localizing infos
                result.append(contributor)
                continue

            #append the new localized peer to the cache
            current_contributors_addresses[contributor['ip_address']] = {'city': city, 'region': region, 'country_name':country_name, 'country_code':country_code}
            #and append it also for the result
            result.append({**contributor, **current_contributors_addresses[contributor['ip_address']]})

    return jsonify(result)

@views.route("/api/stop/<cid>")
def stop_download(cid):
    '''
    This API stops the download by simpling killing the thread
    '''
    global downloading_cid

    pass

