let elementsArray = document.querySelectorAll("form");
const submitReview = (event) => {
	event.preventDefault()
	let form = event.target
	let product_id = form.getAttribute('id')
	let errorMsg = form.querySelector('.errorMessage')
	let successMsg = form.querySelector('.successMessage')
	let csrf_token = form.querySelector('#csrf_token').value
	let reviewString = form.querySelector('.review')
	let rating = form.querySelector('.rating')
	let data = {
		prod_id: product_id,
		csrf_token: csrf_token,
		review: reviewString.value,
		rating: rating.value
	}
	fetch('/submit_review', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		})
		.then(res => res.json())
		.then(data => {
			console.log(data)
			if (data.hasOwnProperty('error')) {
				let errors = data.error
				let errorText = ''
				for (err in errors) {
					errorText = errorText + " - " + errors[err]
				}
				errorMsg.innerHTML = `Errored out ${errorText}`
				errorMsg.style.display = "block"
				reviewString.classList.add('is-invalid')
				setTimeout(() => {
				        errorMsg.textContent=null
				        errorMsg.style.display="none"
				    },3000
				);
			}else{
				successMsg.innerHTML = "The review has been added."
				successMsg.style.display = "block"
				reviewString.value =''
				reviewString.classList.remove('is-invalid')
				setTimeout(() => {
				        successMsg.textContent=null
				        successMsg.style.display="none"
				    },3000
				);
			}
		})
		.catch(error => console.log("Errored out....", error))
}
elementsArray.forEach(function (elem) {
	elem.addEventListener("submit", submitReview)
});