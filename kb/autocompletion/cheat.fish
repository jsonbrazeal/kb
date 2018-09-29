#completion for kb
complete -c kb -s h -l help -f -x --description "Display help and exit"
complete -c kb -l edit -f -x --description "Edit <resource>"
complete -c kb -s e -f -x --description "Edit <resource>"
complete -c kb -s l -l list -f -x --description "List all available resources"
complete -c kb -s d -l kb-directories -f -x --description "List all current resource dirs"
complete -c kb --authoritative -f
for resource in (kb -l | cut -d' ' -f1)
    complete -c kb -a "$resource"
    complete -c kb -o e -a "$resource"
    complete -c kb -o '-edit' -a "$resource"
end
