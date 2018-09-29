function _kb_autocomplete {
    resources=$(kb -l | cut -d' ' -f1)
    COMPREPLY=()
    if [ $COMP_CWORD = 1 ]; then
	COMPREPLY=(`compgen -W "$resources" -- $2`)
    fi
}

complete -F _kb_autocomplete kb
