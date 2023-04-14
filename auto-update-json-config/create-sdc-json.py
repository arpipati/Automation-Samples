import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--service-principal', required=True, help='the value of the servicePrincipal field')
parser.add_argument('--filename', required=True, help='the sdc json file')
parser.add_argument("--accounts", nargs='+', type=str, help="list of account IDs to add")
parser.add_argument("--accounts-file", type=str, help="file containing list of account IDs to add")
parser.add_argument('--create-slr', action='store_true', help='service accounts allowlisting for CreateSLR')
parser.add_argument('--service-access', action='store_true', help='management accounts allowlisting for Enable/Disable AWS Service Access')
parser.add_argument('--register-da', action='store_true', help='management accounts allowlisting for enabling Delegated Adiminstrator for member accounts')
parser.add_argument('--ticket', required=True, help='provide the ticket url for this allowlisting request')

args = parser.parse_args()

with open(args.filename, 'r') as f:
    data = json.load(f)

matching_sp = next((sp for sp in data["allowlistedServicePrincipals"] if sp["servicePrincipal"] == args.service_principal), None)
'''
This is a generator expression that loops through each dictionary ("sp") in the "allowlistedServicePrincipals" list and filters them based on the condition that their "servicePrincipal" value is equal to the "service_principal_to_match" variable.

The generator expression is then passed to the "next()" function, which returns the first value that the generator expression produces. This value is the dictionary that matches the condition. If no match is found, the "next()" function returns None.

So, the "matching_sp" variable is assigned the value of the first dictionary in the "allowlistedServicePrincipals" list that matches the "servicePrincipal" condition, or None if no matches are found.
'''

if matching_sp:

    if args.create_slr:
        allowlist_api = matching_sp["accountIdsInServicePrincipal"]
        update_ticket = matching_sp["commentsAndRelatedTickets"]

        if args.accounts:
            allowlist_api.extend(args.accounts)
            if args.ticket not in update_ticket: update_ticket.append(args.ticket)

        if args.accounts_file:
            with open(args.accounts_file, 'r') as slr:
                for account in slr:
                    allowlist_api.append(account.strip())
                if args.ticket not in update_ticket: update_ticket.append(args.ticket)

        with open('output.json', "w") as slr:
            json.dump(data, slr, indent=4)

    if args.service_access:
        allowlist_api = matching_sp["allowedTargetManagementAccountIds"]
        update_ticket = matching_sp["commentsAndRelatedTickets"]

        if args.accounts:
            allowlist_api.extend(args.accounts)
            if args.ticket not in update_ticket: update_ticket.append(args.ticket)

        if args.accounts_file:
            with open(args.accounts_file, 'r') as sa:
                for account in sa:
                    allowlist_api.append(account.strip())
            if args.ticket not in update_ticket: update_ticket.append(args.ticket)

        with open('output.json', "w") as sa:
            json.dump(data, sa, indent=4)

    if args.register_da:
        
        allowlist_api = matching_sp["allowedTargetManagementAccountIdsForDelegatedAdmin"]
        update_ticket = matching_sp["commentsAndRelatedTickets"]
        
        if args.accounts:
            allowlist_api.extend(args.accounts)
            if args.ticket not in update_ticket: update_ticket.append(args.ticket)

        if args.accounts_file:
            with open(args.accounts_file, 'r') as da:
                for account in da:
                    allowlist_api.append(account.strip())
            if args.ticket not in update_ticket: update_ticket.append(args.ticket)
                
        with open('output.json', "w") as da:
            json.dump(data, da, indent=4)
else:
    print("The Service Principal is not in SDC!! Please reach out to ISO on-call for assistance...")