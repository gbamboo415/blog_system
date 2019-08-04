#!/bin/bash -euxv
source "$(dirname $0)/../conf"
exec 2> "$logdir/$(basename $0).$(date +%Y%m%d_%H%M%S).$$"
set -o pipefail

### VARIABLES ###
Tmp=/tmp/${0##*/}.$$

dd bs=${CONTENT_LENGTH:-0} count=1 |
cgi-name                           > ${Tmp}-cgivars

dir_tmp=$(nameread post_title ${Tmp}-cgivars)
dir="$(tr -dc 'a-zA-Z0-9_=' <<< ${dir_tmp} | sed 's;=;s/;')"
[ -z "$dir" ] && dir="pages/top"
[ "$dir" = "post" ] && dir="$(tail -n 1 "$datadir/post_list" | cut -d' ' -f 3)"
name=$(nameread name ${Tmp}-cgivars)
postdate=$(date '+%Y-%m-%d %H:%M:%S')
comment=$(nameread comment ${Tmp}-cgivars)
commentsfile="$datadir/comments/$(tr '/' '_' <<< $dir)_comments.un.yaml"

### 排他制御開始 ###
lockinst=$(pshlock -w 5 -d lock comment_post)
if [ $? -ne 0 ]; then
  echo '*** failed to lock "comment_post"' 1>&2
  exit 1
fi

### コメントをファイルに記録する ###
echo -e "- name: '${name}'\n  postdate: '${postdate}'\n  comment: '${comment}'" >> ${commentsfile}

### 排他制御終了 ###
punlock "$lockinst"

echo -e "Content-Type: text/plain; charset=utf-8\n"
echo "${CONTENT_LENGTH} bytes Received"
echo "name: ${name}"
echo "comment: ${comment}"
echo "dir: ${dir}"

rm -f $Tmp-cgivars
