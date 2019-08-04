function submit_comment() {
	fetch("./bsview/post_comment.cgi", {
		method: "POST",
		headers: {
			"Content-Type": "text/plain; charset=utf-8"
		},
		body: "name=" + document.getElementById('name').value + 
		      "&post_title=" + window.location.search +
		      "&comment=" + document.getElementById('comment').value,
	}).then(async response => {
		if (response.ok) {
			return response.text();
		} else {
			throw new Error(`Request failed: ${response.status}`);
		}
	})
	.then(text => {
		console.log(text);
		alert("コメントは正常に送信されました。開発中のため登録・公開はされません。");
	})
	.catch(err => console.error(err));
}
