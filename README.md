# IFF OPC-UA data service deployments with Akri OPC-UA Discovery-Handler

**Folder - akri:**

OPC-UA (Open Platform Communications Unified Architecture) is a communication protocol for industrial automation. Akri has implemented a Discovery Handler for discovering OPC UA Servers that live at specified endpoints or are registered with specified Local Discovery Servers.

The akri folder contains fleet configuration to deploy Akri components and OPC-UA discovery handler. The fleet config file internally uses Akri Helm charts for the deployment. Akri is responsible for deploying IFF OPC-UA data broker service stack upon discovery of a specified server endpoint (More on this below).

**Folder - iff:**

IFF broker service Helm chart is located in this folder. Using values.yaml file, the IFF broker service Helm template can be configured.

IFF OPCUA data broker service/pod contains two containers, one is the fusionopcuadataservice which is a Python client for fetching data from OPC UA servers and another is the PDT agent (Process Data Twin) for transferring the fetched data to the PDT backend.

The IFF broker containers are deployed under a single broker pod. The broker pod's lifecycle management is handled by Akri. The broker pod also needs extra resource configurations such as secrets, configmaps, etc that are also part of the deployment file.

**Discovery Handler (DH) Configuration:**

The Akri's DH must be given a set of URLs and the OPC-UA servers's applicationName value to discover the appropriate machine. These are passed to Akri with IFF broker's Helm template as part of Akri 'Configuration' custom resource.

IFF uses a single node for each machine, and each machine will have its own OPC configuration data tree. These configurations are deployed as configmaps as described above. Because of the single node, the applicationName config for Akri will contain only one server name.


**Usecase:**

IFF prepares the single node smartbox as a platform by running the above mentioned Akri components and deploying the configurations (secrets, configmaps) for IFF broker (Note: IFF Broker pod itself will not be pre-deployed as it will be done automatically at the user end by Akri DH) and ships them to users for connecting them to a predefined machine. The application name of OPC-UA server inside the user's machine will be pre-configured for discovery in the Akri DH. Also, the IP address list of the user's IP subnet with the appropriate port numbers combination must be preconfigured in DH before sending the smartbox to users. Once the pre-configuration of the smartbox with akri and iff configuration related deployments is done, and the smartbox is IF ready, it is shipped to the user.

User connects the smartbox to the LAN to which his machine is also connected and switches it on (Akri configuration already knows this IP address range and the machine's OPC server name). The Akri DH scans the network using the IP address list and chooses the right OPC server based on the pre-configured OPC server application name. Once the detection is successful, Akri automatically deploys the IFF broker pod and handles the lifecycle of the pod based on machine availability. Akri not only discovers the machine but also fetches its connection URL and automatically passes it to the IFF broker pod internally as an environment varibales for connection.


**Troubleshooting/Known Issues**

1. All IP addresses in the subnet must be listed with possible ports, which is a huge list of combinations. The Local Discovery Server (LDS) proposal from the OPC foundation might help to aggregate all the OPC-UA servers in one place. (Reaserch and Testing - In Progress) [https://profiles.opcfoundation.org/profile/1634]
2. Some machines have their OPC UA server port at 4840 (standard), and some at 62548 (custom).
3. The single node Kubernetes is based on RKE2. When the smartbox is shipped to another IP subnet at the user end, the IP address used in Kubernetes services previously in IFF might differ at the user end. This causes Kubernetes breakdown (Research and Testing for the solution - In Progress)
4. The OPC server's application name value is not unique across locations and clients. It might be a localized value. (Akri must be restructured to use applicationUri instead - SUSE has taken note)
5. RKE2 CIS profile prerequisites are not saved after reboot in elemental OS. When the smartbox is rebooted at the user end the values are not persistent. (Solution: Don't use RKE2 CIS profile)

