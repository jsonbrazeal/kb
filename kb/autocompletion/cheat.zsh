#compdef kb

declare -a kbs
kbs=$(kb -l | cut -d' ' -f1)
_arguments "1:kbs:(${kbs})" && return 0
