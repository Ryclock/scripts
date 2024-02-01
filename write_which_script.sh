#!/usr/bin/env bash

new_script(){
    if [ $# -ne 1 ]; then
        echo "Usage: $0 folder_path"
        return 1
    fi

    folder_path=$1
    num=$(find "${folder_path}" -type f | wc -l)
    target=$((num+1))
    echo "today new: ${target}"

    read -rp "input script name(null to be back): " file_name

    [ ! "${file_name}" ] && return 1

    if [ -f "./${folder_path}/${file_name}.sh" ];then
        echo "the file has been"
        return 1
    fi

    touch "./${folder_path}/${file_name}.sh"
}

review(){
    if [ $# -ne 1 ]; then
        echo "Usage: $0 folder_path"
        return 1
    fi

    folder_path=$1
    target=$(ls -rt "${folder_path}" | awk 'NR==1')
    echo "today review: ${target}"
}


folder_path="practise/"

while :
do
    read -rp "a new script? " yn
    case "${yn}" in
        'y'|'Y')
            new_script "${folder_path}" && break
        ;;
        'n'|'N')
            break
        ;;
        *)
            echo "only y|Y or n|N"
        ;;
    esac
done

while :
do
    read -rp "review the oldest? " yn
    case "${yn}" in
        'y'|'Y')
            review "${folder_path}" && break
        ;;
        'n'|'N')
            break
        ;;
        *)
            echo "only y|Y or n|N"
        ;;
    esac
done