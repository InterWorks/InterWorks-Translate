def lambda_handler(event, context):
    # Info about connector
    return {   
        "description" : "InterWorks Translate",
        "creation_time" : "0",
        "state_path" : "https://github.com/holt-calder/InterWorks-DataDev-Hackathon-2021",
        "server_version" : "1.0.0",
        "name" : "InterWorks Translate", 
        "versions": {
        "v1": {
            "features": {
                "authentication": {
                    "required": True,
                    "methods": {
                        "basic-auth": {}
                        }
                }
            }
        }
    }
}