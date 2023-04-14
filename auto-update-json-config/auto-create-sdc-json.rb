require 'json'
require 'optparse'

options = {}
OptionParser.new do |opts|
  opts.on('--service-principal SERVICE_PRINCIPAL', 'the value of the servicePrincipal field') { |v| options[:service_principal] = v }
  opts.on('--filename FILENAME', 'the sdc json file') { |v| options[:filename] = v }
  opts.on('--accounts ACCOUNTS', Array, 'list of account IDs to add') { |v| options[:accounts] = v }
  opts.on('--accounts-file ACCOUNTS_FILE', 'file containing list of account IDs to add') { |v| options[:accounts_file] = v }
  opts.on('--create-slr', 'service accounts allowlisting for CreateSLR') { |v| options[:create_slr] = v }
  opts.on('--service-access', 'management accounts allowlisting for Enable/Disable AWS Service Access') { |v| options[:service_access] = v }
  opts.on('--register-da', 'management accounts allowlisting for enabling Delegated Adiminstrator for member accounts') { |v| options[:register_da] = v }
  opts.on('--ticket TICKET', 'provide the ticket url for this allowlisting request') { |v| options[:ticket] = v }
end.parse!

data = File.read(options[:filename])
data = JSON.parse(data)

matching_sp = data["allowlistedServicePrincipals"].find { |sp| sp["servicePrincipal"] == options[:service_principal] }

if matching_sp
  if options[:create_slr]
    allowlist_api = matching_sp["accountIdsInServicePrincipal"].dup
    update_ticket = matching_sp["commentsAndRelatedTickets"]

    if options[:accounts]
      allowlist_api += options[:accounts]
      if !update_ticket.include?(options[:ticket])
        update_ticket << options[:ticket]
      end
    end

    if options[:accounts_file]
      File.readlines(options[:accounts_file]).each do |account|
        allowlist_api << account.strip
      end
      if !update_ticket.include?(options[:ticket])
        update_ticket << options[:ticket]
      end
    end

    matching_sp["accountIdsInServicePrincipal"] = allowlist_api

    File.write('output.json', JSON.pretty_generate(data))
  end

  if options[:service_access]
    allowlist_api = matching_sp["allowedTargetManagementAccountIds"].dup
    update_ticket = matching_sp["commentsAndRelatedTickets"]

    if options[:accounts]
      allowlist_api += options[:accounts]
      if !update_ticket.include?(options[:ticket])
        update_ticket << options[:ticket]
      end
    end

    if options[:accounts_file]
      File.readlines(options[:accounts_file]).each do |account|
        allowlist_api << account.strip
      end
      if !update_ticket.include?(options[:ticket])
        update_ticket << options[:ticket]
      end
    end

    matching_sp["allowedTargetManagementAccountIds"] = allowlist_api
    
    File.write('output.json', JSON.pretty_generate(data))
  end

  if options[:register_da]
    allowlist_api = matching_sp["allowedTargetManagementAccountIdsForDelegatedAdmin"].dup
    update_ticket = matching_sp["commentsAndRelatedTickets"]

    if options[:accounts]
      allowlist_api += options[:accounts]
      if !update_ticket.include?(options[:ticket])
        update_ticket << options[:ticket]
      end
    end

    if options[:accounts_file]
      File.readlines(options[:accounts_file]).each do |account|
        allowlist_api << account.strip
      end
      if !update_ticket.include?(options[:ticket])
        update_ticket << options[:ticket]
      end
    end

    matching_sp["allowedTargetManagementAccountIdsForDelegatedAdmin"] = allowlist_api

    File.write('output.json', JSON.pretty_generate(data))
  end
else
  puts "The Service Principal is not in SDC!! Please reach out to OSI team on-call for assistance..."
end
