let container = document.getElementById('container')


setTimeout(() => {
	container.classList.add('sign-in')
}, 200)

toggle = () => {
	container.classList.toggle('sign-in')
	container.classList.toggle('sign-up')
}
