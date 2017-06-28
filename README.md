# Security_Groups_Scripts
Various scripts for the Rackspace Security Groups product

 
The Port Refresh script will refresh all ports in a particular securtity group to push new rules that get added
This will be irrelevent when the rules are autoupdated when the product reaches a general release
Example Usage : python portrefresh.py --securitygroup \<SG uuid\> --region \<Region\> --ddi \<DDI\> --user \<username\> --apikey \<apikey\> --network \<network uuid\>

PublicNet default ID : 00000000-0000-0000-0000-000000000000

ServiceNet default ID : 11111111-1111-1111-1111-111111111111
