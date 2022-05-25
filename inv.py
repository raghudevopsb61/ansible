import boto3
region = 'us-east-1'
route53 = boto3.client('route53')
app = ["mongodb", "redis", "rabbitmq", "mysql", "catalogue", "user", "cart", "shipping", "payment", "dispatch",
       "frontend"]
env = "dev"
domain = "roboshop.internal."

new_list = []  # fqdn

for item in app:
    new_list.append(f'{item}-{env}.{domain}')

res_dict = {}

response = route53.list_hosted_zones()
for item in response['HostedZones']:
    # print(item)
    if item['Name'] == domain:
        res_dict[item['Name']] = item['Id']

current_dns = {}
sub = f'-{env}.{domain}'
dns_records = route53.list_resource_record_sets(HostedZoneId=res_dict[domain])
for item in dns_records['ResourceRecordSets']:
    if item['Type'] == 'A':
        if item['Name'] in new_list:
            current_dns[item['Name'].replace(sub, "").upper()] = item['Name']

print(current_dns)
with open('roboshop.inv', 'w') as outfile:
    for key, value in current_dns.items():
        outfile.write(f'[{key}]\n')
        outfile.write(f'{value}\n')
