var s = new WebSocket("ws://localhost:8000")

s.onopen = (e) => {

  $('.smol').removeClass('disabled')
  $('.smol').addClass('enabled')

}


s.onmessage = (e) => {
  console.log(e)
}
