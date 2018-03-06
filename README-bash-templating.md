1. `echo "\$W" | while read ln; do eval echo "$ln"; done > /dev/stdout`
2. `export W=www ; cat tmpl | while IFS='' read ln; do eval echo \""${ln}"\"; done > /dev/stdout`
3. `export W=www ; cat test | while IFS=$'\n' read -r ln; do eval "echo \"${ln}\""; done > /dev/stdout`
4. eval "cat <<EOF\
   \`cat tmpl\`\
   EOF\
   "`
