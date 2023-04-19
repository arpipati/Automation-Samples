require 'json'
require 'optparse'

options = {}
OptionParser.new do |opts|
  opts.on('--service-principal SERVICE_PRINCIPAL', 'the value of the servicePrincipal field') { |v| options[:service_principal] = v }
  opts.on('--filename FILENAME', 'the sdc json file') { |v| options[:filename] = v }
  opts.on('--accounts ACCOUNTS', Array, 'list of account IDs to add') { |v| options[:accounts] = v }
  opts.on('--accounts-file ACCOUNTS_FILE', 'file containing list of account IDs to add') { |v| options[:accounts_file] = v }
  opts.on('--api-type API_TYPE', 'specify create-slr, service-access or register-da') { |v| options[:api_type] = v }  
  opts.on('--ticket TICKET', 'provide the ticket url for this allowlisting request') { |v| options[:ticket] = v }
end.parse!

data = File.read(options[:filename])
data = JSON.parse(data)

matching_sp = data["allowlistedServicePrincipals"].find { |sp| sp["servicePrincipal"] == options[:service_principal] }

accounts_in_sp = []
data['allowlistedServicePrincipals'].each do |sp|
  sp['accountIdsInServicePrincipal'].each do |account|
    accounts_in_sp << account
  end
end

def allowlist_accounts(api_type, account_list, ticket_list, options, matching_sp, data, accounts_in_sp)
    if options[:accounts]
        options[:accounts].each do |account|
            if api_type == "create-slr"
                if accounts_in_sp.include?(account)
                    abort("\nSercice Account #{account} is already allowlisted under another Service Principal!! Halting execution...\n\n")
                end

                if !account_list.include?(account)
                    account_list << account
                else
                    puts "Account #{account} is already allowlisted under \"accountIdsInServicePrincipal\" of Service Principal \"#{matching_sp['servicePrincipal']}\". Skipping this account..."
                end
                                
                matching_sp["accountIdsInServicePrincipal"] = account_list
            end
            
            if api_type == "service-access"
                if account_list.include?("*")
                    abort("\n\"allowedTargetManagementAccountIds\" is marked as \"*\" for Service Principal \"#{matching_sp["servicePrincipal"]}\". Service access is enabled for ALL accounts by default. Nothing to do here. Aborting...\n\n")
                end

                if !account_list.include?(account)
                    account_list << account
                else
                    puts "Account #{account} is already allowlisted under \"allowedTargetManagementAccountIds\" of Service Principal \"#{matching_sp['servicePrincipal']}\". Skipping this account..."
                end
                                
                matching_sp["allowedTargetManagementAccountIds"] = account_list
            end

            if api_type == "register-da"
                if account_list.include?("*")
                    abort("\n\"allowedTargetManagementAccountIdsForDelegatedAdmin\" is marked as \"*\" for Service Principal \"#{matching_sp["servicePrincipal"]}\". Delegated Admin is enabled for ALL accounts by default. Nothing to do here. Aborting...\n\n")
                end

                if !account_list.include?(account)
                    account_list << account
                else
                    puts "Account #{account.strip} is already allowlisted under \"allowedTargetManagementAccountIdsForDelegatedAdmin\" of Service Principal \"#{matching_sp['servicePrincipal']}\". Skipping this account..."
                end
                
                matching_sp["allowedTargetManagementAccountIdsForDelegatedAdmin"] = account_list
            end
        end        
    end

    if options[:accounts_file]
        File.readlines(options[:accounts_file]).each do |account|
            if api_type == "create-slr"
                if accounts_in_sp.include?(account.strip)
                    abort("Sercice Account #{account.strip} is already allowlisted under another Service Principal!! Halting execution...")
                end

                if !account_list.include?(account.strip)
                    account_list << account.strip
                else
                    puts "Account #{account.strip} is already allowlisted under \"accountIdsInServicePrincipal\" of Service Principal \"#{matching_sp['servicePrincipal']}\". Skipping this account..."
                end
                
                matching_sp["accountIdsInServicePrincipal"] = account_list
            end
            
            if api_type == "service-access"
                if account_list.include?("*")
                    abort("\n\"allowedTargetManagementAccountIds\" is marked as \"*\" for Service Principal \"#{matching_sp["servicePrincipal"]}\". Service access is enabled for ALL accounts by default. Nothing to do here. Aborting...\n\n")
                end

                if !account_list.include?(account.strip)
                    account_list << account.strip
                else
                    puts "Account #{account.strip} is already allowlisted under \"allowedTargetManagementAccountIds\" of Service Principal \"#{matching_sp['servicePrincipal']}\". Skipping this account..."
                end
                
                matching_sp["allowedTargetManagementAccountIds"] = account_list

            end

            if api_type == "register-da"
                if account_list.include?("*")
                    abort("\n\"allowedTargetManagementAccountIdsForDelegatedAdmin\" is marked as \"*\" for Service Principal \"#{matching_sp["servicePrincipal"]}\". Delegated Admin is enabled for ALL accounts by default. Nothing to do here. Aborting...\n\n")
                end
                                
                if !account_list.include?(account.strip)
                    account_list << account.strip
                else
                    puts "Account #{account.strip} is already allowlisted under \"allowedTargetManagementAccountIdsForDelegatedAdmin\" of Service Principal \"#{matching_sp['servicePrincipal']}\". Skipping this account..."
                end
                                
                matching_sp["allowedTargetManagementAccountIdsForDelegatedAdmin"] = account_list
            end
        end
    end
    
    if !ticket_list.include?(options[:ticket])
        ticket_list << options[:ticket]
    end

    File.write('sdc.json', JSON.pretty_generate(data))

end

def create_slr(data, matching_sp, accounts_in_sp, options)
    allowlist_api = matching_sp["accountIdsInServicePrincipal"].dup
    update_ticket = matching_sp["commentsAndRelatedTickets"]
    allowlist_accounts("create-slr", allowlist_api, update_ticket, options, matching_sp, data, accounts_in_sp)
end

def service_access(data, matching_sp, options, accounts_in_sp)
    allowlist_api = matching_sp["allowedTargetManagementAccountIds"].dup
    update_ticket = matching_sp["commentsAndRelatedTickets"]
    allowlist_accounts("service-access", allowlist_api, update_ticket, options, matching_sp, data, accounts_in_sp)
end

def register_da(data, matching_sp, options, accounts_in_sp)
    allowlist_api = matching_sp["allowedTargetManagementAccountIdsForDelegatedAdmin"].dup
    update_ticket = matching_sp["commentsAndRelatedTickets"]
    allowlist_accounts("register-da", allowlist_api, update_ticket, options, matching_sp, data, accounts_in_sp)
end

if matching_sp
    case options[:api_type]
    when "create-slr"
        create_slr(data, matching_sp, accounts_in_sp, options)
    when "service-access"
        service_access(data, matching_sp, options, accounts_in_sp) 
    when "register-da"
        register_da(data, matching_sp, options, accounts_in_sp)
    else
        abort("Invalid API. Exiting execution.")
    end
else
    abort("The Service Principal is not in SDC!! Please reach out to OSI team on-call for assistance...")
end
